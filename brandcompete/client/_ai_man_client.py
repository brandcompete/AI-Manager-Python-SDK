import requests
import json
import base64
import pandas as pd
import PyPDF2
from enum import Enum
from llama_index.core import SimpleDirectoryReader
from llama_index.core import download_loader, Document
from pathlib import Path
from typing import (
    List,
    Optional
)

from brandcompete.core.util import Util
from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import (
    AIModel,
    Attachment,
    DataSource,
    PromptOptions,
    Route,
    Filter,
    Prompt,
    Loader
)


class RequestType(Enum):
    POST = 0,
    GET = 1,
    PUT = 2,
    DELETE = 3


class AIManServiceClient():
    """Represents the AI Manager Service Client
    """

    def __init__(self, credential: TokenCredential) -> None:

        self.credential = credential

    def set_model(self, model: AIModel) -> None:
        pass

    def get_models(self, filter: Optional[Filter] = None) -> List[AIModel]:
        """Get all available models to prompt on

        Args:
            filter (Optional[Filter], optional): Not implemented yet. Defaults to None.

        Returns:
            List[AIModel]: List of available AIModel objects
        """
        results = self._perform_request(
            type=RequestType.GET, route=Route.GET_MODELS.value)
        models = list()
        for model in results['Models']:
            models.append(AIModel.from_dict(model))

        return models

    def prompt(self, **kwargs) -> dict:
        """_summary_

        Args:
            model_id (int): the model id
            query (str): Query to prompt
            loader (Optional[Loader], optional): Content loader. Defaults to None.
            file_append_to_query (Optional[str], optional): Absolute path to a file (The content is added to the query). Defaults to None.
            files_to_rag (Optional[List[str]], optional): Absolute path to a file (File content to rag). Defaults to None.
            prompt_options (Optional[PromptOptions], optional): Prompt options. Defaults to None.

        Raises:
            ValueError: If any of the required parameters are missing

        Returns:
            dict: The API-Response as dict
        """
        if "model_id" in kwargs:
            raise Exception(f"Error: model_id as parameter is deprecated. Use the model_tag instead. Aborting....")
        
        if "model_tag" not in kwargs:
            raise ValueError(f"Error: missing required argument: model_tag")
        
        if "query" not in kwargs:
            raise ValueError(f"Error: missing required argument: query")
        
        model_tag: int = kwargs["model_tag"]
        query = kwargs["query"]
        loader: Optional[Loader] = kwargs["loader"] if "loader" in kwargs else None
        file_append_to_query: Optional[str] = kwargs["file_append_to_query"] if "file_append_to_query" in kwargs else None
        files_to_rag: Optional[List[str]] = kwargs["files_to_rag"] if "files_to_rag" in kwargs else None
        prompt_options: Optional[PromptOptions] = kwargs["prompt_options"] if "prompt_options" in kwargs else None
        
        if loader is not None and file_append_to_query is None and files_to_rag is None:
            raise ValueError(
                f"Missing Argument: file_append_to_query or files_to_rag")

        attachments = list()
        if loader is not None:
            if file_append_to_query is not None:
                doc_content = self.get_document_content(
                    file_path=file_append_to_query, loader=loader)
                if(loader == Loader.IMAGE):
                    encoded_contents = base64.b64encode(doc_content)
                    attachment = Attachment()
                    attachment.name = Util.get_file_name(file_path=file_append_to_query)
                    attachment.base64 = encoded_contents.decode()
                    attachments.append(attachment.to_dict())
                else:
                    query += f" {doc_content}"

            if files_to_rag is not None:

                for file in files_to_rag:
                    content = self.get_document_content(
                        file_path=file, loader=loader)
                    encoded_contents = base64.b64encode(str.encode(content))
                    attachment = Attachment()
                    attachment.name = Util.get_file_name(file_path=file)
                    attachment.base64 = encoded_contents.decode()
                    attachments.append(attachment.to_dict())

        if prompt_options is None:
            prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict
        if len(attachments) > 0:
            prompt_dict['attachments'] = attachments
        
        prompt_dict['raw'] = prompt_options.raw
        prompt_dict['keepContext'] = prompt_options.keep_context
        
        route = Route.PROMPT.value.replace("model_tag", f"{model_tag}")
        response = self._perform_request(
            RequestType.POST, route=route, data=prompt_dict)
        return response

    def prompt_on_datasource(self, datasource_id:int, model_tag_id:int, query:str, prompt_options:PromptOptions = None) -> dict:
        """Prompt on a datasource (by id)

        Args:
            datasource_id (int): The datasource id (related to current account)
            model_tag_id (int): Model tag id
            query (str): The query to prompt
            prompt_options (PromptOptions, optional): Prompt options. Defaults to None.

        Returns:
            dict: The API-Response as dict
        """
        if prompt_options is None:
            prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt.datasource_id = datasource_id
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict
        
        route = f"{Route.PROMPT_WITH_DATASOURCE.value}/{model_tag_id}"
        response = self._perform_request(
            RequestType.POST, route=route, data=prompt_dict)
        return response

    def get_document_content(self, file_path: str, loader: Loader = None) -> Optional[str]:
        """Parsing document content)

        Args:
            file_path (str): The absolute file path
            loader (Loader, optional): Loader to use for parsing (Excel, Image, CSV, PDF, DocX). Defaults to None.

        Returns:
            str: None or string
        """
        if loader == Loader.BASE64_ONLY:
            with open(file_path, "rb") as ragFile:
               return ragFile.read()
        if loader == Loader.EXCEL:
            df = pd.read_excel(file_path)
            return df.to_csv(sep='\t', index=False)

        if loader == Loader.IMAGE:
            with open(file_path, "rb") as imageFile:
               return imageFile.read()
           
        if loader == Loader.CSV:
            df = pd.read_csv(file_path)
            return df.to_csv(sep='\t', index=False)

        if loader == Loader.PDF:
            pdf_reader = PyPDF2.PdfReader(file_path)
            text = ""
            for i in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[i]
                text += page.extract_text()
            return text
        DocxReader = download_loader("DocxReader")

        documents: List[Document] = None

        dir_reader = SimpleDirectoryReader(
            input_files=[file_path],
            file_extractor={
                ".docx": DocxReader()})
        documents = dir_reader.load_data()

        text = ""

        for doc in documents:
            text += doc.get_text()
        return text
    
    def fetch_all_datasources(self) -> List[DataSource]:
        """Fetch all datasources related to the account

        Returns:
            List[DataSource]: List of datasource objects
        """
        fetch_all_response = self._perform_request(RequestType.GET, Route.DATA_SOURCE.value)
        datasources = list()
        for response in fetch_all_response["datasources"]:
            source = self.get_datasource_by_id(response["id"])
            
            datasources.append(source)
        return datasources 
    
    def get_datasource_by_id(self, id:int) -> Optional[DataSource]:
        """Get a specific datasource by id

        Args:
            id (int): the datasource id

        Returns:
            DataSource: None or Datasource object
        """
        #TODO THA 2024-12-13 Check if response has a valid datasource
        
        url = f"{Route.DATA_SOURCE.value}/{id}"
        response = self._perform_request(RequestType.GET, url )
        source = response["datasource"]
        return DataSource(
                id=source["id"],
                name=source["name"],
                summary=source["summary"],
                categories=source["categories"],
                tags=source["tags"],
                status=source["status"],
                media_count=source["mediaCount"],
                owner_id=source["ownerId"],
                assoc_contexts=source["assocContexts"],
                media=source["media"],
                created=source["created"],
                modified=source["modified"]
                )
        
    def init_new_datasource(self, name:str, summary:str, tags:List[str]=[], categories:List[str]= []) -> int:
        """Initiate and add a new datasource to current account

        Args:
            name (str): datasource name
            summary (str): summary
            tags (List[str], optional): A list of tags. Defaults to [].
            categories (List[str], optional): a list of categories. Defaults to [].

        Returns:
            int: The datasource id
        """
        data = {
            "name": name, 
            "summary": summary, 
            "tags": tags, 
            "categories":categories,
            "assocContexts": [],
            "media": []
            }
        response = self._perform_request(type=RequestType.POST, route=Route.DATA_SOURCE.value, data=data)
        
        if "datasource" in response:
            datasource = response["datasource"]
            if "id" in datasource:
                return datasource["id"]
        return -1
        
    def delete_datasource(self, id:int) -> bool:
        """Delete a specific datasource by id

        Args:
            id (int): the datasource id

        Returns:
            bool: success true or false
        """
        code:int = self._perform_request(type=RequestType.DELETE, route=f"{Route.DATA_SOURCE.value}/{id}" )
        return code
    
    def add_documents(self, data_source_id:int, sources:List[str] ) -> DataSource:
        """Add one or more documents (files, urls) to an datasource

        Args:
            data_source_id (int): the datasource id
            sources (List[str]): list of file paths or urls

        Raises:
            Exception: If datasource not exists

        Returns:
            DataSource: the datasource with all added documents (media list)
        """
        datasource:DataSource = self.get_datasource_by_id(id=data_source_id)
        
        for path_or_url in sources:
            path_or_url = path_or_url.lower()
            if Util.validate_url(url=path_or_url, check_only=True):
                datasource.media.append({"name":path_or_url, "mime_type":"text/x-uri"})
                continue
            filename, file_ext = Util.get_file_name_and_ext(file_path=path_or_url)
            loader, mime_type = Util.get_loader_by_ext(file_ext=file_ext)
            if loader is None:
                raise Exception(f"Error: Unsupported filetype:{file_ext} (file:{filename})")
    
            contentBase64 = base64.b64encode(self.get_document_content(file_path=path_or_url, loader=Loader.BASE64_ONLY))        
            size_in_bytes = (len(contentBase64) * (3/4)) - 1
            datasource.media.append({"base64":contentBase64.decode(), "name":filename, "mime_type": mime_type, "size":size_in_bytes * 10})
        return self.update_datasource(datasource=datasource)
    
    
    def update_datasource(self, datasource:DataSource)-> DataSource:
        """Update an existing datasource

        Args:
            datasource (DataSource): The datasource to update

        Returns:
            DataSource: Updated datasource
        """
        data = {
            "name": datasource.name,
            "summary": datasource.summary,
            "categories": datasource.categories,
            "tags": datasource.tags,
            "assocContexts": datasource.assoc_contexts,
            "media": datasource.media}
        
        response = self._perform_request(RequestType.PUT, f"{Route.DATA_SOURCE.value}/{datasource.id}",data=data)
        return response

            
    def _perform_request(self, type: RequestType, route: str, data: dict = None) -> dict:
        """Warning. This method is private and should not be called manually

        Args:
            type (RequestType): Enum of RequestTypes (GET, POST, PUT and DELETE)
            route (str): _description_
            data (dict, optional): _description_. Defaults to None.

        Raises:
            Exception: _description_

        Returns:
            dict: _description_
        """
        if self.credential.auto_refresh_token and Util.is_token_expired(self.credential.access.expires_on):
            self.credential.refresh_access_token()

        url = f"{self.credential.api_host}{route}"
        response = None
        headers = {"accept": "application/json"}
        headers.update({"Authorization": f"Bearer {self.credential.access.token}"})
        if type == RequestType.GET:
            response = requests.get(
                url=url, headers=headers, allow_redirects=True)

        if type == RequestType.POST:
            headers.update({"Content-Type": "application/json"})
            response = requests.post(
                url=url, headers=headers, json=data, allow_redirects=True)
        
        if type == RequestType.DELETE:
            headers.update({"Content-Type": "application/json"})
            response = requests.delete(
                url=url, headers=headers, allow_redirects=True)
            return response.status_code
        
        if type == RequestType.PUT:
            headers.update({"Content-Type": "application/json"})
            response = requests.put(
                url=url, headers=headers, json=data, allow_redirects=True)

        if response.status_code not in [200,201,202]:
            raise Exception(f"[{response.status_code}] Reason: {response.reason}")

        content = json.loads(response.content.decode('utf-8'))
        return content['messageContent']['data']

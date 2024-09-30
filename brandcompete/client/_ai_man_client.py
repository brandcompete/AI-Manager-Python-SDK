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
    Any, Dict, List, Optional, Union,
    TYPE_CHECKING
)

from brandcompete.core.util import Util
from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import (
    AI_Model,
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


class AI_ManServiceClient():

    def __init__(self, credential: TokenCredential) -> None:

        self.credential = credential

    def set_model(self, model: AI_Model) -> None:
        pass

    def get_models(self, filter: Optional[Filter] = None) -> List[AI_Model]:
        results = self._perform_request(
            type=RequestType.GET, route=Route.GET_MODELS.value)
        models = list()
        for model in results['Models']:
            models.append(AI_Model.from_dict(model))

        return models

    def prompt(self, **kwargs) -> dict:
        """_summary_

        Args:
            model_id (int): _description_
            query (str): _description_
            loader (Optional[Loader], optional): _description_. Defaults to None.
            file_append_to_query (Optional[str], optional): _description_. Defaults to None.
            files_to_rag (Optional[List[str]], optional): _description_. Defaults to None.
            prompt_options (Optional[PromptOptions], optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            dict: _description_
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

    def prompt_on_datasource(self, datasource_id:int, model_tag_id:int, query:str, prompt_options:PromptOptions = None) -> str:
        if prompt_options is None:
            prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt.datasourceId = datasource_id
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict
        
        route = f"{Route.PROMPT_WITH_DATASOURCE.value}/{model_tag_id}"
        response = self._perform_request(
            RequestType.POST, route=route, data=prompt_dict)
        return response

    def get_document_content(self, file_path: str, loader: Loader = None) -> str:

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
        fetch_all_response = self._perform_request(RequestType.GET, Route.DATA_SOURCE.value)
        datasources = list()
        for response in fetch_all_response["datasources"]:
            source = self.get_datasource_by_id(response["id"])
            
            datasources.append(source)
        return datasources 
    
    def get_datasource_by_id(self, id:int) -> DataSource:
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
                mediaCount=source["mediaCount"],
                ownerId=source["ownerId"],
                assocContexts=source["assocContexts"],
                media=source["media"],
                created=source["created"],
                modified=source["modified"]
                )
        
    def init_new_datasource(self, name:str, summary:str, tags:List[str]=[], categories:List[str]= []) -> int:
        data = {
            "name": name, 
            "summary": summary, 
            "tags": tags, 
            "categories":categories,
            "assocContexts": [],
            "media": []
            }
        response = self._perform_request(RequestType.POST,Route.DATA_SOURCE.value,data=data)
        
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
        code:int = self._perform_request(RequestType.DELETE, f"{Route.DATA_SOURCE.value}/{id}" )
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
        
        for entry in sources:
            entry = entry.lower()
            if Util.validate_url(entry,check_only=True):
                datasource.media.append({"name":entry, "mime_type":"text/x-uri"})
                continue
            filename, file_ext = Util.get_file_name_and_ext(entry)
            loader, mime_type = Util.get_loader_by_ext(file_ext=file_ext)
            if loader is None:
                raise Exception(f"Error: Unsupported filetype:{file_ext} (file:{filename})")
    
            contentBase64 = base64.b64encode(str.encode(self.get_document_content(file_path=entry,loader=loader)))        
            size_in_bytes = (len(contentBase64) * (3/4)) - 1
            #datasource.media.append({"base64":contentBase64.decode(), "name":filename})
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
            "assocContexts": datasource.assocContexts,
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

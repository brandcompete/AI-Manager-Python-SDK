import requests, json, base64
import pandas as pd
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

    def __init__(self, credential:TokenCredential) -> None:
        
        self.credential = credential   
        
    def set_model(self, model:AI_Model) -> None:
        pass
    
    def get_models(self, filter:Filter = None) -> List[AI_Model]:
        results = self._perform_request(type=RequestType.GET, route=Route.GET_MODELS.value)
        models = list()
        for model in results['Models']:
            models.append(AI_Model.from_dict(model))
        
        return models

    def prompt_with_attachments(self, model_id:int, query:str, file_path:str) -> str:
        prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict
        route = Route.PROMPT.value.replace("model_id", f"{model_id}")

        response = self._perform_request(RequestType.POST,route=route, data=prompt_dict)
        return response['ResponseText']
        pass

    def prompt(self, model_id:int, query:str, loader: Loader = None, file_path:str = None) -> str:

        if loader is not None and file_path is None:
            raise ValueError(f"Missing Argument: file_path (If a loader is passed as argument, you need to set a valid file_path)")            

        prompt_options = PromptOptions()
        prompt = Prompt()
        prompt.prompt = query
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict

        if loader is not None:
            document_text = self.get_document_content( file_path=file_path, loader=loader)            
            encoded_contents = base64.b64encode(str.encode(document_text))
            attachment = Attachment()
            attachment.name = Util.get_file_name(file_path=file_path)
            attachment.base64 = encoded_contents.decode()
            prompt_dict['attachments'] = [attachment.to_dict()] 
        
        route = Route.PROMPT.value.replace("model_id", f"{model_id}")
        response = self._perform_request(RequestType.POST,route=route, data=prompt_dict)
        return response['ResponseText']

    def get_document_content(self, file_path:str, loader: Loader = None) -> str:
    
        if loader == Loader.EXCEL:
            df = pd.read_excel(file_path)
            return df.to_csv(sep='\t', index=False)
        
        if loader == Loader.CSV:
            df = pd.read_csv(file_path)
            return df.to_csv(sep='\t', index=False)
            
        DocxReader = download_loader("DocxReader")
        PDFReader = download_loader("PDFReader")
        documents:List[Document] = None

        dir_reader = SimpleDirectoryReader(
            input_files=[file_path],
            file_extractor={
                ".docx": DocxReader(),
                ".pdf": PDFReader()})
        documents = dir_reader.load_data()

        text = ""

        for doc in documents:
            text += doc.get_text()
        
        print(f"Fetched amount chars: {len(text)}")
        return text

    def _perform_request(self, type: RequestType, route:str, data:dict = None) -> dict:

        if self.credential.auto_refresh_token and Util.is_token_expired(self.credential.access.expires_on):
           self.credential.refresh_access_token()

        url = f"{self.credential.api_host}{route}"
        response = None
        headers = {"accept": "application/json"}
        headers.update({"Authorization": f"Bearer {self.credential.access.token}"})
        if type == RequestType.GET:
            response = requests.get(url=url, headers=headers, allow_redirects=True)

        if type == RequestType.POST:
            headers.update({"Content-Type": "application/json"})
            response = requests.post(url=url, headers=headers, json=data, allow_redirects=True)
        
        if response.status_code != 200:
            raise Exception(f"[{response.status_code}] Reason: {response.reason}")

        content = json.loads(response.content.decode('utf-8'))
        return content['messageContent']['data']
        
        

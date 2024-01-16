import requests, json
from enum import Enum
from llama_index import download_loader
from llama_index.schema import Document
from llama_hub.file.docx import DocxReader
from llama_hub.file.pdf import PDFReader
from llama_hub.file.pandas_excel import PandasExcelReader
from llama_hub.file.simple_csv import SimpleCSVReader
from pathlib import Path
from typing import (
    Any, Dict, List, Optional, Union,
    TYPE_CHECKING
)

from brandcompete.core.credentials import TokenCredential
from brandcompete.core.classes import (
    AI_Model, 
    PromptOptions, 
    Route, 
    Filter, 
    Prompt,
    Loader 
)

from brandcompete.core.util import Util

class RequestType(Enum):
    POST = 0,
    GET = 1,
    PUT = 2,
    DELETE = 3

class AI_ManServiceClient():

    def __init__(self, credential:TokenCredential , **kwargs: Any) -> None:
        
        self.credential = credential   
        
    def set_model(self, model:AI_Model) -> None:
        pass
    
    def get_models(self, filter:Filter = None) -> List[AI_Model]:
        results = self._perform_request(type=RequestType.GET, route=Route.GET_MODELS.value)
        models = list()
        for model in results['Models']:
            models.append(AI_Model.from_dict(model))
        
        return models

    def prompt(self, model_id:int, query:str, loader: Loader = None, file_path:str = None) -> str:

        if loader is not None and file_path is None:
            raise ValueError(f"Missing Argument: file_path (If a loader is passed as argument, you need to set a valid file_path)")            

        prompt_options = PromptOptions()
        prompt = Prompt()

        if loader is not None:
            document_text = self.get_document_content(loader=loader, file_path=file_path)
            query += f'{document_text}'
            
        prompt.prompt = query
        prompt_dict = prompt.to_dict()
        prompt_option_dict = prompt_options.to_dict()
        prompt_dict['options'] = prompt_option_dict
        route = Route.PROMPT.value.replace("model_id", f"{model_id}")
        response = self._perform_request(RequestType.POST,route=route, data=prompt_dict)
        return response['ResponseText']

    def get_document_content(self, loader:Loader, file_path:str) -> str:
        
        documents: List[Document] = None
        if loader is Loader.EXCEL:
            documents = PandasExcelReader(pandas_config={"header": 0}).load_data(file=Path(file_path))
        if loader is Loader.PDF:
            documents = PDFReader().load_data(file=Path(file_path))
        if loader is Loader.CSV: 
            documents = SimpleCSVReader(encoding="utf-8").load_data(file=Path(file_path))
        if loader is Loader.DOCX:
            documents = DocxReader().load_data(file=Path(file_path))
        text = ""

        for doc in documents:
            text += doc.get_text()
        
        print(f"Fetched text out of Documen{file_path}\n")
        print(f"{text}\n")
        print(f"Lenght: {len(text)}")
        return text

    def _perform_request(self, type: RequestType, route:str, data:dict = None) -> dict:

        if self.credential.auto_refresh_token and Util.is_token_expired(self.credential.access.expires_on):
           self.credential.refresh_access_token()

        url = f"{self.credential.api_host}{route}"
        response = None
        headers = {"accept": "application/json"}
        headers.update({"Authorization": f"Bearer {self.credential.access.token}"})
        if type == RequestType.GET:
            response = requests.get(url=url, headers=headers)

        if type == RequestType.POST:
            headers.update({"Content-Type": "application/json"})
            response = requests.post(url=url, headers=headers, json=data)
        
        if response.status_code != 200:
            raise Exception(f"[{response.status_code}] Reason: {response.reason}")

        content = json.loads(response.content.decode('utf-8'))
        return content['messageContent']['data']
        
        

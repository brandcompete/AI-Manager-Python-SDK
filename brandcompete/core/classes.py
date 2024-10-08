from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from dataclasses_json import dataclass_json, LetterCase

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AI_Model:
    id:int
    uuId: str
    type: int
    state: int
    created: str
    modified: str
    name: str
    shortDescription: str
    longDescription: str
    defaultModelTagId: int
    amountOfPulls: str
    amountOfTags: int
    requiredMemory:str
    size: 0

@dataclass_json
@dataclass
class Project:
    id: int
    uuId: str
    type: int
    state: int
    created: str
    modified: str
    ownerId: int
    name: str
    description: str

@dataclass_json
@dataclass
class Query:
    id: int
    uuId: str
    type: int
    state: int
    created: str
    modified: str

@dataclass
class Filter:
    order_by:int = 1

@dataclass_json
@dataclass
class PromptOptions:
    mirostat:int=0
    mirostat_eta:float=0.1
    mirostat_tau:int=5
    num_ctx:int=4096
    num_gqa:int=8
    num_gpu:int=0
    num_thread:int=0
    repeat_last_n:int=64
    repeat_penalty:float=1.1
    temperature:float=0.8
    seed:int=0
    stop=None
    tfs_z:int=1
    num_predict:int=2048
    top_k:int=40
    top_p:float=0.9
    raw:bool = False
    keep_context:bool = True

@dataclass_json
@dataclass
class Prompt:
    prompt:str=""
    modelTagId:int=0
    raw:bool=False
    stream:bool=False
    projectId:int=1
    projectTabId:int=1
    userId:int=1
    verbose:int=True
    attachments:list = None
    keepContext:bool = True
    keepAlive:str = "5m"
    datasourceId:int = 0 

@dataclass_json
@dataclass
class DataSource:
    name:str
    summary:str
    id:Optional[int] = -1
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    assocContexts: Optional[list] = None
    media: Optional[list] = None
    status:Optional[int] = -1
    mediaCount:Optional[int] = -1
    ownerId:Optional[int] = -1
    created:Optional[str] = None
    modified:Optional[str] = None

@dataclass_json
@dataclass
class Media:
    base64:str
    
@dataclass_json
@dataclass   
class Attachment:
    name:str=""
    base64:str=""

class Route(Enum):
    GET_MODELS='/api/v1/models'
    AUTH= '/api/v1/auth/authenticate'
    AUTH_REFRESH = '/api/v1/auth/refresh'
    PROMPT = '/api/v1/prompts/model_tag'
    PROMPT_WITH_DATASOURCE = '/api/v1/prompts'
    DATA_SOURCE = '/api/v1/datasources'

class Loader(Enum):
    PDF = "PDFReader",
    EXCEL = "PandasExcelReader",
    DOCX = "DocxReader",
    CSV = "SimpleCSVReader",
    URL = "url",
    IMAGE = "img"

__all__ = [

    AI_Model,
    Project,
    Query,
    Route,
    Prompt,
    Loader
]
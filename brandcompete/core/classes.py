"""Module providing different dataclasses"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class AIModel:

    """Represents a AIModel instance"""
    id: int
    uu_id: str
    name: str
    short_description: str
    long_description: str
    default_model_tag_id: int
    amount_of_pulls: str
    amount_of_tags: int
    required_memory: str
    size: int = 0

    @classmethod
    def to_dict(cls):
        """Parsing a AIModel Instance to a dict"""
        return {
            "id": cls.id,
            "uuId": cls.uuid,
            "name": cls.name,
            "shortDescription": cls.short_description,
            "longDescription": cls.long_description,
            "defaultModelTagId": cls.default_model_tag_id,
            "amountOfPulls": cls.amount_of_pulls,
            "amountOfTags": cls.amount_of_tags,
            "requiredMemory": cls.required_memory,
            "size": cls.size
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a AIModel Instance"""
        cls.id = values["id"]
        cls.uuid = values["uuId"]
        cls.owner_id = values["name"]
        cls.name = values["shortDescription"]
        cls.description = values["longDescription"]
        cls.owner_id = values["defaultModelTagId"]
        cls.name = values["amountOfPulls"]
        cls.description = values["amountOfTags"]
        cls.owner_id = values["requiredMemory"]
        cls.name = values["size"]


@dataclass
class Project:
    """Represents an aiman project"""
    id: int
    uuid: str
    owner_id: int
    name: str
    description: str

    @classmethod
    def to_dict(cls):
        """Parsing a Projcet Instance to a dict"""
        return {
            "id":           cls.id,
            "uuId":         cls.uuid,
            "ownerId":      cls.owner_id,
            "name":         cls.name,
            "description":  cls.description
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Projcet Instance"""
        cls.id = values["id"]
        cls.uuid = values["uuId"]
        cls.owner_id = values["ownerId"]
        cls.name = values["name"]
        cls.description = values["description"]


@dataclass
class Query:
    """Represents a prompt query"""
    id: int
    uuid: str

    @classmethod
    def to_dict(cls):
        """Parsing a Projcet Instance to a dict"""
        return {
            "id":   cls.id,
            "uuId": cls.uuid
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Projcet Instance"""
        cls.id = values["id"]
        cls.uuid = values["uuId"]


@dataclass
class PromptOptions:
    """Represents prompt options"""
    mirostat: int = 0
    mirostat_eta: float = 0.1
    mirostat_tau: int = 5
    num_ctx: int = 4096
    num_gqa: int = 8
    num_gpu: int = 0
    num_thread: int = 0
    repeat_last_n: int = 64
    repeat_penalty: float = 1.1
    temperature: float = 0.8
    seed: int = 0
    stop = None
    tfs_z: int = 1
    num_predict: int = 2048
    top_k: int = 40
    top_p: float = 0.9
    raw: bool = False
    keep_context: bool = True

    @classmethod
    def to_dict(cls):
        """Parsing a Projcet Instance to a dict"""
        return {
            "mirostat":         cls.mirostat,
            "mirostat_eta":     cls.mirostat_eta,
            "mirostat_tau":     cls.mirostat_tau,
            "num_ctx":          cls.num_ctx,
            "num_gqa":          cls.num_gqa,
            "num_gpu":          cls.num_gpu,
            "num_thread":       cls.num_thread,
            "repeat_last_n":    cls.repeat_last_n,
            "repeat_penalty":   cls.repeat_penalty,
            "temperature":      cls.temperature,
            "seed":             cls.seed,
            "stop":             cls.stop,
            "tfs_z":            cls.tfs_z,
            "num_predict":      cls.num_predict,
            "top_k":            cls.top_k,
            "top_p":            cls.top_p,
            "raw":              cls.raw,
            "keep_context":     cls.keep_context
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Projcet Instance"""
        cls.mirostat = values["mirostat"]
        cls.mirostat_eta = values["mirostat_eta"]
        cls.mirostat_tau = values["mirostat_tau"]
        cls.num_ctx = values["num_ctx"]
        cls.num_gqa = values["num_gqa"]
        cls.num_gpu = values["num_gpu"]
        cls.num_thread = values["num_thread"]
        cls.repeat_last_n = values["repeat_last_n"]
        cls.repeat_penalty = values["repeat_penalty"]
        cls.temperature = values["temperature"]
        cls.seed = values["seed"]
        cls.stop = values["stop"]
        cls.tfs_z = values["tfs_z"]
        cls.num_predict = values["num_predict"]
        cls.top_k = values["top_k"]
        cls.top_p = values["top_p"]
        cls.raw = values["raw"]
        cls.keep_context = values["keep_context"]


@dataclass
class Prompt:
    """Represents a prompt"""
    prompt: str = ""
    model_tag_id: int = 0
    raw: bool = False
    stream: bool = False
    project_id: int = 1
    project_tab_id: int = 1
    user_id: int = 1
    verbose: int = True
    attachments: list = None
    keep_context: bool = True
    keep_alive: str = "5m"
    datasource_id: int = 0

    @classmethod
    def to_dict(cls):
        """Parsing a Prompt Instance to a dict"""
        return {
            "prompt":       cls.prompt,
            "modelTagId":   cls.model_tag_id,
            "raw":          cls.raw,
            "stream":       cls.stream,
            "projectId":    cls.project_id,
            "projectTabId": cls.project_tab_id,
            "userId":       cls.user_id,
            "verbose":      cls.verbose,
            "attachments":  cls.attachments,
            "keepContext":  cls.keep_context,
            "keepAlive":    cls.keep_alive,
            "datasourceId": cls.datasource_id
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Prompt Instance"""
        cls.prompt = values["prompt"]
        cls.model_tag_id = values["modelTagId"]
        cls.raw = values["raw"]
        cls.stream = values["projectId"]
        cls.project_id = values["projectTabId"]
        cls.user_id = values["userId"]
        cls.verbose = values["verbose"]
        cls.repeat_last_n = values["attachments"]
        cls.keep_context = values["keepContext"]
        cls.keep_alive = values["keepAlive"]
        cls.datasource_id = values["datasourceId"]


@dataclass
class DataSource:
    """Represents a prompt datasource (raging)"""
    name: str
    summary: str
    id: Optional[int] = -1
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    assoc_contexts: Optional[list] = None
    media: Optional[list] = None
    status: Optional[int] = -1
    media_count: Optional[int] = -1
    owner_id: Optional[int] = -1

    @classmethod
    def to_dict(cls):
        """Parsing a DataSource Instance to a dict"""
        return {
            "name":             cls.name,
            "summary":          cls.summary,
            "id":               cls.categories,
            "categories":       cls.categories,
            "tags":             cls.tags,
            "assocContexts":    cls.assoc_contexts,
            "media":            cls.media,
            "status":           cls.status,
            "mediaCount":       cls.media_count,
            "ownerId":          cls.owner_id
        }

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a DataSource Instance"""
        cls.name = values["name"]
        cls.summary = values["summary"]
        cls.id = values["id"]
        cls.categories = values["categories"]
        cls.tags = values["tags"]
        cls.assoc_contexts = values["assocContexts"]
        cls.media = values["media"]
        cls.status = values["status"]
        cls.media_count = values["mediaCount"]
        cls.owner_id = values["ownerId"]


@dataclass
class Media:
    """Represents a prompt media"""
    base64: str

    @classmethod
    def to_dict(cls):
        """Parsing a Media Instance to a dict"""
        return { "base64":  cls.base64}

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Media Instance"""
        cls.base64 = values["base64"]


@dataclass
class Attachment:
    """Represents an prompt attachment"""
    name: str = ""
    base64: str = ""

    @classmethod
    def to_dict(cls):
        """Parsing a Media Instance to a dict"""
        return { "base64":  cls.base64, "name": cls.name}

    @classmethod
    def from_dict(cls, values: dict):
        """Parsing a dict to a Media Instance"""
        cls.name = values["name"]
        cls.base64 = values["base64"]


class Route(Enum):
    """Enumeration of different routes"""
    GET_MODELS = '/api/v1/models'
    AUTH = '/api/v1/auth/authenticate'
    AUTH_REFRESH = '/api/v1/auth/refresh'
    PROMPT = '/api/v1/prompts/model_tag'
    PROMPT_WITH_DATASOURCE = '/api/v1/prompts'
    DATA_SOURCE = '/api/v1/datasources'


class Loader(Enum):
    """Enumeration of different loader"""
    PDF = "PDFReader"
    EXCEL = "PandasExcelReader"
    BASE64_ONLY = "Base64"
    DOCX = "DocxReader"
    CSV = "SimpleCSVReader"
    URL = "url"
    IMAGE = "img"


class RequestType(Enum):
    """Enumeration of different request types"""
    POST = 0
    GET = 1
    PUT = 2
    DELETE = 3


__all__ = [
    "AIModel",
    "Project",
    "Query",
    "Route",
    "Prompt",
    "Loader",
    "RequestType"
]

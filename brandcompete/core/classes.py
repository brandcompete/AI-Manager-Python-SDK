"""Module providing different dataclasses"""
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


@dataclass
class AIModel:

    """Represents a AIModel instance"""
    id: int = -1
    uuid: str = ""
    name: str = ""
    short_description: str = ""
    long_description: str = ""
    default_model_tag_id: int = -1
    amount_of_pulls: str = ""
    amount_of_tags: int = -1
    required_memory: str = -1
    size: int = -1


    def to_dict(self):
        """Parsing a AIModel Instance to a dict"""
        return {
            "id": self.id,
            "uuId": self.uuid,
            "name": self.name,
            "shortDescription": self.short_description,
            "longDescription": self.long_description,
            "defaultModelTagId": self.default_model_tag_id,
            "amountOfPulls": self.amount_of_pulls,
            "amountOfTags": self.amount_of_tags,
            "requiredMemory": self.required_memory,
            "size": self.size
        }


    def from_dict(self, values: dict):
        """Parsing a dict to a AIModel Instance"""
        self.id = 0 if "id" not in values else values["id"]
        self.uuid = "" if "uuId" not in values else values["uuId"]
        self.name = "" if "name" not in values else values["name"]
        self.short_description = "" if "shortDescription" not in values else values["shortDescription"]
        self.long_description = "" if "longDescription" not in values else values["longDescription"]
        self.default_model_tag_id = 0 if "defaultModelTagId" not in values else values["defaultModelTagId"]
        self.amount_of_pulls = "" if "amountOfPulls" not in values else values["amountOfPulls"]
        self.amount_of_tags = 0 if "amountOfTags" not in values else values["amountOfTags"]
        self.required_memory = "" if "requiredMemory" not in values else values["requiredMemory"]
        self.size = 0 if "size" not in values else values["size"]
        return self


@dataclass
class Project:
    """Represents an aiman project"""
    id: int = -1
    uuid: str = ""
    owner_id: int = -1
    name: str = ""
    description: str = ""

    def to_dict(self):
        """Parsing a Projcet Instance to a dict"""
        return {
            "id":           self.id,
            "uuId":         self.uuid,
            "ownerId":      self.owner_id,
            "name":         self.name,
            "description":  self.description
        }

    def from_dict(self, values: dict):
        """Parsing a dict to a Projcet Instance"""
        self.id = values["id"]
        self.uuid = values["uuId"]
        self.owner_id = values["ownerId"]
        self.name = values["name"]
        self.description = values["description"]
        return self


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
        return cls


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

    def to_dict(self):
        """Parsing a Projcet Instance to a dict"""
        return {
            "mirostat":         self.mirostat,
            "mirostat_eta":     self.mirostat_eta,
            "mirostat_tau":     self.mirostat_tau,
            "num_ctx":          self.num_ctx,
            "num_gqa":          self.num_gqa,
            "num_gpu":          self.num_gpu,
            "num_thread":       self.num_thread,
            "repeat_last_n":    self.repeat_last_n,
            "repeat_penalty":   self.repeat_penalty,
            "temperature":      self.temperature,
            "seed":             self.seed,
            "stop":             self.stop,
            "tfs_z":            self.tfs_z,
            "num_predict":      self.num_predict,
            "top_k":            self.top_k,
            "top_p":            self.top_p,
            "raw":              self.raw,
            "keep_context":     self.keep_context
        }

    def from_dict(self, values: dict):
        """Parsing a dict to a Projcet Instance"""
        self.mirostat = 0 if "mirostat" not in values else values["mirostat"]
        self.mirostat_eta = 100 if "mirostat_eta" not in values else values["mirostat_eta"]
        self.mirostat_tau = 5 if "mirostat_tau" not in values else values["mirostat_tau"]
        self.num_ctx = 4096 if "num_ctx" not in values else values["num_ctx"]
        self.num_gqa = 8 if "num_gqa" not in values else values["num_gqa"]
        self.num_gpu = 0 if "num_gpu" not in values else values["num_gpu"]
        self.num_thread = 0 if "num_thread" not in values else values["num_thread"]
        self.repeat_last_n = 64 if "repeat_last_n" not in values else values["repeat_last_n"]
        self.repeat_penalty = 1.1 if "repeat_penalty" not in values else values["repeat_penalty"]
        self.temperature = 0.8 if "temperature" not in values else values["temperature"]
        self.seed = 0 if "seed" not in values else values["seed"]
        self.stop = None if "stop" not in values else values["stop"]
        self.tfs_z = 1 if "tfs_z" not in values else values["tfs_z"]
        self.num_predict = 2048 if "num_predict" not in values else values["num_predict"]
        self.top_k = 40 if "top_k" not in values else values["top_k"]
        self.top_p = 0.9 if "top_p" not in values else values["top_p"]
        self.raw = False if "raw" not in values else values["raw"]
        self.keep_context = True if "keep_context" not in values else values["keep_context"]
        return self


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

    def to_dict(self):
        """Parsing a Prompt Instance to a dict"""
        return {
            "prompt":       self.prompt,
            "modelTagId":   self.model_tag_id,
            "raw":          self.raw,
            "stream":       self.stream,
            "projectId":    self.project_id,
            "projectTabId": self.project_tab_id,
            "userId":       self.user_id,
            "verbose":      self.verbose,
            "attachments":  self.attachments,
            "keepContext":  self.keep_context,
            "keepAlive":    self.keep_alive,
            "datasourceId": self.datasource_id
        }

    def from_dict(self, values: dict):
        """Parsing a dict to a Prompt Instance"""
        self.prompt = "" if "prompt" not in values else values["prompt"]
        self.model_tag_id = 0 if "modelTagId" not in values else values["modelTagId"]
        self.raw = False if "raw" not in values else values["raw"]
        self.stream = False if "stream" not in values else values["stream"]
        self.project_id = False if "projectId" not in values else values["projectId"]
        self.project_tab_id = 0 if "projectTabId" not in values else values["projectTabId"]
        self.user_id = 0 if "userId" not in values else values["userId"]
        self.verbose = True if "verbose" not in values else values["verbose"]
        self.attachments = None if "attachments" not in values else values["attachments"]
        self.keep_context = True if "keepContext" not in values else values["keepContext"]
        self.keep_alive = "5m" if "keepAlive" not in values else values["keepAlive"]
        self.datasource_id = 0 if "datasourceId" not in values else values["datasourceId"]
        return self


@dataclass
class DataSource:
    """Represents a prompt datasource (raging)"""
    name: str = ""
    summary: str = ""
    id: Optional[int] = -1
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    assoc_contexts: Optional[list] = None
    media: Optional[list] = None
    status: Optional[int] = -1
    media_count: Optional[int] = -1
    owner_id: Optional[int] = -1

    def to_dict(self):
        """Parsing a DataSource Instance to a dict"""
        return {
            "name":             self.name,
            "summary":          self.summary,
            "id":               self.categories,
            "categories":       self.categories,
            "tags":             self.tags,
            "assocContexts":    self.assoc_contexts,
            "media":            self.media,
            "status":           self.status,
            "mediaCount":       self.media_count,
            "ownerId":          self.owner_id
        }

    def from_dict(self, values: dict):
        """Parsing a dict to a DataSource Instance"""
        self.name = values["name"]
        self.summary = values["summary"]
        self.id = values["id"]
        self.categories = values["categories"]
        self.tags = values["tags"]
        self.assoc_contexts = values["assocContexts"]
        self.media = values["media"]
        self.status = values["status"]
        self.media_count = values["mediaCount"]
        self.owner_id = values["ownerId"]
        return self


@dataclass
class Media:
    """Represents a prompt media"""
    base64: str = ""

    def to_dict(self):
        """Parsing a Media Instance to a dict"""
        return { "base64":  self.base64}

    def from_dict(self, values: dict):
        """Parsing a dict to a Media Instance"""
        self.base64 = values["base64"]
        return self


@dataclass
class Attachment:
    """Represents an prompt attachment"""
    name: str = ""
    base64: str = ""
    size: int = 0
    mime_type: str = ""

    def to_dict(self):
        """Parsing a Media Instance to a dict"""
        return {
            "base64":   self.base64,
            "name":     self.name,
            "size":     self.size,
            "mime_type":self.mime_type
        }

    def from_dict(self, values: dict):
        """Parsing a dict to a Media Instance"""
        if values == {}:
            return self
        if "name" in values:
            self.name = values["name"]
        if "base64" in values:
            self.base64 = values["base64"]
        if "size" in values:
            self.size = values["size"]
        if "mime_type" in values:
            self.mime_type = values["mime_type"]
        return self


class Route(Enum):
    """Enumeration of different routes"""
    BASE = '/api/v1/'
    GET_MODELS = f'{BASE}models'
    AUTH = f'{BASE}auth/authenticate'
    AUTH_REFRESH = f'{BASE}auth/refresh'
    PROMPT = f'{BASE}prompts/model_tag'
    PROMPT_WITH_DATASOURCE = f'{BASE}prompts'
    DATA_SOURCE = f'{BASE}datasources'


class RequestType(Enum):
    """Enumeration of different request types"""
    POST = 0
    GET = 1
    PUT = 2
    DELETE = 3

class Loader(Enum):
    """Enumeration of different loader"""
    PDF = "PDFReader"
    EXCEL = "PandasExcelReader"
    BASE64_ONLY = "Base64"
    DOCX = "DocxReader"
    CSV = "SimpleCSVReader"
    URL = "url"
    IMAGE = "img"


__all__ = [
    "AIModel",
    "Project",
    "Query",
    "Route",
    "Prompt",
    "RequestType"
]

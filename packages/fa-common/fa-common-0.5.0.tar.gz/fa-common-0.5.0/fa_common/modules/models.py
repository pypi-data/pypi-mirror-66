from enum import Enum

from fa_common.db import DocumentDBModel


class ModuleType(str, Enum):
    SYNC = "sync"  # Is run via a service call
    ASYNC = "async"  # Is executed via gitlab ci


class ScidraModule(DocumentDBModel):
    version: str
    module_type: ModuleType

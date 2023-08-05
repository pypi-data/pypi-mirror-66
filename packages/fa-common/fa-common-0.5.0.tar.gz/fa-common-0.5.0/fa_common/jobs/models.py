from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

from fa_common import CamelModel
from fa_common.db import DocumentDBModel


class InversionRunner(str, Enum):
    DOCKER = "docker"
    PEARCEY = "pearcey"


class JobStatus(str, Enum):
    NOT_SET = ""
    RECEIVED = "RECEIVED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    FAILED = "FAILED"


class ScidraJob(DocumentDBModel):
    project_id: str
    user_id: str
    module_id: str
    status: Optional[JobStatus]
    inputs: dict = {}
    outputs: dict = {}

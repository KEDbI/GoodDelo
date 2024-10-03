from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TaskDescription(BaseModel):
    description: str


class CreateTask(TaskDescription):
    user: str


class TaskResponse(CreateTask):
    model_config = ConfigDict(from_attributes=True)

    id: int
    completed: bool | None
    created_at: datetime


class UpdateTask(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    description: str | None = None # новое описание
    completed: bool | None
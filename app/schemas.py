from pydantic import BaseModel, field_validator, ConfigDict

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    completed: bool = False
    priority: int = 1

    @field_validator("title")
    def title_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Title cannot be empty")
        return value

    @field_validator("priority")
    def priority_must_be_non_negative(cls, value: int) -> int:
        if value is None:
            return value
        if value < 0:
            raise ValueError("Priority must be non-negative")
        return value

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    priority: int | None = None

    @field_validator("title")
    def title_not_empty_if_provided(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("Title cannot be empty")
        return value

    @field_validator("priority")
    def priority_non_negative_if_provided(cls, value: int | None) -> int | None:
        if value is not None and value < 0:
            raise ValueError("Priority must be non-negative")
        return value

class TaskRead(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    priority: int

    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    model_config = ConfigDict(frozen=True)

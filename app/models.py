from pydantic import BaseModel

class MessageModel(BaseModel):
    id: int | None = None
    message: str

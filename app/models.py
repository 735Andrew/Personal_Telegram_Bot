from pydantic import BaseModel, Field
from typing import Optional


class LogInSchema(BaseModel):
    login: str = Field(pattern="^@", min_length=2)
    password: str = Field(min_length=5)



class UserSchema(LogInSchema):
    u_id: Optional[int] = None
    name: str

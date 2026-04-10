from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: str | None = None


class UserMe(BaseModel):
    id: int
    email: str
    role: Optional[str] = None

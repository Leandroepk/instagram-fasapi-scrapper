from pydantic import BaseModel


class Cookie(BaseModel):
    domain: str
    expiry: int = None
    httpOnly: bool
    name: str
    path: str
    sameSite: str
    secure: bool
    value: str

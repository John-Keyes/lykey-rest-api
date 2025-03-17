from enum import Enum
from pydantic import BaseModel

class Role(Enum):
    GUEST = 1
    USER = 2

class AuthForgot(BaseModel):
    email: str

class AuthLogin(AuthForgot):
    password: str

class AuthVerify(AuthLogin):
    code: str = ""

class AuthUpdate(AuthVerify):
    country: str = ""
    pic: str = ""

class Token(BaseModel):
    accessToken: str
    tokenType: str
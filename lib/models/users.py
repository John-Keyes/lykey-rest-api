from lib.models.auth import AuthUpdate, Role
from pydantic import BaseModel

class User(AuthUpdate):
    isVerified: str
    userId: int
    role: Role

class SafeUser(BaseModel):
    userId: int
    email: str
    country: str = ""
    pic: str = ""
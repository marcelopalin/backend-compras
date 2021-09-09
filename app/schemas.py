from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    nome: Optional[str]
    email: str

class UserCreate(UserBase):
    password: str
    
class UserUpdate(BaseModel):
    id: int
    nome: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]


class UserSaida(BaseModel):
    nome: str
    email: str
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


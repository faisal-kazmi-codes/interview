from pydantic import BaseModel, EmailStr, constr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone_number: Optional[str]
    password: constr(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

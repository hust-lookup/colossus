from pydantic import BaseModel

class UserCreate(BaseModel):
    first_name: str
    sur_name: str
    email: str
    password: str

class UserInDB(BaseModel):
    first_name: str
    sur_name: str
    email: str
    hashed_password: str

class UserLogin(BaseModel):
    email: str
    password: str
 

from pydantic import BaseModel


## Based on tutorial example at 
## https://fastapi.tiangolo.com/tutorial/extra-models/
class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str = None
    is_admin: bool

class UserOut(BaseModel):
    username: str
    email: str
    full_name: str = None
    is_admin: bool

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: str
    full_name: str = None
    is_admin: bool

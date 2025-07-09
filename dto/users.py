from pydantic import BaseModel
from typing import Dict, Any

class ProfileDTO(BaseModel):
  userId: str
  introduction: str
  data: Dict[str, Any] 

class UserCreateDTO(BaseModel):
  email: str
  password: str

  
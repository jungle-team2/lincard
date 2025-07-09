from pydantic import BaseModel
from typing import Dict, Any, List


class ProfileDTO(BaseModel):
    userId: str
    introduction: str
    data: Dict[str, Any]
    email: str
    name: str
    avatarId: int


class UserCreateDTO(BaseModel):
    email: str
    password: str


class RecommendItemDTO(BaseModel):
    title: str
    url: str
    description: str


class RecommendsResponseDTO(BaseModel):
    userId: str
    recommends: List[RecommendItemDTO]

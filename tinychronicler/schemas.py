from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ChronicleBase(BaseModel):
    title: str
    description: str


class ChronicleIn(ChronicleBase, BaseModel):
    pass


class Chronicle(ChronicleBase, BaseModel):
    id: int

    class Config:
        orm_mode = True


class ChronicleOut(ChronicleBase, BaseModel):
    id: int
    created_at: datetime


class FileBase(BaseModel):
    mime: str
    name: str
    url: str
    thumb_name: str
    thumb_url: str


class FileIn(FileBase, BaseModel):
    path: str
    thumb_path: str


class File(FileBase, BaseModel):
    id: int
    path: str
    thumb_path: str

    class Config:
        orm_mode = True


class FileOut(FileBase, BaseModel):
    id: int
    created_at: datetime


class CompositionBase(BaseModel):
    is_ready: bool
    title: str


class CompositionIn(CompositionBase, BaseModel):
    data: Optional[bytes] = None


class Composition(CompositionBase, BaseModel):
    id: int
    data: Optional[bytes] = None

    class Config:
        orm_mode = True


class CompositionOut(CompositionBase, BaseModel):
    created_at: datetime
    id: int

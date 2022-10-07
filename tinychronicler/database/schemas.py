from datetime import datetime
from typing import List, Optional, Tuple

from pydantic import BaseModel, Field


class ChronicleBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)


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
    version: int


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


class CompositionDataParameters(BaseModel):
    parameters: List[str]
    module: Tuple[int, int]


class CompositionData(BaseModel):
    notes: List[Tuple[float, float]]
    parameters: List[CompositionDataParameters]


class CompositionDataOut(CompositionBase, BaseModel):
    created_at: datetime
    data: Optional[CompositionData] = None
    id: int


class IOTest(BaseModel):
    name: str

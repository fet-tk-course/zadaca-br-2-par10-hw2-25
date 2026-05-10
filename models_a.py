from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date


class Album(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    artist: str
    release_year: int
    price: float= Field(default=0.0)
    is_available: bool = Field(default=True)  
    world_premiere: date  

class AlbumCreate(SQLModel): 
    title: str
    artist: str
    release_year: int
    price: float = Field(default=0.0)
    is_available: bool = Field(default=True)  
    world_premiere: date


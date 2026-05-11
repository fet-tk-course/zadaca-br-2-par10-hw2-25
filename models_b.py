from sqlmodel import SQLModel, Field
from typing import Optional

#Osnovni model sa svim poljima koje pjesma ima
class SongBase(SQLModel):
    title: str
    artist: str
    duration: int  # Duration u sekundama
    is_available: bool = Field(default=True)
    genre: Optional[str] = None
    album_id: Optional[int] = None  # Veza sa Albumom, može biti null ako pjesma nije povezana s albumom

#Klasa koja predstavlja tabelu u bazi podataka, nasljeđuje SongBase i dodaje id polje koje je primarni ključ
class Song(SongBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

#Shema za kreiranje nove pjesme (POST zahtjev)
class SongCreate(SongBase):
    pass

#Shema za djelimicno ažuriranje pjesme (PATCH zahtjev), sva polja su opcionalna
class SongUpdate(SQLModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    is_available: Optional[bool] = None
    genre: Optional[str] = None
    album_id: Optional[int] = None 

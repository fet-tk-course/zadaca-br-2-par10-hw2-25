from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

#Osnovni model sa svim poljima koje pjesma ima
class SongBase(SQLModel):
    title: str
    artist: str
    duration: int  # Duration u sekundama
    price: float = 0.0
    is_available: bool = Field(default=True)
    genre: Optional[str] = None
    album_id: Optional[int] = None  # Veza sa Albumom, može biti null ako pjesma nije povezana s albumom

#Klasa koja predstavlja tabelu u bazi podataka, nasljeđuje SongBase i dodaje id polje koje je primarni ključ
class Song(SongBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

#Shema za kreiranje nove pjesme (POST zahtjev)
class SongCreate(SongBase):
    pass
    @field_validator('title')
    @classmethod
    def not_empty_title(cls, v):
        if not v.strip():
            raise ValueError('Naziv pjesme ne smije biti prazan string!')
        return v
    
    @field_validator('artist')
    @classmethod
    def not_empty_artist(cls, v):
        if not v.strip():
            raise ValueError('Naziv izvođača ne smije biti prazan string!')
        return v
    
    @classmethod
    def positive_duration(cls, v):
        if v <= 0:
            raise ValueError('Trajanje pjesme mora biti pozitivan broj!')
        return v
    


#Shema za djelimicno ažuriranje pjesme (PATCH zahtjev), sva polja su opcionalna
class SongUpdate(SQLModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[int] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    genre: Optional[str] = None
    album_id: Optional[int] = None 

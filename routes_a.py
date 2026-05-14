from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import field_validator
from sqlmodel import Session, select
from typing import List, Optional
from models_a import Album, AlbumCreate, AlbumUpdate, AlbumFilter
from database import get_session
from models_a import MyResourceCreate


router = APIRouter(prefix="/Albumi", tags=["Resurs A"])
@router.get("/", response_model=List[Album])
def read_albums(
    params:AlbumFilter=Depends(),
    session = Depends(get_session)
):
    query=select(Album)
    filters=params.model_dump(exclude_none=True)
    for key, value in filters.items():
        if key in ["title", "artist"]:
            query=query.where(getattr(Album, key).ilike(f"%{value}%"))
        elif key=="price":
            query=query.where(Album.price<=value)
        elif hasattr(Album, key):
            query=query.where(getattr(Album, key)==value)
                    
    albums=session.exec(query).all()
    return albums

#Zadatak 2
@router.get("/count", response_model=int)
def count_albums(session: Session=Depends(get_session)):
    count=session.exec(select(Album)).count()
    return count



@router.get("/{album_id}", response_model=Album)
def read_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    return db_album 



#Zadatak 1a
@field_validator("price")
@classmethod
def validate_price(cls, value):
    if value is not None and value > 10000:
        raise ValueError("Cijena ne smije biti veća od 10000")
    return value

@field_validator("title")
@classmethod
def validate_title(cls, value):
    if not value.strip():
        raise ValueError("Naslov ne smije biti prazan")
    return value

@field_validator("release_year")
@classmethod
def validate_release_year(cls, value):
    if value is not None and value == float('inf'):
        raise ValueError("Godina izdavanja mora biti cijeli broj")
    return value


@router.post("/", response_model=Album, status_code=status.HTTP_201_CREATED)
def create_album(album: AlbumCreate, session: Session = Depends(get_session)):
    if album.price  is not None and album.price > 10000: #Zadatak 1b
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cijena ne smije biti veća od 10000")
    if album.release_year is not None and album.release_year == float('inf'):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Godina izdavanja mora biti cijeli broj")
    if album.title.strip() == "":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Naslov ne smije biti prazan")
    new_db_album = Album.model_validate(album)
    session.add(new_db_album)
    session.commit()
    session.refresh(new_db_album)
    return new_db_album

@router.put("/{album_id}", response_model=Album)
def update_album(album_id: int, album_update: AlbumCreate, session: Session=Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    album_data = album_update.model_dump() 
    for key, value in album_data.items():
        setattr(db_album, key, value)
    session.add(db_album)
    session.commit()
    session.refresh(db_album)
    return db_album


    

@router.patch("/{album_id}", response_model=Album)
def partial_update_album(album_id: int, album_update: AlbumUpdate, session: Session=Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    album_data = album_update.model_dump(exclude_unset=True) 
    for key, value in album_data.items():
        setattr(db_album, key, value)
    session.add(db_album)
    session.commit()
    session.refresh(db_album)
    return db_album

@router.delete("/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    session.delete(db_album)
    session.commit()
    return None



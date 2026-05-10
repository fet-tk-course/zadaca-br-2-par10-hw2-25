from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from models_a import Album, AlbumCreate, AlbumUpdate, AlbumFilter
from database import get_session


router = APIRouter(prefix="/resursi_a", tags=["Resurs A"])
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

@router.get("/{album_id}", response_model=Album)
def read_album(album_id: int, session: Session = Depends(get_session)):
    db_album = session.get(Album, album_id)
    if not db_album:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Album nije pronađen")
    return db_album 

@router.post("/", response_model=Album, status_code=status.HTTP_201_CREATED)
def create_album(album: AlbumCreate, session: Session = Depends(get_session)):
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
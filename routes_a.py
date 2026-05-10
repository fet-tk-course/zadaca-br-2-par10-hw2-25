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

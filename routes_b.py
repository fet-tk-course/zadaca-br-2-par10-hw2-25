from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from models_b import Song, SongCreate, SongUpdate
from typing import List, Optional

from database import get_session

router = APIRouter(prefix="/songs", tags=["Resurs B"])

@router.get("/", response_model=List[Song])
def read_songs(genre: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(Song)
    if genre:
        query = query.where(Song.genre == genre)
    songs = session.exec(query).all()
    return songs

@router.get("/{song_id}", response_model=Song)
def read_song(song_id: int, session: Session = Depends(get_session)):
    db_song = session.get(Song, song_id)
    if not db_song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pjesma nije pronađena")
    return db_song

@router.post("/", response_model=Song, status_code=status.HTTP_201_CREATED)
def create_song(song: SongCreate, session: Session = Depends(get_session)):
    new_db_song = Song.model_validate(song)
    session.add(new_db_song)
    session.commit()
    session.refresh(new_db_song)
    return new_db_song

@router.put("/{song_id}", response_model=Song)
def update_song(song_id: int, song_input: SongCreate, session: Session = Depends(get_session)):
    db_song = session.get(Song, song_id)
    if not db_song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pjesma nije pronađena")
    song_data = song_input.model_dump()
    for key, value in song_data.items():
        setattr(db_song, key, value)
    session.add(db_song)
    session.commit()
    session.refresh(db_song)
    return db_song

@router.patch("/{song_id}", response_model=Song)
def partial_update_song(song_id: int, song_update: SongUpdate, session: Session = Depends(get_session)):
    db_song = session.get(Song, song_id)
    if not db_song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pjesma nije pronađena")
    #Dumpujem podatke iz song_update objekta, ali samo one koje su postavljene (exclude_unset=True)
    song_data = song_update.model_dump(exclude_unset=True)
    for key, value in song_data.items():
        setattr(db_song, key, value)

    session.add(db_song)
    session.commit()
    session.refresh(db_song)
    return db_song

@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_song(song_id: int, session: Session = Depends(get_session)):
    db_song = session.get(Song, song_id)
    if not db_song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pjesma nije pronađena")
    session.delete(db_song)
    session.commit()
    return None
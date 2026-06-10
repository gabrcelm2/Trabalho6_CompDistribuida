from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, User, Song, Playlist
from pydantic import BaseModel
from typing import Optional

rest_router = APIRouter()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ========== Schemas Pydantic ==========
class UserCreate(BaseModel):
    nome: str
    idade: int

class SongCreate(BaseModel):
    nome: str
    artista: str

class PlaylistCreate(BaseModel):
    nome: str
    usuario_id: int

# ========== USUARIOS CRUD ==========

@rest_router.get("/usuarios")
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "nome": u.nome, "idade": u.idade} for u in users]

@rest_router.get("/usuarios/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if u:
        return {"id": u.id, "nome": u.nome, "idade": u.idade}
    return {"error": "Usuário não encontrado"}

@rest_router.post("/usuarios")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    u = User(nome=user.nome, idade=user.idade)
    db.add(u)
    db.commit()
    db.refresh(u)
    return {"id": u.id, "nome": u.nome, "idade": u.idade}

@rest_router.put("/usuarios/{user_id}")
async def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if u:
        u.nome = user.nome
        u.idade = user.idade
        db.commit()
        return {"id": u.id, "nome": u.nome, "idade": u.idade}
    return {"error": "Usuário não encontrado"}

@rest_router.delete("/usuarios/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.query(User).filter(User.id == user_id).first()
    if u:
        db.delete(u)
        db.commit()
        return {"message": "Usuário removido"}
    return {"error": "Usuário não encontrado"}

# ========== MUSICAS CRUD ==========

@rest_router.get("/musicas")
async def get_songs(db: Session = Depends(get_db)):
    songs = db.query(Song).all()
    return [{"id": s.id, "nome": s.nome, "artista": s.artista} for s in songs]

@rest_router.get("/musicas/{song_id}")
async def get_song(song_id: int, db: Session = Depends(get_db)):
    s = db.query(Song).filter(Song.id == song_id).first()
    if s:
        return {"id": s.id, "nome": s.nome, "artista": s.artista}
    return {"error": "Música não encontrada"}

@rest_router.post("/musicas")
async def create_song(song: SongCreate, db: Session = Depends(get_db)):
    s = Song(nome=song.nome, artista=song.artista)
    db.add(s)
    db.commit()
    db.refresh(s)
    return {"id": s.id, "nome": s.nome, "artista": s.artista}

@rest_router.put("/musicas/{song_id}")
async def update_song(song_id: int, song: SongCreate, db: Session = Depends(get_db)):
    s = db.query(Song).filter(Song.id == song_id).first()
    if s:
        s.nome = song.nome
        s.artista = song.artista
        db.commit()
        return {"id": s.id, "nome": s.nome, "artista": s.artista}
    return {"error": "Música não encontrada"}

@rest_router.delete("/musicas/{song_id}")
async def delete_song(song_id: int, db: Session = Depends(get_db)):
    s = db.query(Song).filter(Song.id == song_id).first()
    if s:
        db.delete(s)
        db.commit()
        return {"message": "Música removida"}
    return {"error": "Música não encontrada"}

# ========== PLAYLISTS CRUD ==========

@rest_router.get("/playlists")
async def get_playlists(db: Session = Depends(get_db)):
    playlists = db.query(Playlist).all()
    return [{"id": p.id, "nome": p.nome, "usuario_id": p.usuario_id} for p in playlists]

@rest_router.get("/playlists/{playlist_id}")
async def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    p = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if p:
        return {"id": p.id, "nome": p.nome, "usuario_id": p.usuario_id}
    return {"error": "Playlist não encontrada"}

@rest_router.post("/playlists")
async def create_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    p = Playlist(nome=playlist.nome, usuario_id=playlist.usuario_id)
    db.add(p)
    db.commit()
    db.refresh(p)
    return {"id": p.id, "nome": p.nome, "usuario_id": p.usuario_id}

@rest_router.put("/playlists/{playlist_id}")
async def update_playlist(playlist_id: int, playlist: PlaylistCreate, db: Session = Depends(get_db)):
    p = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if p:
        p.nome = playlist.nome
        p.usuario_id = playlist.usuario_id
        db.commit()
        return {"id": p.id, "nome": p.nome, "usuario_id": p.usuario_id}
    return {"error": "Playlist não encontrada"}

@rest_router.delete("/playlists/{playlist_id}")
async def delete_playlist(playlist_id: int, db: Session = Depends(get_db)):
    p = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if p:
        db.delete(p)
        db.commit()
        return {"message": "Playlist removida"}
    return {"error": "Playlist não encontrada"}

# ========== CONSULTAS ESPECIAIS ==========

@rest_router.get("/usuarios/{user_id}/playlists")
async def get_playlists_by_user(user_id: int, db: Session = Depends(get_db)):
    playlists = db.query(Playlist).filter(Playlist.usuario_id == user_id).all()
    return [{"id": p.id, "nome": p.nome, "usuario_id": p.usuario_id} for p in playlists]

@rest_router.get("/playlists/{playlist_id}/musicas")
async def get_songs_by_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if playlist:
        return [{"id": s.id, "nome": s.nome, "artista": s.artista} for s in playlist.songs]
    return []

@rest_router.get("/musicas/{song_id}/playlists")
async def get_playlists_by_song(song_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_id).first()
    if song:
        return [{"id": p.id, "nome": p.nome, "usuario_id": p.usuario_id} for p in song.playlists]
    return []

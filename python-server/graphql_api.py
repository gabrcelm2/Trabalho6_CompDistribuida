import strawberry
from typing import List, Optional
from database import SessionLocal, User as DBUser, Song as DBSong, Playlist as DBPlaylist

@strawberry.type
class SongType:
    id: int
    nome: str
    artista: str

@strawberry.type
class PlaylistType:
    id: int
    nome: str
    usuario_id: int
    songs: Optional[List[SongType]] = None

@strawberry.type
class UserType:
    id: int
    nome: str
    idade: int
    playlists: Optional[List[PlaylistType]] = None

@strawberry.type
class Query:
    @strawberry.field
    def all_users(self) -> List[UserType]:
        db = SessionLocal()
        users = db.query(DBUser).all()
        result = [UserType(id=u.id, nome=u.nome, idade=u.idade) for u in users]
        db.close()
        return result

    @strawberry.field
    def all_songs(self) -> List[SongType]:
        db = SessionLocal()
        songs = db.query(DBSong).all()
        result = [SongType(id=s.id, nome=s.nome, artista=s.artista) for s in songs]
        db.close()
        return result

    @strawberry.field
    def playlists_by_user(self, user_id: int) -> List[PlaylistType]:
        db = SessionLocal()
        playlists = db.query(DBPlaylist).filter(DBPlaylist.usuario_id == user_id).all()
        result = [PlaylistType(id=p.id, nome=p.nome, usuario_id=p.usuario_id, songs=[
            SongType(id=s.id, nome=s.nome, artista=s.artista) for s in p.songs
        ]) for p in playlists]
        db.close()
        return result

    @strawberry.field
    def songs_by_playlist(self, playlist_id: int) -> List[SongType]:
        db = SessionLocal()
        playlist = db.query(DBPlaylist).filter(DBPlaylist.id == playlist_id).first()
        result = []
        if playlist:
            result = [SongType(id=s.id, nome=s.nome, artista=s.artista) for s in playlist.songs]
        db.close()
        return result

    @strawberry.field
    def playlists_by_song(self, song_id: int) -> List[PlaylistType]:
        db = SessionLocal()
        song = db.query(DBSong).filter(DBSong.id == song_id).first()
        result = []
        if song:
            result = [PlaylistType(id=p.id, nome=p.nome, usuario_id=p.usuario_id, songs=[
                SongType(id=s.id, nome=s.nome, artista=s.artista) for s in p.songs
            ]) for p in song.playlists]
        db.close()
        return result

schema = strawberry.Schema(query=Query)

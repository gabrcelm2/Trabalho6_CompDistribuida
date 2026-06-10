from concurrent import futures
import grpc
import streaming_pb2
import streaming_pb2_grpc
from database import SessionLocal, User as DBUser, Song as DBSong, Playlist as DBPlaylist

class StreamingServiceServicer(streaming_pb2_grpc.StreamingServiceServicer):
    def ListUsers(self, request, context):
        db = SessionLocal()
        users = db.query(DBUser).all()
        response = streaming_pb2.UserList()
        for u in users:
            response.users.add(id=u.id, nome=u.nome, idade=u.idade)
        db.close()
        return response

    def ListSongs(self, request, context):
        db = SessionLocal()
        songs = db.query(DBSong).all()
        response = streaming_pb2.SongList()
        for s in songs:
            response.songs.add(id=s.id, nome=s.nome, artista=s.artista)
        db.close()
        return response

    def ListPlaylistsByUser(self, request, context):
        db = SessionLocal()
        playlists = db.query(DBPlaylist).filter(DBPlaylist.usuario_id == request.id).all()
        response = streaming_pb2.PlaylistList()
        for p in playlists:
            pb = response.playlists.add(id=p.id, nome=p.nome, usuario_id=p.usuario_id)
            for s in p.songs:
                pb.songs.add(id=s.id, nome=s.nome, artista=s.artista)
        db.close()
        return response

    def ListSongsByPlaylist(self, request, context):
        db = SessionLocal()
        playlist = db.query(DBPlaylist).filter(DBPlaylist.id == request.id).first()
        response = streaming_pb2.SongList()
        if playlist:
            for s in playlist.songs:
                response.songs.add(id=s.id, nome=s.nome, artista=s.artista)
        db.close()
        return response

    def ListPlaylistsBySong(self, request, context):
        db = SessionLocal()
        song = db.query(DBSong).filter(DBSong.id == request.id).first()
        response = streaming_pb2.PlaylistList()
        if song:
            for p in song.playlists:
                pb = response.playlists.add(id=p.id, nome=p.nome, usuario_id=p.usuario_id)
                for s in p.songs:
                    pb.songs.add(id=s.id, nome=s.nome, artista=s.artista)
        db.close()
        return response

def serve_grpc():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    streaming_pb2_grpc.add_StreamingServiceServicer_to_server(StreamingServiceServicer(), server)
    server.add_insecure_port('[::]:9091')
    server.start()
    print("gRPC Server started on port 9091")
    server.wait_for_termination()

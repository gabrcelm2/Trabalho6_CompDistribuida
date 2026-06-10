import sys
import collections.abc
import http.cookies
import urllib.parse
import urllib
import operator
import six

six.get_method_function = operator.attrgetter("__func__")
six.get_method_self = operator.attrgetter("__self__")
six.get_function_closure = operator.attrgetter("__closure__")
six.get_function_code = operator.attrgetter("__code__")
six.get_function_defaults = operator.attrgetter("__defaults__")
six.get_function_globals = operator.attrgetter("__globals__")
six.get_function_name = operator.attrgetter("__name__")
six.iterlists = lambda d, **kw: iter(d.lists(**kw))

six.moves.collections_abc = collections.abc
sys.modules['spyne.util.six'] = six
sys.modules['spyne.util.six.moves'] = six.moves
sys.modules['spyne.util.six.moves.collections_abc'] = collections.abc
sys.modules['spyne.util.six.moves.http_cookies'] = http.cookies
sys.modules['spyne.util.six.moves.urllib'] = urllib
sys.modules['spyne.util.six.moves.urllib.parse'] = urllib.parse

from spyne import Application, rpc, ServiceBase, Integer, Unicode, Iterable, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from database import SessionLocal, User as DBUser, Song as DBSong, Playlist as DBPlaylist

class SongSoap(ComplexModel):
    id = Integer
    nome = Unicode
    artista = Unicode

class PlaylistSoap(ComplexModel):
    id = Integer
    nome = Unicode
    usuario_id = Integer
    songs = Array(SongSoap)

class UserSoap(ComplexModel):
    id = Integer
    nome = Unicode
    idade = Integer

class StreamingSoapService(ServiceBase):
    @rpc(_returns=Array(UserSoap), _operation_name="GetUsersRequest")
    def get_users(ctx):
        db = SessionLocal()
        users = db.query(DBUser).all()
        result = [UserSoap(id=u.id, nome=u.nome, idade=u.idade) for u in users]
        db.close()
        return result

    @rpc(_returns=Array(SongSoap), _operation_name="GetSongsRequest")
    def get_songs(ctx):
        db = SessionLocal()
        songs = db.query(DBSong).all()
        result = [SongSoap(id=s.id, nome=s.nome, artista=s.artista) for s in songs]
        db.close()
        return result

    @rpc(Integer, _returns=Array(PlaylistSoap), _operation_name="GetPlaylistsByUserRequest")
    def get_playlists_by_user(ctx, userId):
        db = SessionLocal()
        playlists = db.query(DBPlaylist).filter(DBPlaylist.usuario_id == userId).all()
        result = []
        for p in playlists:
            songs = [SongSoap(id=s.id, nome=s.nome, artista=s.artista) for s in p.songs]
            result.append(PlaylistSoap(id=p.id, nome=p.nome, usuario_id=p.usuario_id, songs=songs))
        db.close()
        return result

    @rpc(Integer, _returns=Array(SongSoap), _operation_name="GetSongsByPlaylistRequest")
    def get_songs_by_playlist(ctx, playlistId):
        db = SessionLocal()
        playlist = db.query(DBPlaylist).filter(DBPlaylist.id == playlistId).first()
        result = []
        if playlist:
            result = [SongSoap(id=s.id, nome=s.nome, artista=s.artista) for s in playlist.songs]
        db.close()
        return result

    @rpc(Integer, _returns=Array(PlaylistSoap), _operation_name="GetPlaylistsBySongRequest")
    def get_playlists_by_song(ctx, songId):
        db = SessionLocal()
        song = db.query(DBSong).filter(DBSong.id == songId).first()
        result = []
        if song:
            for p in song.playlists:
                songs = [SongSoap(id=s.id, nome=s.nome, artista=s.artista) for s in p.songs]
                result.append(PlaylistSoap(id=p.id, nome=p.nome, usuario_id=p.usuario_id, songs=songs))
        db.close()
        return result

soap_app = Application([StreamingSoapService], 'http://streaming.unifor.br/soap',
                       in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())

soap_wsgi_app = WsgiApplication(soap_app)

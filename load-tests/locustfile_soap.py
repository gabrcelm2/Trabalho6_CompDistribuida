import random
from locust import HttpUser, task, between

class SoapUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def do_soap(self, content, name):
        body = f"""<?xml version="1.0" encoding="utf-8"?>
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://streaming.unifor.br/soap">
    <soap11env:Body>
        {content}
    </soap11env:Body>
</soap11env:Envelope>"""
        self.client.post("/ws", data=body, headers={"Content-Type": "text/xml"}, name=name)

    @task
    def list_usuarios(self):
        self.do_soap("<tns:GetUsersRequest/>", "SOAP_GetUsers")

    @task
    def list_musicas(self):
        self.do_soap("<tns:GetSongsRequest/>", "SOAP_GetSongs")

    @task
    def playlists_by_user(self):
        uid = random.randint(1, 1000)
        tag = f'<tns:GetPlaylistsByUserRequest><tns:userId>{uid}</tns:userId></tns:GetPlaylistsByUserRequest>'
        self.do_soap(tag, "SOAP_GetPlaylistsByUser")

    @task
    def musicas_by_playlist(self):
        pid = random.randint(1, 200)
        tag = f'<tns:GetSongsByPlaylistRequest><tns:playlistId>{pid}</tns:playlistId></tns:GetSongsByPlaylistRequest>'
        self.do_soap(tag, "SOAP_GetSongsByPlaylist")

    @task
    def playlists_by_song(self):
        sid = random.randint(1, 500)
        tag = f'<tns:GetPlaylistsBySongRequest><tns:songId>{sid}</tns:songId></tns:GetPlaylistsBySongRequest>'
        self.do_soap(tag, "SOAP_GetPlaylistsBySong")

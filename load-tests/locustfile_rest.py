import random
from locust import HttpUser, task, between

class RestUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def list_usuarios(self):
        self.client.get("/api/usuarios", name="REST_list_usuarios")

    @task
    def list_musicas(self):
        self.client.get("/api/musicas", name="REST_list_musicas")

    @task
    def playlists_by_user(self):
        uid = random.randint(1, 1000)
        self.client.get(f"/api/usuarios/{uid}/playlists", name="REST_playlists_by_user")

    @task
    def musicas_by_playlist(self):
        pid = random.randint(1, 200)
        self.client.get(f"/api/playlists/{pid}/musicas", name="REST_musicas_by_playlist")

    @task
    def playlists_by_song(self):
        sid = random.randint(1, 500)
        self.client.get(f"/api/musicas/{sid}/playlists", name="REST_playlists_by_song")

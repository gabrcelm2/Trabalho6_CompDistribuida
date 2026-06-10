import random
from locust import HttpUser, task, between

class GraphqlUser(HttpUser):
    wait_time = between(0.1, 0.5)

    def do_query(self, query, name):
        self.client.post("/graphql", json={"query": query}, name=name)

    @task
    def list_usuarios(self):
        q = "{ allUsers { id nome idade } }"
        self.do_query(q, "GraphQL_list_usuarios")

    @task
    def list_musicas(self):
        q = "{ allSongs { id nome artista } }"
        self.do_query(q, "GraphQL_list_musicas")

    @task
    def playlists_by_user(self):
        uid = random.randint(1, 1000)
        q = f'{{ playlistsByUser(userId: {uid}) {{ id nome }} }}'
        self.do_query(q, "GraphQL_playlists_by_user")

    @task
    def musicas_by_playlist(self):
        pid = random.randint(1, 200)
        q = f'{{ songsByPlaylist(playlistId: {pid}) {{ id nome }} }}'
        self.do_query(q, "GraphQL_musicas_by_playlist")

    @task
    def playlists_by_song(self):
        sid = random.randint(1, 500)
        q = f'{{ playlistsBySong(songId: {sid}) {{ id nome }} }}'
        self.do_query(q, "GraphQL_playlists_by_song")

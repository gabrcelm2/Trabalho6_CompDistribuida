import random
import time
import grpc
from locust import User, task, between
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../python-server'))
import streaming_pb2
import streaming_pb2_grpc

class GrpcClient:
    def __init__(self, host):
        # host format from Locust will be http://domain:port, we need domain:port for grpc
        grpc_host = host.replace("http://", "").replace("https://", "")
        # Use port 50051 for grpc in python, or 9090 for java
        # But run_all_tests replaces this depending on what's running.
        self.channel = grpc.insecure_channel(grpc_host)
        self.stub = streaming_pb2_grpc.StreamingServiceStub(self.channel)
        
class GrpcUser(User):
    wait_time = between(0.1, 0.5)

    def on_start(self):
        self.grpc_client = GrpcClient(self.host)

    def do_rpc(self, method_name, request_obj, name):
        start = time.time()
        try:
            method = getattr(self.grpc_client.stub, method_name)
            method(request_obj)
            elapsed = int((time.time() - start) * 1000)
            self.environment.events.request.fire(
                request_type="gRPC", name=name, response_time=elapsed, response_length=0, exception=None
            )
        except Exception as e:
            elapsed = int((time.time() - start) * 1000)
            self.environment.events.request.fire(
                request_type="gRPC", name=name, response_time=elapsed, response_length=0, exception=e
            )

    @task
    def list_usuarios(self):
        self.do_rpc("ListUsers", streaming_pb2.Empty(), "gRPC_ListUsers")

    @task
    def list_musicas(self):
        self.do_rpc("ListSongs", streaming_pb2.Empty(), "gRPC_ListSongs")

    @task
    def playlists_by_user(self):
        uid = random.randint(1, 1000)
        self.do_rpc("ListPlaylistsByUser", streaming_pb2.IdRequest(id=uid), "gRPC_PlaylistsByUser")

    @task
    def musicas_by_playlist(self):
        pid = random.randint(1, 200)
        self.do_rpc("ListSongsByPlaylist", streaming_pb2.IdRequest(id=pid), "gRPC_SongsByPlaylist")

    @task
    def playlists_by_song(self):
        sid = random.randint(1, 500)
        self.do_rpc("ListPlaylistsBySong", streaming_pb2.IdRequest(id=sid), "gRPC_PlaylistsBySong")

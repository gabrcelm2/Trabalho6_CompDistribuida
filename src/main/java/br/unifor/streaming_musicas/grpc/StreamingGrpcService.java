package br.unifor.streaming_musicas.grpc;

import br.unifor.streaming_musicas.model.Playlist;
import br.unifor.streaming_musicas.model.Song;
import br.unifor.streaming_musicas.model.User;
import br.unifor.streaming_musicas.repository.PlaylistRepository;
import br.unifor.streaming_musicas.repository.SongRepository;
import br.unifor.streaming_musicas.repository.UserRepository;
import io.grpc.stub.StreamObserver;
import org.springframework.stereotype.Service;
import br.unifor.streaming_musicas.grpc.StreamingServiceGrpc.StreamingServiceImplBase;

@Service
public class StreamingGrpcService extends StreamingServiceImplBase {

    private final UserRepository userRepository;
    private final SongRepository songRepository;
    private final PlaylistRepository playlistRepository;

    public StreamingGrpcService(UserRepository userRepository, SongRepository songRepository, PlaylistRepository playlistRepository) {
        this.userRepository = userRepository;
        this.songRepository = songRepository;
        this.playlistRepository = playlistRepository;
    }

    @Override
    public void listUsers(Empty request, StreamObserver<UserList> responseObserver) {
        UserList.Builder builder = UserList.newBuilder();
        for (User u : userRepository.findAll()) {
            builder.addUsers(br.unifor.streaming_musicas.grpc.User.newBuilder()
                    .setId(u.getId())
                    .setNome(u.getNome())
                    .setIdade(u.getIdade())
                    .build());
        }
        responseObserver.onNext(builder.build());
        responseObserver.onCompleted();
    }

    @Override
    public void listSongs(Empty request, StreamObserver<SongList> responseObserver) {
        SongList.Builder builder = SongList.newBuilder();
        for (Song s : songRepository.findAll()) {
            builder.addSongs(br.unifor.streaming_musicas.grpc.Song.newBuilder()
                    .setId(s.getId())
                    .setNome(s.getNome())
                    .setArtista(s.getArtista())
                    .build());
        }
        responseObserver.onNext(builder.build());
        responseObserver.onCompleted();
    }

    @Override
    public void listPlaylistsByUser(IdRequest request, StreamObserver<PlaylistList> responseObserver) {
        PlaylistList.Builder builder = PlaylistList.newBuilder();
        for (Playlist p : playlistRepository.findByUserId(request.getId())) {
            builder.addPlaylists(mapPlaylist(p));
        }
        responseObserver.onNext(builder.build());
        responseObserver.onCompleted();
    }

    @Override
    public void listSongsByPlaylist(IdRequest request, StreamObserver<SongList> responseObserver) {
        SongList.Builder builder = SongList.newBuilder();
        playlistRepository.findById(request.getId()).ifPresent(p -> {
            for (Song s : p.getSongs()) {
                builder.addSongs(br.unifor.streaming_musicas.grpc.Song.newBuilder()
                        .setId(s.getId())
                        .setNome(s.getNome())
                        .setArtista(s.getArtista())
                        .build());
            }
        });
        responseObserver.onNext(builder.build());
        responseObserver.onCompleted();
    }

    @Override
    public void listPlaylistsBySong(IdRequest request, StreamObserver<PlaylistList> responseObserver) {
        PlaylistList.Builder builder = PlaylistList.newBuilder();
        for (Playlist p : playlistRepository.findBySongsId(request.getId())) {
            builder.addPlaylists(mapPlaylist(p));
        }
        responseObserver.onNext(builder.build());
        responseObserver.onCompleted();
    }

    private br.unifor.streaming_musicas.grpc.Playlist mapPlaylist(Playlist p) {
        br.unifor.streaming_musicas.grpc.Playlist.Builder pb = br.unifor.streaming_musicas.grpc.Playlist.newBuilder()
                .setId(p.getId())
                .setNome(p.getNome())
                .setUsuarioId(p.getUser().getId());
        for (Song s : p.getSongs()) {
            pb.addSongs(br.unifor.streaming_musicas.grpc.Song.newBuilder()
                    .setId(s.getId())
                    .setNome(s.getNome())
                    .setArtista(s.getArtista())
                    .build());
        }
        return pb.build();
    }
}

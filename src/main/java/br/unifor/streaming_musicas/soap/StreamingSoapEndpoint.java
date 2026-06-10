package br.unifor.streaming_musicas.soap;

import br.unifor.streaming_musicas.model.Playlist;
import br.unifor.streaming_musicas.model.Song;
import br.unifor.streaming_musicas.model.User;
import br.unifor.streaming_musicas.repository.PlaylistRepository;
import br.unifor.streaming_musicas.repository.SongRepository;
import br.unifor.streaming_musicas.repository.UserRepository;
import org.springframework.ws.server.endpoint.annotation.Endpoint;
import org.springframework.ws.server.endpoint.annotation.PayloadRoot;
import org.springframework.ws.server.endpoint.annotation.RequestPayload;
import org.springframework.ws.server.endpoint.annotation.ResponsePayload;

import br.unifor.streaming.soap.*;

import org.springframework.transaction.annotation.Transactional;

@Endpoint
@Transactional
public class StreamingSoapEndpoint {
    private static final String NAMESPACE_URI = "http://streaming.unifor.br/soap";

    private final UserRepository userRepository;
    private final SongRepository songRepository;
    private final PlaylistRepository playlistRepository;

    public StreamingSoapEndpoint(UserRepository userRepository, SongRepository songRepository, PlaylistRepository playlistRepository) {
        this.userRepository = userRepository;
        this.songRepository = songRepository;
        this.playlistRepository = playlistRepository;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetUsersRequest")
    @ResponsePayload
    public GetUsersResponse getUsers(@RequestPayload GetUsersRequest request) {
        GetUsersResponse response = new GetUsersResponse();
        for (User u : userRepository.findAll()) {
            br.unifor.streaming.soap.UserSoap us = new br.unifor.streaming.soap.UserSoap();
            us.setId(u.getId());
            us.setNome(u.getNome());
            us.setIdade(u.getIdade());
            response.getUsers().add(us);
        }
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetSongsRequest")
    @ResponsePayload
    public GetSongsResponse getSongs(@RequestPayload GetSongsRequest request) {
        GetSongsResponse response = new GetSongsResponse();
        for (Song s : songRepository.findAll()) {
            br.unifor.streaming.soap.SongSoap ss = new br.unifor.streaming.soap.SongSoap();
            ss.setId(s.getId());
            ss.setNome(s.getNome());
            ss.setArtista(s.getArtista());
            response.getSongs().add(ss);
        }
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetPlaylistsByUserRequest")
    @ResponsePayload
    public GetPlaylistsByUserResponse getPlaylistsByUser(@RequestPayload GetPlaylistsByUserRequest request) {
        GetPlaylistsByUserResponse response = new GetPlaylistsByUserResponse();
        for (Playlist p : playlistRepository.findByUserId(request.getUserId())) {
            response.getPlaylists().add(mapPlaylist(p));
        }
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetSongsByPlaylistRequest")
    @ResponsePayload
    public GetSongsByPlaylistResponse getSongsByPlaylist(@RequestPayload GetSongsByPlaylistRequest request) {
        GetSongsByPlaylistResponse response = new GetSongsByPlaylistResponse();
        playlistRepository.findById(request.getPlaylistId()).ifPresent(p -> {
            for (Song s : p.getSongs()) {
                br.unifor.streaming.soap.SongSoap ss = new br.unifor.streaming.soap.SongSoap();
                ss.setId(s.getId());
                ss.setNome(s.getNome());
                ss.setArtista(s.getArtista());
                response.getSongs().add(ss);
            }
        });
        return response;
    }

    @PayloadRoot(namespace = NAMESPACE_URI, localPart = "GetPlaylistsBySongRequest")
    @ResponsePayload
    public GetPlaylistsBySongResponse getPlaylistsBySong(@RequestPayload GetPlaylistsBySongRequest request) {
        GetPlaylistsBySongResponse response = new GetPlaylistsBySongResponse();
        for (Playlist p : playlistRepository.findBySongsId(request.getSongId())) {
            response.getPlaylists().add(mapPlaylist(p));
        }
        return response;
    }

    private br.unifor.streaming.soap.PlaylistSoap mapPlaylist(Playlist p) {
        br.unifor.streaming.soap.PlaylistSoap ps = new br.unifor.streaming.soap.PlaylistSoap();
        ps.setId(p.getId());
        ps.setNome(p.getNome());
        ps.setUsuarioId(p.getUser().getId());
        for(Song s : p.getSongs()) {
            br.unifor.streaming.soap.SongSoap ss = new br.unifor.streaming.soap.SongSoap();
            ss.setId(s.getId());
            ss.setNome(s.getNome());
            ss.setArtista(s.getArtista());
            ps.getSongs().add(ss);
        }
        return ps;
    }
}

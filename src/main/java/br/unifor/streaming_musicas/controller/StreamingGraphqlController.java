package br.unifor.streaming_musicas.controller;

import br.unifor.streaming_musicas.model.Playlist;
import br.unifor.streaming_musicas.model.Song;
import br.unifor.streaming_musicas.model.User;
import br.unifor.streaming_musicas.repository.PlaylistRepository;
import br.unifor.streaming_musicas.repository.SongRepository;
import br.unifor.streaming_musicas.repository.UserRepository;
import org.springframework.graphql.data.method.annotation.Argument;
import org.springframework.graphql.data.method.annotation.QueryMapping;
import org.springframework.stereotype.Controller;

import java.util.List;

@Controller
public class StreamingGraphqlController {

    private final UserRepository userRepository;
    private final SongRepository songRepository;
    private final PlaylistRepository playlistRepository;

    public StreamingGraphqlController(UserRepository userRepository, SongRepository songRepository, PlaylistRepository playlistRepository) {
        this.userRepository = userRepository;
        this.songRepository = songRepository;
        this.playlistRepository = playlistRepository;
    }

    @QueryMapping
    public List<User> allUsers() {
        return userRepository.findAll();
    }

    @QueryMapping
    public List<Song> allSongs() {
        return songRepository.findAll();
    }

    @QueryMapping
    public List<Playlist> playlistsByUser(@Argument Long userId) {
        return playlistRepository.findByUserId(userId);
    }

    @QueryMapping
    public List<Song> songsByPlaylist(@Argument Long playlistId) {
        return playlistRepository.findById(playlistId)
                .map(Playlist::getSongs)
                .orElse(List.of());
    }

    @QueryMapping
    public List<Playlist> playlistsBySong(@Argument Long songId) {
        return playlistRepository.findBySongsId(songId);
    }
}

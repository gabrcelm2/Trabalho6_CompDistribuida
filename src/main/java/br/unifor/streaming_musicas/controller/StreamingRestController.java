package br.unifor.streaming_musicas.controller;

import br.unifor.streaming_musicas.model.Playlist;
import br.unifor.streaming_musicas.model.Song;
import br.unifor.streaming_musicas.model.User;
import br.unifor.streaming_musicas.repository.PlaylistRepository;
import br.unifor.streaming_musicas.repository.SongRepository;
import br.unifor.streaming_musicas.repository.UserRepository;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api")
public class StreamingRestController {

    private final UserRepository userRepository;
    private final SongRepository songRepository;
    private final PlaylistRepository playlistRepository;

    public StreamingRestController(UserRepository userRepository, SongRepository songRepository, PlaylistRepository playlistRepository) {
        this.userRepository = userRepository;
        this.songRepository = songRepository;
        this.playlistRepository = playlistRepository;
    }

    // ===================== USUÁRIOS - CRUD =====================

    @GetMapping("/usuarios")
    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    @GetMapping("/usuarios/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/usuarios")
    public User createUser(@RequestBody User user) {
        return userRepository.save(user);
    }

    @PutMapping("/usuarios/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody User userData) {
        return userRepository.findById(id).map(user -> {
            user.setNome(userData.getNome());
            user.setIdade(userData.getIdade());
            return ResponseEntity.ok(userRepository.save(user));
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/usuarios/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        if (userRepository.existsById(id)) {
            userRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // ===================== MÚSICAS - CRUD =====================

    @GetMapping("/musicas")
    public List<Song> getAllSongs() {
        return songRepository.findAll();
    }

    @GetMapping("/musicas/{id}")
    public ResponseEntity<Song> getSongById(@PathVariable Long id) {
        return songRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/musicas")
    public Song createSong(@RequestBody Song song) {
        return songRepository.save(song);
    }

    @PutMapping("/musicas/{id}")
    public ResponseEntity<Song> updateSong(@PathVariable Long id, @RequestBody Song songData) {
        return songRepository.findById(id).map(song -> {
            song.setNome(songData.getNome());
            song.setArtista(songData.getArtista());
            return ResponseEntity.ok(songRepository.save(song));
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/musicas/{id}")
    public ResponseEntity<Void> deleteSong(@PathVariable Long id) {
        if (songRepository.existsById(id)) {
            songRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // ===================== PLAYLISTS - CRUD =====================

    @GetMapping("/playlists")
    public List<Playlist> getAllPlaylists() {
        return playlistRepository.findAll();
    }

    @GetMapping("/playlists/{id}")
    public ResponseEntity<Playlist> getPlaylistById(@PathVariable Long id) {
        return playlistRepository.findById(id)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @PostMapping("/playlists")
    public Playlist createPlaylist(@RequestBody Playlist playlist) {
        return playlistRepository.save(playlist);
    }

    @PutMapping("/playlists/{id}")
    public ResponseEntity<Playlist> updatePlaylist(@PathVariable Long id, @RequestBody Playlist playlistData) {
        return playlistRepository.findById(id).map(playlist -> {
            playlist.setNome(playlistData.getNome());
            if (playlistData.getUser() != null) {
                playlist.setUser(playlistData.getUser());
            }
            if (playlistData.getSongs() != null) {
                playlist.setSongs(playlistData.getSongs());
            }
            return ResponseEntity.ok(playlistRepository.save(playlist));
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/playlists/{id}")
    public ResponseEntity<Void> deletePlaylist(@PathVariable Long id) {
        if (playlistRepository.existsById(id)) {
            playlistRepository.deleteById(id);
            return ResponseEntity.noContent().build();
        }
        return ResponseEntity.notFound().build();
    }

    // ===================== CONSULTAS ESPECIAIS =====================

    // 3. Listar playlists de um usuário
    @GetMapping("/usuarios/{userId}/playlists")
    public List<Playlist> getPlaylistsByUser(@PathVariable Long userId) {
        return playlistRepository.findByUserId(userId);
    }

    // 4. Listar músicas de uma playlist
    @GetMapping("/playlists/{playlistId}/musicas")
    public List<Song> getSongsByPlaylist(@PathVariable Long playlistId) {
        return playlistRepository.findById(playlistId)
                .map(Playlist::getSongs)
                .orElse(List.of());
    }

    // 5. Listar playlists que contêm uma música específica
    @GetMapping("/musicas/{songId}/playlists")
    public List<Playlist> getPlaylistsBySong(@PathVariable Long songId) {
        return playlistRepository.findBySongsId(songId);
    }
}

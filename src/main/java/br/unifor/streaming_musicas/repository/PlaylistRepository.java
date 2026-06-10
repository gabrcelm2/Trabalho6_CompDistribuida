package br.unifor.streaming_musicas.repository;

import br.unifor.streaming_musicas.model.Playlist;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface PlaylistRepository extends JpaRepository<Playlist, Long> {
    List<Playlist> findByUserId(Long userId);

    @Query("SELECT DISTINCT p FROM Playlist p JOIN p.songs s WHERE s.id = :songId")
    List<Playlist> findBySongsId(@Param("songId") Long songId);
}

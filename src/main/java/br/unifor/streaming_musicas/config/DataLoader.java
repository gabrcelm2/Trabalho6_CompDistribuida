package br.unifor.streaming_musicas.config;

import br.unifor.streaming_musicas.model.Playlist;
import br.unifor.streaming_musicas.model.Song;
import br.unifor.streaming_musicas.model.User;
import br.unifor.streaming_musicas.repository.PlaylistRepository;
import br.unifor.streaming_musicas.repository.SongRepository;
import br.unifor.streaming_musicas.repository.UserRepository;
import com.github.javafaker.Faker;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.*;

@Configuration
public class DataLoader {

    @Bean
    CommandLineRunner initDatabase(UserRepository userRepository, SongRepository songRepository, PlaylistRepository playlistRepository) {
        return args -> {
            if (userRepository.count() > 0) return;

            Faker faker = new Faker(new Locale("pt-BR"));
            Random random = new Random();

            // 1. Criar 1000 usuários
            System.out.println("Populando banco com 1000 usuários...");
            List<User> users = new ArrayList<>();
            for (int i = 0; i < 1000; i++) {
                User u = new User(faker.name().fullName(), 15 + random.nextInt(56));
                users.add(u);
            }
            userRepository.saveAll(users);
            System.out.println("1000 usuários criados.");

            // 2. Criar 500 músicas
            System.out.println("Populando banco com 500 músicas...");
            List<Song> songs = new ArrayList<>();
            for (int i = 0; i < 500; i++) {
                Song s = new Song(
                    faker.book().title(),       // nome da música (simulado)
                    faker.artist().name()        // artista
                );
                songs.add(s);
            }
            songRepository.saveAll(songs);
            System.out.println("500 músicas criadas.");

            // 3. Criar 200 playlists (cada uma pertence a um usuário aleatório e tem 3-10 músicas aleatórias)
            System.out.println("Populando banco com 200 playlists...");
            List<Playlist> playlists = new ArrayList<>();
            for (int i = 0; i < 200; i++) {
                User owner = users.get(random.nextInt(users.size()));
                Playlist p = new Playlist(faker.music().genre() + " Mix #" + (i + 1), owner);

                // Adicionar de 3 a 10 músicas aleatórias
                int numSongs = 3 + random.nextInt(8);
                Set<Integer> chosen = new HashSet<>();
                for (int j = 0; j < numSongs; j++) {
                    int idx = random.nextInt(songs.size());
                    if (chosen.add(idx)) {
                        p.getSongs().add(songs.get(idx));
                    }
                }
                playlists.add(p);
            }
            playlistRepository.saveAll(playlists);
            System.out.println("200 playlists criadas. Banco populado com sucesso!");
        };
    }
}

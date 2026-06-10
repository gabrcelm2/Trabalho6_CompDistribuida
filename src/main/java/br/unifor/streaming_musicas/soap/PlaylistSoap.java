package br.unifor.streaming_musicas.soap;

import javax.xml.bind.annotation.*;
import java.util.ArrayList;
import java.util.List;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "PlaylistSoap")
public class PlaylistSoap {
    private long id;
    private String nome;
    private long usuarioId;

    @XmlElement(name = "songs")
    private List<SongSoap> songs = new ArrayList<>();

    public long getId() { return id; }
    public void setId(long id) { this.id = id; }
    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }
    public long getUsuarioId() { return usuarioId; }
    public void setUsuarioId(long usuarioId) { this.usuarioId = usuarioId; }
    public List<SongSoap> getSongs() { return songs; }
    public void setSongs(List<SongSoap> songs) { this.songs = songs; }
}

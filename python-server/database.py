from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from faker import Faker
import random

Base = declarative_base()

playlist_musica = Table('playlist_musicas', Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.id')),
    Column('musica_id', Integer, ForeignKey('musicas.id'))
)

class User(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    idade = Column(Integer)
    playlists = relationship("Playlist", back_populates="user")

class Song(Base):
    __tablename__ = 'musicas'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    artista = Column(String)
    playlists = relationship("Playlist", secondary=playlist_musica, back_populates="songs")

class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    user = relationship("User", back_populates="playlists")
    songs = relationship("Song", secondary=playlist_musica, back_populates="playlists")

from sqlalchemy.pool import QueuePool

engine = create_engine(
    'sqlite:///file:memdb1?mode=memory&cache=shared', 
    connect_args={'check_same_thread': False, 'uri': True},
    poolclass=QueuePool,
    pool_size=100,
    max_overflow=900
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if db.query(User).count() == 0:
        fake = Faker('pt_BR')

        # 1000 usuários
        print("Populando banco com 1000 usuários...")
        users = []
        for _ in range(1000):
            u = User(nome=fake.name(), idade=random.randint(15, 70))
            users.append(u)
        db.add_all(users)
        db.flush()

        # 500 músicas
        print("Populando banco com 500 músicas...")
        songs = []
        for _ in range(500):
            s = Song(nome=fake.sentence(nb_words=3).rstrip('.'), artista=fake.name())
            songs.append(s)
        db.add_all(songs)
        db.flush()

        # 200 playlists
        print("Populando banco com 200 playlists...")
        genres = ['Pop', 'Rock', 'MPB', 'Sertanejo', 'Funk', 'Jazz', 'Eletronica', 'Hip Hop', 'Samba', 'Pagode']
        for i in range(200):
            owner = random.choice(users)
            p = Playlist(
                nome=f"{random.choice(genres)} Mix #{i+1}",
                user=owner,
                songs=random.sample(songs, random.randint(3, 10))
            )
            db.add(p)
        db.commit()
        print("Banco populado com sucesso!")
    db.close()

from typing import List,Optional
from sqlalchemy import ForeignKey,String,create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "player"
    id_player: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    role: Mapped[str]
    alive: Mapped[bool]
    ip: Mapped[str]
    hauteur: Mapped[int]
    largeur: Mapped[int]
    game: Mapped["Game"] = relationship(back_populates="players")
    game_id: Mapped[int] = mapped_column(ForeignKey("game.id"))

class Game(Base):
    __tablename__ = "game"
    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    max_player: Mapped[int]
    nb_tours: Mapped[int]
    hauteur: Mapped[int]
    largeur: Mapped[int]
    temps_par_tour: Mapped[int]
    statut: Mapped[bool]
    players: Mapped[List["Player"]] = relationship(
        back_populates="game", cascade="all, delete-orphan"
    )

engine = create_engine("sqlite:///test.db", echo=True)
Base.metadata.create_all(engine)
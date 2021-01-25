from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

import enum

Base = declarative_base()


class CardType(enum.Enum):
    creature = "Creature"
    instant = "Instant"
    spell = "Spell"
    land = "Land"
    planeswalker = "Planeswalker"


class CardDefinition(Base):
    __tablename__ = "card_definitions"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    card_type = Column(Enum(CardType), nullable=False)
    power = Column(Integer)
    toughness = Column(Integer)

    text = Column(String, nullable=False)

    mana_cost_red = Column(Integer)
    mana_cost_blue = Column(Integer)
    mana_cost_black = Column(Integer)
    mana_cost_green = Column(Integer)
    mana_cost_white = Column(Integer)
    mana_cost_any = Column(Integer)

    cards = relationship("Card", back_populates="definition")


class Container(Base):
    __tablename__ = "containers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    cards = relationship("Card", back_populates="container")


class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    foil = Column(Boolean, default=False)

    definition_id = Column(ForeignKey("card_definitions.id"), nullable=False)
    definition = relationship("CardDefinition", back_populates="cards")

    container_id = Column(ForeignKey("containers.id"), nullable=False)
    container = relationship("Container", back_populates="cards")
    container_index = Column(String)
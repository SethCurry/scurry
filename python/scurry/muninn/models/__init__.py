from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Genus(Base):
    __tablename__ = "genuses"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    notes = Column(String)

    species = relationship("Species", back_populates="genus")

    def __repr__(self):
        return "<Genus (id='%s' name='%s')>" % (self.id, self.name)


class Species(Base):
    __tablename__ = "species"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    common_name = Column(String)
    notes = Column(String)

    genus_id = Column(ForeignKey("genuses.id"), nullable=False)
    genus = relationship("Genus", back_populates="species")

    min_temperature = Column(Float, nullable=False)
    max_temperature = Column(Float, nullable=False)

    min_humidity = Column(Float, nullable=False)
    max_humidity = Column(Float, nullable=False)

    day_start = Column(Integer, nullable=False)
    day_end = Column(Integer, nullable=False)

    creatures = relationship("Creature", back_populates="species")

    def __repr__(self):
        return "<Species (id='%s' name='%s')>" % (self.id, self.name)


class Enclosure(Base):
    __tablename__ = "enclosures"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    creatures = relationship("Creature", back_populates="enclosure")


class Creature(Base):
    __tablename__ = "creatures"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    notes = Column(String)
    cost = Column(Float)
    price = Column(Float)
    for_sale = Column(Boolean, default=False)

    species_id = Column(ForeignKey("species.id"))
    species = relationship("Species", back_populates="creatures")

    enclosure_id = Column(ForeignKey("enclosures.id"))
    enclosure = relationship("Enclosure", back_populates="creatures")


class Printer(Base):
    __tablename__ = "printers"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, unique=True, nullable=False)
    api_key = Column(String, nullable=False)

    statuses = relationship("PrinterStatus", back_populates="printer")


class PrinterStatus(Base):
    __tablename__ = "printer_statuses"

    timestamp = Column(DateTime, primary_key=True)

    printer_id = Column(ForeignKey("printers.id"), nullable=False)
    printer = relationship("Printer", back_populates="statuses")

    status = Column(String, primary_key=True)

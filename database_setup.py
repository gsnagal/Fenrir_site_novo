import sys

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String, Float

# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base

# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship

# for configuration
from sqlalchemy import create_engine

# create declarative_base instance
Base = declarative_base()


# We will add classes here
class Fenrir_db(Base):
    __tablename__ = 'Fenrir_db'
    id = Column(Integer, primary_key=True)
    round_uuid = Column(String(250))
    lap = Column(Integer)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    vel = Column(Float)
    datetime = Column(Float)

    @property
    def serialize(self):
        return {
            'round_uuid': self.round_uuid,
            'lap': self.lap,
            'lat': self.lat,
            'lon': self.lon,
            'vel': self.vel,
            'datetime': self.datetime,
        }



# creates a create_engine instance at the bottom of the file
engine = create_engine('sqlite:///fenrir_db.db')
Base.metadata.create_all(engine)
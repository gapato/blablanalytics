from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Trip(Base):
    __tablename__  = 'trips'

    id             = Column(Integer, primary_key=True)
    upstream_id    = Column(String)
    url            = Column(String, unique=True)

    route_id       = Column(Integer, ForeignKey('routes.id'), nullable=False)

    creation_time  = Column(DateTime)
    departure_time = Column(DateTime, nullable=False)
    modif_time     = Column(DateTime)

    fare           = Column(Integer, nullable=False)

    departure      = Column(String, nullable=False)
    ft_departure   = Column(String, nullable=False)

    destination    = Column(String, nullable=False)
    ft_destination = Column(String, nullable=False)

    distance       = Column(Integer)

    seats          = Column(Integer, nullable=False)
    free_seats     = Column(Integer, nullable=False)

    driver_url     = Column(String)

    def __init__(self, fields):
        for (k, v) in fields.items():
            self.__dict__[k] = v

class Route(Base):
    __tablename__  = 'routes'

    id = Column(Integer, primary_key=True)
    url   = Column(String, unique=True, nullable=False)
    name  = Column(String)

    active = Column(Boolean, nullable=False)
    failed = Column(DateTime)

    trips = relationship("Trip", order_by="Trip.departure_time", backref="route")

    def __init__(self, name, url):
        self.name   = name
        self.url    = url
        self.active = True

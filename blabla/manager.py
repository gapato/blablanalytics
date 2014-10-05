import logging
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .parser import get_trip_urls, parse_trip
from .models import Route, Trip, Base

def get_engine(uri):
    engine = create_engine(uri)
    return engine

def get_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def init_database(engine):
    Base.metadata.create_all(engine)

def add_route(session, name, url):
    route = Route(name, url)
    session.add(route)

def delete_route(session, route_id):
    session.query(Route).filter(Route.id == route_id).delete()

def activate_route(session, route_id):
    route = session.query(Route).filter(Trip.id == route_id).first()
    route.active = True

def deactivate_route(session, route_id):
    route = session.query(Route).filter(Trip.id == route_id).first()
    route.active = False

def update_trips(session):
    routes = session.query(Route).filter(Route.active == True)
    for r in routes:
        try:
            trip_urls = get_trip_urls(r.url)
        except e:
            r.active = False
            r.failed = datetime.now()
            logging.error(str(e))
        for url in trip_urls:
            trip = parse_trip(url)
            trip.route_id = r.id
            stored_trip = session.query(Trip).filter(Trip.url == url).first()
            if stored_trip is None:
                session.add(trip)
            else:
                stored_trip.fare       = trip.fare
                stored_trip.free_seats = trip.free_seats
        session.commit()

#!/usr/bin/env python
# coding: utf-8

from __future__ import division

import sys
import logging
from datetime import datetime

# Centos quirk
sys.path.append('/usr/lib64/python2.6/site-packages/SQLAlchemy-0.8.2-py2.6-linux-x86_64.egg')

from blabla.manager import *
from blabla import models

logger = logging.Logger('blabla')
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel(logging.WARNING)

debug    = logger.debug
info     = logger.info
warn     = logger.warning
error    = logger.error
critical = logger.critical

engine = get_engine('sqlite:///blabla.db')

if 'init' in sys.argv[1:]:
    init_database(engine)

session = get_session(engine)

# your default routes
#if 'init' in sys.argv[1:]:
    #add_route(session, u'Foo > Bar', 'http://www.covoiturage.fr/trajets/foo/bar/')
    #session.commit()

if 'delete' in sys.argv[1:]:
    idx = sys.argv.index('delete')
    for i in sys.argv[idx+1:]:
        delete_route(session, int(i))
    session.commit()

if 'update' in sys.argv[1:]:
    update_trips(session)
    session.commit()

if 'list' in sys.argv[1:]:
    for route in session.query(models.Route).all():
        print u'{0: >3}) {1: <30} {2}'.format(route.id, route.name, route.url)

if 'plot' in sys.argv[1:]:

    import matplotlib.pyplot as pyplot

    routes = []
    fares = []
    times = []
    passengers = []

    now = datetime.now()

    for route in session.query(models.Route).all():

        trips = route.trips

        f = map(lambda t:t.fare, trips)
        t = map(lambda t:t.departure_time.hour + t.departure_time.minute/50, trips)
        p = map(lambda t:t.seats-t.free_seats, trips)

        routes.append(route.name)
        fares.append(f)
        times.append(t)
        passengers.append(p)

    pyplot.subplot(131)
    pyplot.hist(fares)
    pyplot.legend(routes)
    pyplot.xlabel("Fare")
    pyplot.subplot(132)
    pyplot.hist(times)
    pyplot.legend(routes)
    pyplot.xlabel("Departure time")
    pyplot.subplot(133)
    pyplot.hist(passengers, bins=[0, 1, 2, 3, 4])
    pyplot.legend(routes)
    pyplot.xlabel("Passengers")
    pyplot.show()

session.close()

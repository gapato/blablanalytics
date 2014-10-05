import urllib2
import bs4
import re
from datetime import datetime

from .models import Trip

VERSION = 1

def get_trip_urls(url):
    resp = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(resp)
    return map(lambda m:m.attrs['content'], soup('meta', itemprop='url'))

def parse_trip(url):
    resp = urllib2.urlopen(url)
    soup = bs4.BeautifulSoup(resp)

    trip_d = {'url':url}

    trip_d['fare'] = int(soup.find("meta", property="blablacar:price")['content'])
    trip_d['departure_time'] = datetime.strptime(soup.find("meta", property="blablacar:date")['content'], "%Y-%m-%dT%H:%MZ")
    trip_d['distance'] = int(soup.find("meta", property="blablacar:distance")['content'])

    # trip id
    trip_d['upstream_id'] = url.split('/')[-1]

    div = soup.find('div', class_='trip-container')

    # trip depature/destination + complete trip
    stops = div.find('span', class_='trip-main-title')('span')
    got_depart = False
    for k, s in enumerate(stops):
        if 'arrow-ie' in s['class'] or k == len(stops)-1: continue
        if k == 0:
            trip_d['ft_departure'] = s.text
        if 'trip-roads-stop' in s['class']:
            if got_depart:
                trip_d['destination'] = s.text
            else:
                trip_d['departure'] = s.text
                got_depart = True
        if k == len(stops) - 2:
            trip_d['ft_destination'] = s.text
            if 'trip-roads-stop' in s['class']:
                trip_d['destination'] = s.text

    # seats
    seat_list = div.find("ul", class_="list-seats-available")
    trip_d['seats'] = len(seat_list("li")) - 1
    trip_d['free_seats'] = len(seat_list("li", class_="empty"))

    # driver
    trip_d['driver_url'] = 'http://www.blablacar.fr' + soup.find('a', rel="nofollow", href=re.compile('^/membre/'))['href']

    return Trip(trip_d)


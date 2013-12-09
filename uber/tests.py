#import from Django
from django.db.models import Sum, Avg
from django.test import TestCase, Client, RequestFactory
#from unittest import TestCase

#import from python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from decimal import *
import json
import urllib
import urllib2

#import from App Uber
from uber.models import TripEvent, UberBase
import views
from uber_util import *

'''
Create test data for unittest
'''
def creat_events():
    record_trip_event(1, 11, 1385895912, Decimal("37.774650"), Decimal("-122.419122"), Decimal("5.0"), Decimal("5.0"), 5) #SF
    record_trip_event(1, 12, 1385895926, Decimal("37.790184"), Decimal("-122.429845"), Decimal("3.0"), Decimal("5.0"), 3) #SF
    record_trip_event(2, 11, 1385895927, Decimal("37.68776"),  Decimal("-122.486598"), Decimal("10.0"), Decimal("6.0"), 4) #Daly City
    record_trip_event(3, 12, 1385895928, Decimal("37.637072"), Decimal("-122.418277"), Decimal("11.0"), Decimal("7.0"), 4) # San Bruno
    record_trip_event(4, 12, 1417850394, Decimal("37.5688"),   Decimal("-122.316336"), Decimal("12.0"), Decimal("8.0"), 5) #future #San Mateo

'''
Send a post request (without CSRF) with a form to the url given
'''
def send_post_addTrip(url, values):
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    return  response.read()

class UberFunctionTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.f = RequestFactory()
        creat_events()

    def test_convertDateStringToUnixTime(TestCase):
        (start_unixtime, end_unixtime) = views.convertDateStringToUnixTime("20131201", "20131202")
        TestCase.assertEqual(start_unixtime, "1385856000")
        TestCase.assertEqual(end_unixtime, "1385942400")

    def test_addTrip(self):
        values = { 'client_id' : 5, 
                   'driver_id' : 12, 
                   'start_time' : 1417850395, 
                   'lat' : Decimal("37.774651"), 
                   'lng' : Decimal("-122.419121"), 
                   'fare' : Decimal("8.0"), 
                   'distance' : Decimal("2.0"), 
                   'rating' : 1 }
        response = self.c.post('/uber/trip/add/', values)
        d = json.loads(response.content)
        self.assertIn('success', d.keys())
        self.assertEqual(d['success'], 'Success')
        self.assertIn('trip', d.keys())
        self.assertIn('fare', d['trip'].keys())
        self.assertIn('distance', d['trip'].keys())
        self.assertIn('rating', d['trip'].keys())
        self.assertIn('start_time', d['trip'].keys())
        self.assertIn('driver_id', d['trip'].keys())
        self.assertIn('client_id', d['trip'].keys())
        self.assertIn('lat', d['trip'].keys())
        self.assertIn('lng', d['trip'].keys())
        self.assertIn('id', d['trip'].keys())
        self.assertEqual(d['trip']['fare'], '8.0')
        self.assertEqual(d['trip']['distance'], '2.0')
        self.assertEqual(d['trip']['rating'], '1')
        self.assertEqual(d['trip']['start_time'], '1417850395')
        self.assertEqual(d['trip']['driver_id'], '12')
        self.assertEqual(d['trip']['client_id'], '5')
        self.assertEqual(d['trip']['lat'], '37.774651')
        self.assertEqual(d['trip']['lng'], '-122.419121')

    def test_addTrip_failed1(self):
        values = { 'client_id' : 5,
                   'driver_id' : 12,
                   'start_time' : 1417850395,
                   'lat' : 13579,
                   'lng' : "STRING",
                   'fare' : Decimal("8.0"),
                   'distance' : Decimal("2.0"),
                   'rating' : 1 }
        response = self.c.post('/uber/trip/add/', values)
        d = json.loads(response.content)
        self.assertIn('error', d.keys())
        
    def test_addTrip_failed2(self):
        values = { 'client_id' : 5,
                   'start_time' : 1417850395,
                   'lat' : 13579,
                   'lng' : "STRING",
                   'fare' : Decimal("8.0"),
                   'distance' : Decimal("2.0"),
                   'rating' : 1 }
        response = self.c.post('/uber/trip/add/', values)
        d = json.loads(response.content)
        self.assertIn('error', d.keys())

    def test_showAllTrip(self):
        response = self.c.get('/uber/trip/')
        d = json.loads(response.content)
        self.assertIn('trip', d.keys())
        self.assertIn('fare', d['trip'][0].keys())
        self.assertIn('distance', d['trip'][0].keys())
        self.assertIn('rating', d['trip'][0].keys())
        self.assertIn('start_time', d['trip'][0].keys())
        self.assertIn('driver_id', d['trip'][0].keys())
        self.assertIn('client_id', d['trip'][0].keys())
        self.assertIn('lat', d['trip'][0].keys())
        self.assertIn('lng', d['trip'][0].keys())
        self.assertIn('id', d['trip'][0].keys())
        self.assertEqual(d['trip'][0]['fare'], float(5.0))
        self.assertEqual(d['trip'][0]['distance'], float(5.0))
        self.assertEqual(d['trip'][0]['rating'], 5)
        self.assertEqual(d['trip'][0]['start_time'], 1385895912)
        self.assertEqual(d['trip'][0]['driver_id'], 11)
        self.assertEqual(d['trip'][0]['client_id'], 1)
        self.assertEqual(d['trip'][0]['lat'], float(37.77465))
        self.assertEqual(d['trip'][0]['lng'], float(-122.419122))
        self.assertEqual(d['trip'][0]['id'], 1)
        self.assertEqual(len(d['trip']), 5)

    def test_showTrip(self):
        response = self.c.get('/uber/trip/1/')
        d = json.loads(response.content)
        self.assertIn('trip', d.keys())
        self.assertIn('fare', d['trip'].keys())
        self.assertIn('distance', d['trip'].keys())
        self.assertIn('rating', d['trip'].keys())
        self.assertIn('start_time', d['trip'].keys())
        self.assertIn('driver_id', d['trip'].keys())
        self.assertIn('client_id', d['trip'].keys())
        self.assertIn('lat', d['trip'].keys())
        self.assertIn('lng', d['trip'].keys())
        self.assertIn('id', d['trip'].keys())
        self.assertEqual(d['trip']['fare'], float(5.0))
        self.assertEqual(d['trip']['distance'], float(5.0))
        self.assertEqual(d['trip']['rating'], 5)
        self.assertEqual(d['trip']['start_time'], 1385895912)
        self.assertEqual(d['trip']['driver_id'], 11)
        self.assertEqual(d['trip']['client_id'], 1)
        self.assertEqual(d['trip']['lat'], float(37.77465))
        self.assertEqual(d['trip']['lng'], float(-122.419122))
        self.assertEqual(d['trip']['id'], 1)

    def test_showTrip_failed(self):
        response = self.c.get('/uber/trip/7/')
        d = json.loads(response.content)
        self.assertIn('error', d.keys())

    def test_view_tripCount(self):
        response = self.c.get('/uber/trip/num/')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_trip'], 5)

    def test_view_tripCount_date(self):
        response = self.c.get('/uber/trip/num/?starttime=20131201&endtime=20131202')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_trip'], 4)
        self.assertEqual(d['starttime'], "1385856000")
        self.assertEqual(d['endtime'], "1385942400")

    def test_view_tripCountLastHour(self):
        response = self.c.get('/uber/trip/num_last_hour/')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_trip'], 0)

    def test_view_clientCount(self):
        response = self.c.get('/uber/client/num/')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_client'], 4)

    def test_view_clientCount_date(self):
        response = self.c.get('/uber/client/num/?starttime=20131201&endtime=20131202')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_client'], 3)
        self.assertEqual(d['starttime'], "1385856000")
        self.assertEqual(d['endtime'], "1385942400")

    def test_view_clientCount_finished(self):
        response = self.c.get('/uber/client/num/?finished=true')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_client'], 3)
        self.assertEqual(d['finished'], True)

    def test_view_clientCount_finished_date(self):
        response = self.c.get('/uber/client/num/?finished=true&starttime=20131201&endtime=20131202')
        d = json.loads(response.content)
        self.assertEqual(d['total_num_client'], 3)
        self.assertEqual(d['starttime'], "1385856000")
        self.assertEqual(d['endtime'], "1385942400")

    def test_view_milesPerClient(self):
        response = self.c.get('/uber/client/1/sum_miles/')
        d = json.loads(response.content)
        self.assertIn('total_miles_per_client', d.keys())
        self.assertEqual(d['total_miles_per_client']['1'], float(10.0))

    def test_view_milesPerClient_date(self):
        response = self.c.get('/uber/client/1/sum_miles/?starttime=20131201&endtime=20131202')
        d = json.loads(response.content)
        self.assertIn('total_miles_per_client', d.keys())
        self.assertEqual(d['total_miles_per_client']['1'], float(10.0))
        self.assertEqual(d['starttime'], "1385856000")
        self.assertEqual(d['endtime'], "1385942400")

    def test_view_avgFareInCity(self):
        response = self.c.get('/uber/city/san_francisco/avg_fare/')
        d = json.loads(response.content)
        self.assertIn('avg_fare_in_city', d.keys())
        self.assertEqual(d['avg_fare_in_city']['fare__avg'], float(4.0))

    def test_view_avgFareInCity_date(self):
        response = self.c.get('/uber/city/san_francisco/avg_fare/?starttime=20131201&endtime=20131202')
        d = json.loads(response.content)
        self.assertIn('avg_fare_in_city', d.keys())
        self.assertEqual(d['avg_fare_in_city']['fare__avg'], float(4.0))
        self.assertEqual(d['starttime'], "1385856000")
        self.assertEqual(d['endtime'], "1385942400")

    def test_view_medianDriverRating(self):
        response = self.c.get('/uber/driver/11/avg_rating/')
        d = json.loads(response.content)
        self.assertIn('avg_rating_per_driver', d.keys())
        self.assertEqual(d['avg_rating_per_driver']['rating__avg'], float(4.5))

    def test_view_medianDriverRating_date(self):
        response = self.c.get('/uber/driver/11/avg_rating/?starttime=20131201&endtime=20131202')
        d = json.loads(response.content)
        self.assertIn('avg_rating_per_driver', d.keys())
        self.assertEqual(d['avg_rating_per_driver']['rating__avg'], float(4.5))
        self.assertEqual(d['starttime'], "1385856000")
        self.assertEqual(d['endtime'], "1385942400")


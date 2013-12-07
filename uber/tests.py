#import from Django
from django.test import TestCase
from django.db.models import Sum, Avg
from django.test import Client
client = Client()
from django.test import TestCase, RequestFactory

#import from python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import time
import datetime
from datetime import timedelta, datetime
import urllib2
#from unittest import TestCase
from decimal import *
import json

#import from App Uber
from uber.models import TripEvent, UberBase
import views

def record_trip_event(client_id, driver_id, start_time, lat, lng, fare, distance, rating):
    return TripEvent.objects.create(client_id=client_id, driver_id=driver_id, start_time=start_time, \
                                    lat=lat, lng=lng, fare=fare, distance=distance, rating=rating)

def creat_events():
    record_trip_event(1, 11, 1385895912, Decimal("37.774650"), Decimal("-122.419122"), Decimal("5.0"), Decimal("5.0"), 5) #SF
    record_trip_event(1, 12, 1385895926, Decimal("37.790184"), Decimal("-122.429845"), Decimal("3.0"), Decimal("5.0"), 3) #SF
    record_trip_event(2, 11, 1385895927, Decimal("37.68776"),  Decimal("-122.486598"), Decimal("10.0"), Decimal("6.0"), 4) #Daly City
    record_trip_event(3, 12, 1385895928, Decimal("37.637072"), Decimal("-122.418277"), Decimal("11.0"), Decimal("7.0"), 4) # San Bruno
    record_trip_event(4, 12, 1417850394, Decimal("37.5688"),   Decimal("-122.316336"), Decimal("12.0"), Decimal("8.0"), 5) #future #San Mateo

class UberFunctionTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.f = RequestFactory()
        creat_events()

    def test_convertDateStringToUnixTime(TestCase):
        (start_unixtime, end_unixtime) = views.convertDateStringToUnixTime("20131201", "20131202")
        TestCase.assertEqual(start_unixtime, "1385856000")
        TestCase.assertEqual(end_unixtime, "1385942400")

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


"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

#import from Django
from django.test import TestCase
from django.db.models import Sum, Avg

#import from python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import time
import datetime
from datetime import timedelta, datetime
import urllib2

#import from App Uber
from uber.models import TripEvent, UberBase
import views

class UberURLTest(TestCase):

    def test_curl(TestCase):
        tests = {
            "num_trip"                 : "http://lans-h.com:8000/uber/trip/num/",
            "num_trip_date"            : "http://lans-h.com:8000/uber/trip/num/?starttime=20131201&endtime=20131202",

            "num_trip_lasthour"        : "http://lans-h.com:8000/uber/trip/num_last_hour/",

            "num_client"               : "http://lans-h.com:8000/uber/client/num/",
            "num_client_date"          : "http://lans-h.com:8000/uber/client/num/?starttime=20131201&endtime=20131202",

            "num_client_finished"      : "http://lans-h.com:8000/uber/client/num/?finished=true",
            "num_client_finished_date" : "http://lans-h.com:8000/uber/client/num/?finished=true&starttime=20131201&endtime=20131202",

            "sum_miles_cid1" : "http://lans-h.com:8000/uber/client/1/sum_miles/",
            "sum_miles_cid2" : "http://lans-h.com:8000/uber/client/2/sum_miles/",
            "sum_miles_cid3" : "http://lans-h.com:8000/uber/client/3/sum_miles/",
            "sum_miles_cid_date1" : "http://lans-h.com:8000/uber/client/1/sum_miles/?starttime=20131201&endtime=20131202",
            "sum_miles_cid_date2" : "http://lans-h.com:8000/uber/client/2/sum_miles/?starttime=20131201&endtime=20131202",
            "sum_miles_cid_date3" : "http://lans-h.com:8000/uber/client/3/sum_miles/?starttime=20131201&endtime=20131202",

            "avg_fare_city1" : "http://lans-h.com:8000/uber/city/san_francisco/avg_fare/",
            "avg_fare_city2" : "http://lans-h.com:8000/uber/city/daly_city/avg_fare/",
            "avg_fare_city3" : "http://lans-h.com:8000/uber/city/san_bruno/avg_fare/",
            "avg_fare_city4" : "http://lans-h.com:8000/uber/city/san_mateo/avg_fare/",
            "avg_fare_city_date1" : "http://lans-h.com:8000/uber/city/san_francisco/avg_fare/?starttime=20131201&endtime=20131202",
            "avg_fare_city_date2" : "http://lans-h.com:8000/uber/city/daly_city/avg_fare/?starttime=20131201&endtime=20131202",
            "avg_fare_city_date3" : "http://lans-h.com:8000/uber/city/san_bruno/avg_fare/?starttime=20131201&endtime=20131202",
            "avg_fare_city_date4" : "http://lans-h.com:8000/uber/city/san_mateo/avg_fare/?starttime=20131201&endtime=20131202",
            
            "avg_rating_did1" : "http://lans-h.com:8000/uber/driver/11/avg_rating/",
            "avg_rating_did2" : "http://lans-h.com:8000/uber/driver/12/avg_rating/",
            "avg_rating_did_date1" : "http://lans-h.com:8000/uber/driver/11/avg_rating/?starttime=20131201&endtime=20131202",
            "avg_rating_did_date2" : "http://lans-h.com:8000/uber/driver/12/avg_rating/?starttime=20131201&endtime=20131202",
        }

        print
        for key, value in tests.items():
            req = urllib2.Request(value)
            res = urllib2.urlopen(req)
            print "testing [%s], result = \n%s\n" % (value, res.read())

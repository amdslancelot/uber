#import from django
from django.http import HttpResponse
from django.db.models import Sum, Avg
from django.shortcuts import render, get_object_or_404

#import from python
import os
os.environ['TZ'] = "GMT"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import json
import time
import datetime
from datetime import timedelta, datetime
from decimal import *

#import from app uber
import city
from uber.models import TripEvent, UberBase

#######################################
############ RESTful APIs #############
#######################################

def index(request):
    return HttpResponse("Hello, world. You're at the uber index.")

'''
total number of trips by date
'''
def tripCount(request):
    response = {}
    get = request.GET

    if get.has_key('starttime') and get.has_key('endtime'):
        result = getTripCount(get['starttime'], get['endtime'])
        ( response['starttime'], response['endtime'] ) = convertDateStringToUnixTime(get['starttime'], get['endtime'])
    else:
        result = getTripCount(None, None)
    response['total_num_trip'] = result

    return makeHttpResponse(response)

'''
total number of trips in the last hour
''' 
def tripCountLastHour(request):
    response = {}

    dtNow = datetime.now()
    utNow = dtNow.strftime("%s")
    utLastHour = (dtNow - timedelta(hours=1)).strftime("%s")
    
    result = TripEvent.objects.filter(start_time__gte=utLastHour) \
                              .filter(start_time__lt=utNow) \
                              .count()

    response['starttime'] = utLastHour
    response['endtime'] = utNow
    response['total_num_trip'] = result

    return makeHttpResponse(response)

'''
total numbers of clients
'''
def clientCount(request):
    response = {}
    get = request.GET

    # process 'finished' keyword
    finished = False
    if get.has_key('finished'):
        finished = True if get['finished'] == 'true' else False
        response['finished'] = finished

    # 1. processing 'starttime', 'endtime'
    # 2. run the query
    if get.has_key('starttime') and get.has_key('endtime'):
        result = getClientCount(get['starttime'], get['endtime'], finished=finished)
        ( response['starttime'], response['endtime'] ) = convertDateStringToUnixTime(get['starttime'], get['endtime'])
    else:
        result = getClientCount(None, None, finished=finished)
    response['total_num_client'] = result

    return makeHttpResponse(response)

'''
total miles per client
'''
def milesPerClient(request, cid):
    response = {}
    get = request.GET

    # 1. processing 'starttime', 'endtime'
    # 2. run the query
    if get.has_key('starttime') and get.has_key('endtime'):
        result = getMilesPerClient(cid, get['starttime'], get['endtime'])
        ( response['starttime'], response['endtime'] ) = convertDateStringToUnixTime(get['starttime'], get['endtime'])
    else:
        result = getMilesPerClient(cid, None, None)
    response['total_miles_per_client'] = convertResultToDict(result) #convert for Decimal

    return makeHttpResponse(response)

'''
avg fare for a specific city (where a city can be defined as a square)
'''
def avgFareInCity(request, ctname):
    response = {}
    get = request.GET

    # 1. processing 'starttime', 'endtime'
    # 2. run the query
    if get.has_key('starttime') and get.has_key('endtime'):
        result = getFaresInCityResult(ctname.lower(), get['starttime'], get['endtime'])
        ( response['starttime'], response['endtime'] ) = convertDateStringToUnixTime(get['starttime'], get['endtime'])
    else:
        result = getFaresInCityResult(ctname.lower(), None, None)
    response['avg_fare_in_city'] = result

    return makeHttpResponse(response)

'''
median rating for a driver
'''
def medianDriverRating(request, did):
    response = {}
    get = request.GET

    # 1. processing 'starttime', 'endtime'
    # 2. run the query
    if get.has_key('starttime') and get.has_key('endtime'):
        result = getRecordsByDriver(did, get['starttime'], get['endtime'])
        ( response['starttime'], response['endtime'] ) = convertDateStringToUnixTime(get['starttime'], get['endtime'])
    else:
        result = getRecordsByDriver(did, None, None)
    response['avg_rating_per_driver'] = result

    return makeHttpResponse(response)


###############################################
############ Processing functions #############
###############################################

'''
Convert starttime & endtime to unix time
'''
def convertDateStringToUnixTime(starttime, endtime):
    return ( datetime.strptime(starttime, "%Y%m%d").strftime("%s"), datetime.strptime(endtime, "%Y%m%d").strftime("%s") )

def getTripCount(starttime, endtime):
    
    result = TripEvent.objects

    if starttime is not None and endtime is not None:
        ( unixtime_start, unixtime_end ) = convertDateStringToUnixTime(starttime, endtime)
        result = result.filter(start_time__range=(unixtime_start, unixtime_end))

    return result.count()
    

def getClientCount(starttime, endtime, finished=False):

    result = TripEvent.objects
    
    if finished:
        now = int(time.time())
        result = result.filter(start_time__lt=now)

    if starttime is not None and endtime is not None:
        ( unixtime_start, unixtime_end ) = convertDateStringToUnixTime(starttime, endtime)
        result = result.filter(start_time__range=(unixtime_start, unixtime_end))
    
    return result.values_list('client_id', flat=True).distinct().count()

def getMilesPerClient(cid, starttime, endtime):

    result = TripEvent.objects.filter(client_id=cid)

    if starttime is not None and endtime is not None:
        ( unixtime_start, unixtime_end ) = convertDateStringToUnixTime(starttime, endtime)
        result = result.filter(start_time__range=(unixtime_start, unixtime_end))

    return result.values_list('client_id', 'distance') \
                 .annotate(total_miles=Sum('distance')) \
                 .values_list('client_id', 'total_miles')

def getFaresInCityResult(ctname, starttime, endtime):

    max_lat = max(city.city_coordinates[ctname][0][0], city.city_coordinates[ctname][1][0])
    min_lat = min(city.city_coordinates[ctname][0][0], city.city_coordinates[ctname][1][0])
    max_lng = max(city.city_coordinates[ctname][0][1], city.city_coordinates[ctname][1][1])
    min_lng = min(city.city_coordinates[ctname][0][1], city.city_coordinates[ctname][1][1])

    result = TripEvent.objects.filter(lat__range=(min_lat, max_lat)) \
                              .filter(lng__range=(min_lng, max_lng))

    if starttime is not None and endtime is not None:
        ( unixtime_start, unixtime_end ) = convertDateStringToUnixTime(starttime, endtime)
        result = result.filter(start_time__range=(unixtime_start, unixtime_end))

    return result.aggregate(Avg('fare'))

def getRecordsByDriver(did, starttime, endtime):
    result = TripEvent.objects.filter(driver_id=did)

    if starttime is not None and endtime is not None:
        ( unixtime_start, unixtime_end ) = convertDateStringToUnixTime(starttime, endtime)
        result = result.filter(start_time__range=(unixtime_start, unixtime_end))

    return result.aggregate(Avg('rating'))

def convertResultToDict(result):
    d = {}
    for key, value in result:
        if type(value) == Decimal:
            d[key] = float(value)
        else:
            d[key] = value

    return d

def makeHttpResponse(response):
   return HttpResponse(json.dumps(response), content_type="application/json")

import sys, os
sys.path.append(os.path.abspath(''))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import json, time, datetime
from decimal import *
from datetime import datetime

# Import from django
from django.http import HttpResponse
from django.db.models import Sum, Avg

# Import from project Uber
from uber.models import TripEvent, UberBase
import city

'''
Store a trip event record
'''
def record_trip_event(client_id, driver_id, start_time, lat, lng, fare, distance, rating):
    e = TripEvent(client_id=client_id, driver_id=driver_id, start_time=start_time, \
                  lat=lat, lng=lng, fare=fare, distance=distance, rating=rating)
    e.save()

def delete_all_records():
    TripEvent.objects.all().delete()

def print_all_records():
    return TripEvent.objects.all()

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

def getTripCountLastHour(utLastHour, utNow):
    return TripEvent.objects.filter(start_time__gte=utLastHour) \
                            .filter(start_time__lt=utNow) \
                            .count()

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

if __name__ == "__main__":
    delete_all_records()
    record_trip_event(1, 11, 1385895912, Decimal("37.774650"), Decimal("-122.419122"), Decimal("5.0"), Decimal("5.0"), 5) #SF
    record_trip_event(1, 12, 1385895926, Decimal("37.790184"), Decimal("-122.429845"), Decimal("3.0"), Decimal("5.0"), 3) #SF
    record_trip_event(2, 11, 1385895927, Decimal("37.68776"),  Decimal("-122.486598"), Decimal("10.0"), Decimal("6.0"), 4) #Daly City
    record_trip_event(3, 12, 1385895928, Decimal("37.637072"), Decimal("-122.418277"), Decimal("11.0"), Decimal("7.0"), 4) # San Bruno
    record_trip_event(4, 12, 1417850394, Decimal("37.5688"),   Decimal("-122.316336"), Decimal("12.0"), Decimal("8.0"), 5) #future #San Mateo
    print print_all_records()

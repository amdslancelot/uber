from datetime import timedelta
from uber_util import *

#######################################
############ RESTful APIs #############
#######################################

'''
Project landing page
'''
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

    result = getTripCountLastHour(utLastHour, utNow)

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


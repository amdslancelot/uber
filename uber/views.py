from datetime import timedelta
from uber_util import *
from django.views.decorators.csrf import csrf_exempt

#######################################
############ RESTful APIs #############
#######################################

'''
Project landing page
'''
def index(request):
    return HttpResponse("Hello, world. You're at the uber index.")

'''
Add a new trip through API
'''
@csrf_exempt
def addTrip(request):
    response = {}
    post = request.POST

    if post.has_key('client_id') and post.has_key('driver_id') and post.has_key('start_time') and \
       post.has_key('lat') and post.has_key('lng') and post.has_key('fare') and \
       post.has_key('distance') and post.has_key('rating'):
        record = record_trip_event(post['client_id'], post['driver_id'], post['start_time'], post['lat'], \
                          post['lng'], post['fare'], post['distance'], post['rating'])
        response['trip'] = record.dict()
        response['success'] = "Success"
    else:
        response['error'] = "Missing columns"

    return makeHttpResponse(response)

'''
Show all trip records
'''
def showAllTrip(request):
    response = {}
    l = []

    for e in TripEvent.objects.all():
        l.append(e.dict())
    response['trip'] = l

    return makeHttpResponse(response)

'''
Show trip info through trip id
'''
def showTrip(request, tid):
    response = {}
    
    if tid:
        response['trip'] = TripEvent.objects.filter(id=tid)[0].dict()
        response['success'] = "Success"
    else:
        response['error'] = "Cannot find Trip record by id %s" % (tid)

    return makeHttpResponse(response)

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


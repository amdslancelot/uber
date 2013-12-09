
Uber Code Challenge

====
[A Quick Overview of Uber Application]

The application is for a simple code challenge provided by Uber.
This application is trying to build a system to allow users to access trip event records by calling RESTful API service.
It is able to do the following things: 

    
    GET uber/trip/
        return all the trip info

    GET uber/trip/<trip_id>/
        return the trip record according to the given <trip_id>
   
   POST uber/trip/add/
        doing a POST request to insert one new trip record into database
        form:
            { 
              'client_id' : x, 
              'driver_id' : xx, 
              'start_time' : xxxxxxxxxx, 
              'lat' : Decimal("xx.xxxx"), 
              'lng' : Decimal("xxx.xxxxxx"), 
              'fare' : Decimal("x.x"), 
              'distance' : Decimal("x.x"), 
              'rating' : x
            }

    GET uber/trip/num/
        return the total number of trips

    GET uber/client/num/
        return the total number of clients

    GET uber/client/num/?finished=true
        return the total number of clients who’ve taken trips

    GET uber/trip/num_last_hour/
        return the total number of trips in the last hour

    GET uber/client/<client_id>/sum_miles/
        return the total miles per client

    GET uber/city/<city_name>/avg_fare/
        return the avg fare for a specific city (where a city can be defined as a square)

        * According to the doc descrption, "where a city can be defined as a square",
          here I only support the following city tags for now:

          'san_francisco', 'daly_city', 'san_bruno', 'san_mateo'
        
          For each city, the system records the left-up most coordinate and the right-down most coordinate to define a square.
          In the uber/city.py, the system uses this look-up dictionary to decide if a coordinate is in a city:

          city_coordinates = {
              'san_francisco' : [ [Decimal("37.804359"), Decimal("-122.51924")], [Decimal("37.70664"), Decimal("-122.370633")] ],
              'daly_city' : [ [Decimal("37.70827"), Decimal("-122.506588")], [Decimal("37.650665"), Decimal("-122.44479")] ],
              'san_bruno' : [ [Decimal("37.650665"),Decimal("-122.44479")], [Decimal("37.60988"),Decimal("-122.35484")] ],
              'san_mateo' : [ [Decimal("37.569617"),Decimal("-122.34866")], [Decimal("37.531782"),Decimal("-122.277884")] ],
          }

    GET uber/driver/<driver_id>/avg_rating/
        ●   Get the median rating for a driver


Extra Points:

    It also supports giving date strings to do date range queries.
    * () means not required

    GET uber/trip/num/(?starttime=YYYYmmdd&endtime=YYYYmmdd)
        ex: uber/trip/num/?starttime=20131201&endtime=20131202

    GET uber/client/num/(?starttime=YYYYmmdd&endtime=YYYYmmdd)
        ex: uber/client/num/?starttime=20131201&endtime=20131202

    GET uber/client/num/?finished=true(&starttime=YYYYmmdd&endtime=YYYYmmdd)
        ex: uber/client/num/?finished=true&starttime=20131201&endtime=20131202

    GET uber/client/<client_id>/sum_miles/(?starttime=YYYYmmdd&endtime=YYYYmmdd)
        ex: uber/client/1/sum_miles/?starttime=20131201&endtime=20131202

    GET uber/city/<city_name>/avg_fare/(?starttime=YYYYmmdd&endtime=YYYYmmdd)
        ex: uber/city/san_francisco/avg_fare/?starttime=20131201&endtime=20131202

    GET uber/driver/<driver_id>/avg_rating/(?starttime=YYYYmmdd&endtime=YYYYmmdd)
        ex: uber/driver/11/avg_rating/?starttime=20131201&endtime=20131202


###############################################################

[File System]

db/
__init__.py
main
manage.py
mysite/
    __init__.py
    settings.py
    urls.py
    wsgi.py
README.md
uber/
    city.py
    __init__.py
    models.py
    tests.py
    uber_util.py
    urls.py
    views.py

###############################################################

[Install Guide]

1. This application is built on Django 1.6 and using it's default database SQLite 3.
   (For information about how to install Django: https://docs.djangoproject.com/en/1.6/intro/install/)

2. (Source code: https://github.com/amdslancelot/uber)

   After install the version control tool 'Git',
   (Git install guide: http://git-scm.com/book/en/Getting-Started-Installing-Git)
   you can use the command below to checkout the developement version:

   $ git clone https://github.com/amdslancelot/uber.git YOUR-DIRECTORY-NAME

3. Go to your new directory:

   $ cd YOUR-DIRECTORY-NAME

4. Establish Uber database by the command below:

   $ python manage.py syncdb

   Your outout should be like:

   ===========================================================================================
   Creating tables ...
   Creating table auth_permission
   Creating table auth_group_permissions
   Creating table auth_group
   Creating table auth_user_groups
   Creating table auth_user_user_permissions
   Creating table auth_user
   Creating table django_content_type
   Creating table django_session
   Creating table django_site
   Creating table uber_tripevent

   You just installed Django's auth system, which means you don't have any superusers defined.
   Would you like to create one now? (yes/no):
   ===========================================================================================

   You can simply answer 'no' to skip this step.

5. Run the command below to insert some sample data for Uber project:

   $ python uber/uber_util.py

   The uber_util.py is using the sample data below:
   
   <TripEvent: TripEvent(client_id=1 ,distance=5 ,driver_id=11 ,fare=5 ,id=1 ,lat=37.77465 ,lng=-122.419122 ,rating=5 ,start_time=1385895912)>, 
   <TripEvent: TripEvent(client_id=1 ,distance=5 ,driver_id=12 ,fare=3 ,id=2 ,lat=37.790184 ,lng=-122.429845 ,rating=3 ,start_time=1385895926)>, 
   <TripEvent: TripEvent(client_id=2 ,distance=6 ,driver_id=11 ,fare=10 ,id=3 ,lat=37.68776 ,lng=-122.486598 ,rating=4 ,start_time=1385895927)>, 
   <TripEvent: TripEvent(client_id=3 ,distance=7 ,driver_id=12 ,fare=11 ,id=4 ,lat=37.637072 ,lng=-122.418277 ,rating=4 ,start_time=1385895928)>, 
   <TripEvent: TripEvent(client_id=4 ,distance=8 ,driver_id=12 ,fare=12 ,id=5 ,lat=37.5688 ,lng=-122.316336 ,rating=5 ,start_time=1417850394)>

   ***The record_trip_event() function is located in uber/uber_util.py
      If you want to insert more records, feel free to use it.

6. You can run the server by
   ex:

   $ python manage.py runserver YOUR-SERVER-ADDRESS

7. Now you can play with the RESTful API which has been described in the [A Quick Overview of Uber Application] section!

###############################################################

[Testing]

1. To run unittest, use this command below:

   $ ./manage.py test uber
   Creating test database for alias 'default'...
   ..............
   ----------------------------------------------------------------------
   Ran 14 tests in 0.075s
   
   OK
   Destroying test database for alias 'default'...

   The unittest will create a temporary database in Django, generate test records and test all the Django views in Uber project.
   The unittest code is in uber/tests.py.

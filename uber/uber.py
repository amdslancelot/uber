import sys
import os
sys.path.append(os.path.abspath('..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from uber.models import TripEvent, UberBase

from decimal import *

def record_trip_event(client_id, driver_id, start_time, lat, lng, fare, distance, rating):
    e = TripEvent(client_id=client_id, driver_id=driver_id, start_time=start_time, \
                  lat=lat, lng=lng, fare=fare, distance=distance, rating=rating)
    e.save()

def delete_all_records():
    TripEvent.objects.all().delete()

def print_all_records():
    return TripEvent.objects.all()

if __name__ == "__main__":
    delete_all_records()
    record_trip_event(1, 11, 1385895912, Decimal("37.774650"), Decimal("-122.419122"), Decimal("5.0"), Decimal("5.0"), 5) #SF
    record_trip_event(1, 12, 1385895926, Decimal("37.790184"), Decimal("-122.429845"), Decimal("3.0"), Decimal("5.0"), 3) #SF
    record_trip_event(2, 11, 1385895927, Decimal("37.68776"),  Decimal("-122.486598"), Decimal("10.0"), Decimal("6.0"), 4) #Daly City
    record_trip_event(3, 12, 1385895928, Decimal("37.637072"), Decimal("-122.418277"), Decimal("11.0"), Decimal("7.0"), 4) # San Bruno
    record_trip_event(4, 12, 1417850394, Decimal("37.5688"),   Decimal("-122.316336"), Decimal("12.0"), Decimal("8.0"), 5) #future #San Mateo
    print print_all_records()

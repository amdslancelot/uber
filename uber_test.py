import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
from uber.models import TripEvent, UberBase
from django.db.models import Sum, Avg
from decimal import *

if __name__ == "__main__":
    r = TripEvent.objects.filter(client_id=1).values_list('client_id', 'distance').annotate(total_miles=Sum('distance')).values_list('client_id', 'total_miles')
    for key, value in r:
        print key
        print type(value)

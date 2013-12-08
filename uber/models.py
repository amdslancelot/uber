from django.db import models
from decimal import *

class UberBase(models.Model):
    def __unicode__(self):
        result = self.__class__.__name__ + "("

        result += "id=%s" % (self.id)

        for a in self._meta.get_all_field_names():
            result += ", %s=%s" % (a, getattr(self, a))
            
        return result + ")"

    def dict(self):
        d = {}
        
        d['id'] = self.id
        
        for a in self._meta.get_all_field_names():
            v = getattr(self, a)
            if type(v) == Decimal:
                d[a] = float(v)
            else:
                d[a] = v

        return d

    class Meta:
        abstract = True

class TripEvent(UberBase):
    #UberBase.__init__(self)
    id         = models.AutoField(primary_key=True)
    client_id  = models.IntegerField(default=0)
    driver_id  = models.IntegerField(default=0)
    start_time = models.BigIntegerField(default=0)
    lat        = models.DecimalField(max_digits=20,  decimal_places=10)
    lng        = models.DecimalField(max_digits=20,  decimal_places=10)
    fare       = models.DecimalField(max_digits=20, decimal_places=4)
    distance   = models.DecimalField(max_digits=20, decimal_places=4)
    rating     = models.IntegerField(default=0)


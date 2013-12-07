from django.db import models

class UberBase(models.Model):
    def __unicode__(self):
        count = 0
        result = self.__class__.__name__ + "("
        for a in self._meta.get_all_field_names():
            if count != 0:
                result += " ,"
            #result += "%s=%s" % (a, self._meta.get_field(a))
            result += "%s=%s" % (a, getattr(self, a))
            
            count += 1
        return result + ")"

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

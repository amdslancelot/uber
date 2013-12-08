from django.conf.urls import patterns, url

from uber import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^trip/num/$', views.tripCount, name='tripCount'),
    url(r'^trip/$', views.showAllTrip, name='showAllTrip'),
    url(r'^trip/(?P<tid>\d+)/$', views.showTrip, name='showTrip'),
    url(r'^trip/add/$', views.addTrip, name='addTrip'),
    url(r'^trip/num_last_hour/$', views.tripCountLastHour, name='tripCountLastHour'),
    url(r'^client/num/$', views.clientCount, name='clientCount'),
    url(r'^client/(?P<cid>\d+)/sum_miles/$', views.milesPerClient, name='milesPerClient'),
    url(r'^city/(?P<ctname>[a-zA-Z_]+)/avg_fare/$', views.avgFareInCity, name='avgFareInCity'),
    url(r'^driver/(?P<did>\d+)/avg_rating/$', views.medianDriverRating, name='medianDriverRating'),
)

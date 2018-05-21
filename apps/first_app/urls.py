from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.add_plan),
    url(r'^process/add$', views.process_add),
    url(r'^login$', views.login),
    url(r'^jointrip/(?P<tripid>\d+)$', views.jointrip),
    url(r'^travels/destination/(?P<placeid>\d+)$', views.destination),
    url(r'^logout$', views.logout),
]

from django.conf.urls import patterns, include, url
from road_traffic.views import find_road, traffic_notif_main, highway_subscribe

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'traffic_notify.views.home', name='home'),
    url(r'^traffic-notifier/', traffic_notif_main),
    url(r'^find-road/', find_road),
    url(r'^highway-subscribe/', highway_subscribe),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

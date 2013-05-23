from django.db import models
from picklefield.fields import PickledObjectField
from datetime import datetime
import pytz

class Subscriber(models.Model) :
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __unicode__(self) :
        return "Subscriber-Email: " + self.email

class HighwaySubscriptions(models.Model) :
    highway = models.CharField(max_length=20)
    start_time = models.TimeField()
    subscribers = models.ManyToManyField(Subscriber)

    class Meta:
        verbose_name_plural = "HighwaySubscriptions"

    def __unicode__(self) :
        return "Highway: {0} @Time: {1}".format(self.highway,self.start_time)


class HighwayTrafficHistory(models.Model) :
    highway = models.CharField(max_length=20)
    direction = models.CharField(max_length=20)
    highway_id = models.IntegerField()
    traffic_date = models.DateTimeField()
    traffic = PickledObjectField()

    class Meta:
        verbose_name_plural = "HighwayTrafficHistories"

    def __unicode__(self) :
        return "Traffic History for {0} @DateTime: {1}".format(self.highway,
                    self.traffic_date)

def save_traffic_results(results_dict,traffic_time):
    """
    save the traffic dict into the db using a pickle model object
    Will use these for historical traffic analysis
    """
    # {'highway': highway, 'direction': 'direction', 'id': 'hwy_id'}
    results_header = results_dict[0]
    # get metadata from header
    highway = results_header['highway']
    direction = results_header['direction']
    highway_id = results_header['id']
    now = datetime.now(tz=pytz.UTC)
    # in theory we should not find a db entry unless time travel has been invented
    traffic_subscription_datetime = datetime(now.year,now.month,now.day,
                                        traffic_time.hour,traffic_time.minute,
                                        traffic_time.second,tzinfo=pytz.UTC)
    try :
        history = HighwayTrafficHistory.objects.get(highway=highway,
                            direction=direction,
                            highway_id=highway_id,
                            traffic_date=traffic_subscription_datetime)
    except HighwayTrafficHistory.DoesNotExist:
        # we don't have an entry in db, let's add one
        history = HighwayTrafficHistory(highway=highway,
                            direction=direction,
                            highway_id=highway_id,
                            traffic_date=traffic_subscription_datetime,
                            traffic=results_dict)
        history.save()
    except:
        print "Exception getting history obj hwy:{0}-{1}".format(highway,direction)
    else:
        print "Added history obj hwy:{0}-{1}".format(highway,direction)

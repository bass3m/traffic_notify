from datetime import time
from road_traffic.models import HighwaySubscriptions, Subscriber
from traffic_periodic.tasks import add_traffic_task

def get_email(subscriber) :
    email = [sub_vals['value'] for sub_vals in subscriber if sub_vals['name'] == 'subscriber_email'][0]
    # html does validation on this form, so it shouldn't be empty
    # raise an exception just in case
    if email == '':
        raise invalidEmailSpecified
    return email

def get_delivery_time(subscriber) :
    start_time = [sub_vals['value'] for sub_vals in subscriber if sub_vals['name'] == 'email_delivery_time'][0]
    if start_time is '':
        # default to 8am if no time was specified
        # Django only supports naive time objects and will raise 
        # an exception if you attempt to save an aware time object.
        email_delivery_time = time(8,0,0)
    else :
        hrs, mins = start_time.split(":")
        # Django only supports naive time objects and will raise 
        # an exception if you attempt to save an aware time object.
        email_delivery_time = time(int(hrs),int(mins),0)
    print "delivery email time is {0}".format(email_delivery_time)
    return email_delivery_time

def add_highway_subscription(highway,subscriber,location) :
    """
    {u'subscriber': [{u'name': u'subscriber_email', u'value': u'c@b.com'},
                     {u'name': u'email_delivery_time', u'value': ''}],
    """
    try:
        email = get_email(subscriber)
    except invalidEmailSpecified:
        raise

    try :
        subscriber_db = Subscriber.objects.get(email=email)
    except Subscriber.DoesNotExist:
        # a new subscriber
        subscriber_db = Subscriber(email=email)
        subscriber_db.save()
    except :
        print "Exception getting obj from db for subscriber: " + email
    else :
        print "Got/create db object for: " + email

    email_delivery_time = get_delivery_time(subscriber)
    # now let's go through the highways
    try :
        hwy_sub = HighwaySubscriptions.objects.get(highway=highway,
                    start_time=email_delivery_time)
    except HighwaySubscriptions.DoesNotExist:
        # we don't have an entry in db, let's add one
        hwy_sub = HighwaySubscriptions(highway=highway,
                                       start_time=email_delivery_time)
        hwy_sub.save()
    except:
        print "Exception getting obj from db for hwy: " + highway
    else:
        print "Added obj db for hwy: " + highway

    hwy_sub.subscribers.add(subscriber_db)
    task_id = add_traffic_task(highway,email,email_delivery_time,location)

def handle_subscription_request(sub_req) :
    """
    Subscription request contains an array of highways
    as well as the subscriber info (email) and the subscription
    time
    {u'subscriber': [{u'name': u'subscriber_email', u'value': u'c@b.com'},
                     {u'name': u'email_delivery_time', u'value': ''}],
     u'highways': [{u'latlng': {u'lat': 37.367428642539245, u'lng': -122.0642852783203}, u'highway': u'Norman Y. Mineta Hwy'},
                   {u'latlng': {u'lat': 37.317205770306465, u'lng': -121.97433471679689}, u'highway': u'I-280'},
                   {u'latlng': {u'lat': 37.25000751785145, u'lng': -121.95854187011717}, u'highway': u'CA-17'}]}
    """
    ret = "OK"
    # if time was not set, then default to 8am
    for hwy in sub_req['highways']:
        try:
            add_highway_subscription(hwy['highway'],sub_req['subscriber'],sub_req['location'])
        except:
            print ("Exception adding Hwy: {0} for Subscriber: {1}"
                    .format(hwy['highway'],sub_req['subscriber']))
            ret = "FAIL"
    return ret

def handle_unsubscribe_request(sub_req) :
    try:
        email = get_email(subscriber)
    except invalidEmailSpecified:
        raise

    try :
        subscriber_db = Subscriber.objects.get(email=email)
    except :
        print "Exception getting obj from db for subscriber: " + email
    else :
        print "unsubscribing : " + email

    # now let's go through the highways for subscriber
    try :
        hwy_sub = HighwaySubscriptions.objects.get(highway=highway,start_time=email_delivery_time)
    except HighwaySubscriptions.DoesNotExist:
        # we don't have an entry in db, let's add one
        hwy_sub = HighwaySubscriptions(highway=highway,
                                       start_time=email_delivery_time)
        hwy_sub.save()
    except:
        print "Exception getting obj from db for hwy: " + highway
    else:
        print "Added obj db for hwy: " + highway

    #hwy_sub.subscribers.add(subscriber_db)
    #task_id = add_traffic_task(highway,email,email_delivery_time)

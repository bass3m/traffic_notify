from celery import task
from datetime import timedelta, datetime
import subprocess

from road_traffic.models import save_traffic_results
from road_traffic.hwy_utils import get_hwy_mapping, parse_traffic_results
from traffic_notify.notify import notify_subscriber
from traffic_notify.settings import TRAFFIC_NOTIFY

def get_highway_traffic(highway,location) :
    """
    Invoke phantomJS to do the required query, using subprocess
    """
    hwy_details = get_hwy_mapping(highway)
    phantom_results = []

    for hwy in hwy_details['detail']:
        cmd = [TRAFFIC_NOTIFY['phantomjs_location'],
               TRAFFIC_NOTIFY['phantomjs_script_location'],
               str(hwy['hwy_id']),"{0:.05f}".format(location['lat']),
               "{0:.05f}".format(location['lng'])]
        print cmd
        phantom = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
        # basic cleanup and trimming
        phantom = phantom.strip().split('\n')
        # get rid of the status header containing status from phantomJS
        phantom.pop(0)
        # filter out some spurious errors
        phantom = filter(lambda item : item and 'alert' not in item,phantom)
        phantom.insert(0,{'highway': highway, 'direction': hwy['direction'],
                          'id': hwy['hwy_id']})
        phantom_results.append(phantom)
    return phantom_results

@task(name='task.get_latest_traffic')
def get_latest_traffic(highway,email,email_delivery_time,location,keep_running) :
    """
    need to call phantomjs with parameters indicating the highway
    for our query. Is the latlng needed ? XXX
    Need to schedule this task again in 24 hrs
    """
    phantom_res = get_highway_traffic(highway,location)
    for res in phantom_res:
        traffic_dict_list = parse_traffic_results(res)
        save_traffic_results(traffic_dict_list,email_delivery_time)
        notify_subscriber(email,email_delivery_time,traffic_dict_list)

    if keep_running == True:
        # schedule task to run in 24hrs
        now = datetime.now()
        requested_time = now.replace(day=(now + timedelta(days=1)).day,
                                     hour=email_delivery_time.hour,
                                     minute=email_delivery_time.minute,
                                     second=email_delivery_time.second)
        # this takes care of rollover as well
        interval = (requested_time - now).seconds
        print "Hwy: {0} email: {1} to run in: {2}".format(highway,email,interval)
        task_id = get_latest_traffic.apply_async(args=[highway,email,
                                                 email_delivery_time,
                                                 location,
                                                 keep_running],
                                                 countdown=interval)
    else:
        print "Done with running this task"
        task_id = 0
    return task_id

def add_traffic_task(highway,email,email_delivery_time,location,keep_running=True) :
    """
    eta is conveniantly a python datetime
    """
    # schedule task to run at specified time
    now = datetime.now()
    requested_time = now.replace(hour=email_delivery_time.hour,
                                 minute=email_delivery_time.minute,
                                 second=email_delivery_time.second)
    # this takes care of rollover as well
    interval = (requested_time - now).seconds
    print "Hwy: {0} email: {1} to run in: {2}".format(highway,email,interval)
    task_id = get_latest_traffic.apply_async(args=[highway,
                                             email,
                                             email_delivery_time,
                                             location,
                                             keep_running],
                                             countdown=interval)
    return task_id

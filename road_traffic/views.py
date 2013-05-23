# Create your views here.
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
from django.http import  HttpResponse , Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import ensure_csrf_cookie

import json
from rev_geo_lookup import GoogleRevGeoLookup
from highway_subscriptions import handle_subscription_request

@ensure_csrf_cookie
def traffic_notif_main(request):
    return render_to_response(u'traffic_template.html',
            # num of subscriptions
            {'subscription_list' : xrange(0,5)},
            context_instance=RequestContext(request))

def find_road(request):
    """
    We have the start and end lat lng so do a reverse geo lookup 
    for motorways, we want to specify closest as well
    Expecting segment_latlng to be formatted as follows:
    {'latlng':[x,y]}
    """
    if not request.is_ajax():
        raise Http404

    if not request.method == 'POST':
        raise Http404

    post_req = json.loads(request.raw_post_data)
    print post_req
    latlng = post_req[u'latlng']

    # do the lookup
    json_resp = json.dumps(GoogleRevGeoLookup(latlng['lat'],latlng['lng']).lookup_hwy())
    return HttpResponse(json_resp,mimetype="application/json")

def highway_subscribe(request):
    """
    Highway subscriptions: User provides email address and optionally
    a time when they want the email to be sent. (If no time provided,
    then i will default to some AM time).
    The user provides up to 5 highways to monitor traffic information.
    Expecting input date to be formatted as follows:
    {'subscriber': {'name' : 'subscriber-email', 'val' : email_addr,
                    'name' : "email_delivery_time", 'val' : time},
     'highways' : ["hwy1", "hwy2", ...]}
    """
    if not request.is_ajax():
        raise Http404

    if not request.method == 'POST':
        raise Http404

    post_req = json.loads(request.raw_post_data)
    print post_req
    ret = handle_subscription_request(post_req)
    json_resp = {'status' : ret}
    return HttpResponse(json_resp,mimetype="application/json")

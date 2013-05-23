import urllib2
import json

class RevGeoLookup :
    """
    Base class to do reverse geo lookups, abstracts the url handling
    """
    def __init__(self,lat,lng) :
        self.lat = lat
        self.lng = lng
    def do_lookup(self,url):
        json_lookup = {}
        try:
            urlf = urllib2.urlopen(url).read()
        except:
            # XXX can i get the class str_name here for the inherited class ?
            print "Error calling urlopen().read() is site down ?"
        else:
            json_lookup = json.loads(urlf)
        return json_lookup
    def lookup_latlng(self):
        """
        Implemented by subclasses
        """
        pass
    def process_results(self):
        """
        Implemented by subclasses
        """
        pass
    def lookup_hwy(self) :
        return self.process_results(self.lookup_latlng())

class CloudmadeRevGeoLookup(RevGeoLookup) :
    """
    Do reverse lookup using the cloudmade api, need to provide the lat/lng
    as well as the api-key. Cloudmade returns a found item in the json
    return data which indicates the number of found matches.
    We are matching closest to the provided lat/lng and since we're
    only searching for highways (motorways) we include that as well
    >>> from road_traffic.rev_geo_lookup import CloudmadeRevGeoLookup
    >>> from traffic_notify.settings import TRAFFIC_NOTIFY
    >>> clo = CloudmadeRevGeoLookup(TRAFFIC_NOTIFY['cloudmade_api_key'],37.316250118431746,-121.97141647338867)
    >>> clo.lookup_hwy()
    >>> {'lat': 37.316250118431746, 'lng': -121.97141647338867, 'name': u'I 880 I 880'}
    """
    def __init__(self,api_key,lat,lng) :
        self.api_key = api_key
        RevGeoLookup.__init__(self,lat,lng)

    def lookup_latlng(self) :
        cloud_url = 'http://geocoding.cloudmade.com/' + self.api_key + '/geocoding/v2/find.js?around='
        url = cloud_url + str(self.lat) +',' + str(self.lng) + '&distance=closest&object_type=motorway'
        return RevGeoLookup.do_lookup(self,url)

    def process_results(self,json_cloudmade_lookup) :
        """
        Process the returned json and return the name and ref back,
        skipping the other bunch of stuff returned
        """
        print json_cloudmade_lookup
        road_lookup_resp = {'lat' : self.lat, 'lng' : self.lng, 'name' : ''}
        if json_cloudmade_lookup.get('found',0):
            # we found a match
            road_lookup_resp['name'] = (
                json_cloudmade_lookup['features'][0]['properties']['name'] +
                " " + json_cloudmade_lookup['features'][0]['properties']['ref'])
        return road_lookup_resp

class GoogleRevGeoLookup(RevGeoLookup) :
    """
    Do reverse lookup using the Google api, need to only provide the lat/lng
    Google returns the results from closest matches. So highway, followed
    by city, county, state etc..
    >>> from road_traffic.rev_geo_lookup import GoogleRevGeoLookup
    >>> goog = GoogleRevGeoLookup(37.316250118431746,-121.97141647338867)
    >>> res = goog.lookup_hwy()
    >>> res['name']
    >>> u'Interstate 280'
    """
    def __init__(self,lat,lng) :
        RevGeoLookup.__init__(self,lat,lng)

    def lookup_latlng(self) :
        """
        Setting sensor to true, i guess since i'm using html5 geolocation
        that's considered true
        """
        url = ('http://maps.googleapis.com/maps/api/geocode/json?latlng='
                  + str(self.lat) + ',' + str(self.lng) + '&sensor=true')
        return RevGeoLookup.do_lookup(self,url)

    def process_results(self,json_goog_lookup) :
        """
        verify that lookup was successful by looking for a status == OK
        we're looking for a returned types of route, otherwise don't consider
        that a match, also return the short_name from the results
        An example is in order:
        "results" : [{
         "address_components" : [{
               "long_name" : "Junipero Serra Fwy",
               "short_name" : "Interstate 280",
               "types" : [ "route" ]
        """
        road_lookup_resp = {'lat' : self.lat, 'lng' : self.lng, 'name' : ''}
        # verify that status was OK
        if json_goog_lookup.get('status','') != 'OK':
            return road_lookup_resp
        # make sure that we found a road/hwy
        if json_goog_lookup['results'][0]['address_components'][0]['types'][0] != u'route':
            return road_lookup_resp
        # things look ok, let's return the name
        road_lookup_resp['name'] = json_goog_lookup['results'][0]['address_components'][0]['short_name']
        print json_goog_lookup['results'][0]['address_components'][0]
        return road_lookup_resp

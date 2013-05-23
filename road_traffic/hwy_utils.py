from difflib import get_close_matches
import itertools

hwy_alternate_names = [
    {"alt_name" : "CHP Officer Scott M. Greenly Memorial Freeway", "name" : "85"},
    {"alt_name" : "Norman Y. Mineta Highway", "name" : "85"},
    {"alt_name" : "West Valley Freeway", "name" : "85"},
    {"alt_name" : "Dwight D. Eisenhower Highway", "name" : "80"},
    {"alt_name" : "Bayshore Freeway", "name" : "101"},
    {"alt_name" : "Officer Dave Chetcuti Memorial Highway", "name" : "101"},
    {"alt_name" : "Donald D. Doyle Highway", "name" : "680"},
    {"alt_name" : "John F. Foran Freeway", "name" : "280"},
    {"alt_name" : "Quentin L. Kopp Freeway", "name" : "380"},
    {"alt_name" : "James Lick Memorial Freeway", "name" : "101"},
    {"alt_name" : "MacArthur Freeway", "name" : "580"},
    {"alt_name" : "Military Servicewomen's Memorial Highway", "name" : "101"},
    {"alt_name" : "Nimitz Freeway", "name" : "880"},
    {"alt_name" : "Lewis E. Platt Memorial Highway", "name" : "87"},
    {"alt_name" : "Junipero Serra Freeway", "name" : "280"},
    {"alt_name" : "Sinclair Freeway", "name" : "280"},
    {"alt_name" : "John B. Williams Freeway", "name" : "980"},
    {"alt_name" : "Cabrillo Highway", "name" : "1"}
]

hwy_names = [
    {"hwy" : "1", "detail" : [{"direction" : "North", "hwy_id" : 0},
        {"direction" : "South", "hwy_id" : 1}]},
    {"hwy" : "4", "detail" : [{"direction" : "East", "hwy_id" : 2},
        {"direction" : "North", "hwy_id" : 3},
        {"direction" : "South", "hwy_id" : 4},
        {"direction" : "West", "hwy_id" : 5}]},
    {"hwy" : "5", "detail" : [{"direction" : "North", "hwy_id" : 6},
        {"direction" : "South", "hwy_id" : 7}]},
    {"hwy" : "12", "detail" : [{"direction" : "East", "hwy_id" : 8},
        {"direction" : "West", "hwy_id" : 9}]},
    {"hwy" : "13", "detail" : [{"direction" : "North", "hwy_id" : 10},
        {"direction" : "South", "hwy_id" : 11}]},
    {"hwy" : "17", "detail" : [{"direction" : "North", "hwy_id" : 12},
        {"direction" : "South", "hwy_id" : 13}]},
    {"hwy" : "24", "detail" : [{"direction" : "East", "hwy_id" : 14},
        {"direction" : "West", "hwy_id" : 15}]},
    {"hwy" : "37", "detail" : [{"direction" : "East", "hwy_id" : 16},
        {"direction" : "West", "hwy_id" : 17}]},
    {"hwy" : "50", "detail" : [{"direction" : "East", "hwy_id" : 18},
        {"direction" : "West", "hwy_id" : 19}]},
    {"hwy" : "65", "detail" : [{"direction" : "North", "hwy_id" : 24},
        {"direction" : "South", "hwy_id" : 25}]},
    {"hwy" : "80", "detail" : [{"direction" : "East", "hwy_id" : 26},
        {"direction" : "West", "hwy_id" : 27}]},
    {"hwy" : "84", "detail" : [{"direction" : "North", "hwy_id" : 30},
        {"direction" : "East", "hwy_id" : 31},
        {"direction" : "North", "hwy_id" : 32},
        {"direction" : "South", "hwy_id" : 33},
        {"direction" : "West", "hwy_id" : 34},
        {"direction" : "South", "hwy_id" : 35}]},
    {"hwy" : "85", "detail" : [{"direction" : "North", "hwy_id" : 36},
        {"direction" : "South", "hwy_id" : 37}]},
    {"hwy" : "87", "detail" : [{"direction" : "North", "hwy_id" : 38},
        {"direction" : "South", "hwy_id" : 39}]},
    {"hwy" : "92", "detail" : [{"direction" : "East", "hwy_id" : 40},
        {"direction" : "West", "hwy_id" : 41}]},
    {"hwy" : "99", "detail" : [{"direction" : "North", "hwy_id" : 42},
        {"direction" : "South", "hwy_id" : 43}]},
    {"hwy" : "101", "detail" : [{"direction" : "North", "hwy_id" : 44},
        {"direction" : "South", "hwy_id" : 45}]},
    {"hwy" : "109", "detail" : [{"direction" : "North", "hwy_id" : 46},
        {"direction" : "South", "hwy_id" : 47}]},
    {"hwy" : "113", "detail" : [{"direction" : "North", "hwy_id" : 48},
        {"direction" : "South", "hwy_id" : 49}]},
    {"hwy" : "205", "detail" : [{"direction" : "East", "hwy_id" : 50},
        {"direction" : "West", "hwy_id" : 51}]},
    {"hwy" : "237", "detail" : [{"direction" : "East", "hwy_id" : 52},
        {"direction" : "West", "hwy_id" : 53}]},
    {"hwy" : "238", "detail" : [{"direction" : "North", "hwy_id" : 54},
        {"direction" : "South", "hwy_id" : 55}]},
    {"hwy" : "242", "detail" : [{"direction" : "North", "hwy_id" : 56},
        {"direction" : "South", "hwy_id" : 57}]},
    {"hwy" : "280", "detail" : [{"direction" : "North", "hwy_id" : 58},
        {"direction" : "South", "hwy_id" : 59}]},
    {"hwy" : "380", "detail" : [{"direction" : "East", "hwy_id" : 60},
        {"direction" : "West", "hwy_id" : 61}]},
    {"hwy" : "505", "detail" : [{"direction" : "North", "hwy_id" : 62},
        {"direction" : "South", "hwy_id" : 63}]},
    {"hwy" : "580", "detail" : [{"direction" : "East", "hwy_id" : 64},
        {"direction" : "West", "hwy_id" : 65}]},
    {"hwy" : "680", "detail" : [{"direction" : "North", "hwy_id" : 66},
        {"direction" : "South", "hwy_id" : 67}]},
    {"hwy" : "780", "detail" : [{"direction" : "East", "hwy_id" : 68},
        {"direction" : "West", "hwy_id" : 69}]},
    {"hwy" : "880", "detail" : [{"direction" : "North", "hwy_id" : 70},
        {"direction" : "South", "hwy_id" : 71}]},
    {"hwy" : "980", "detail" : [{"direction" : "East", "hwy_id" : 72},
        {"direction" : "West", "hwy_id" : 73}]}
]

def get_hwy_mapping(highway) :
    """
    Find the closest match to specified highway.
    If we don't a match then most probably, the highway has
    an alias name, so we need to search for that if required
    """
    hwys = [h['hwy'] for h in hwy_names]
    # set the cutoff in order to match short names like Highway 1
    matches = get_close_matches(highway,hwys,cutoff=0.4)
    if len(matches) == 0:
        # if we didn't find any matches
        # check the alternate names for hwys
        alt_names = [alt['alt_name'] for alt in hwy_alternate_names]
        matches = get_close_matches(alt_names,hwys)
    return [hw for hw in hwy_names if hw['hwy'] == matches[0]][0] \
                if len(matches) else None

def parse_traffic_results(results):
    """
    parse the returned results from phantomJS into a dict.
    """
    # let's remove the header which contains some metadata before processing
    # header looks as follows:
    # {'highway': highway, 'direction': 'direction', 'id': 'hwy_id'}
    res_header = results.pop(0)
    # split the location name, current speed and speed limit
    get_traffic = (traffic_location.split(',') for traffic_location in results)
    # keys for traffic dict
    header = ['name','speed','limit']
    # create the traffic dict using the header list for keys
    traffic_dict_list = [{k : v for k,v in itertools.izip(header,traffic)} \
                            for traffic in get_traffic]
    # now add the header back to our list
    traffic_dict_list.insert(0,res_header)
    return traffic_dict_list

import sys
import json
import urllib

with open(sys.argv[1]) as fp:
    data = json.loads(fp.read())

cache = {}

def search(l):
    if l not in cache:
        cache[l] = json.loads(urllib.urlopen('http://maps.google.com/maps/api/geocode/json?address={}&sensor=false'.format(urllib.urlencode({'a': l})[2:])).read())['results']
    return cache[l]

for friend in data:
    if 'current_location' in friend:
        location = friend['current_location']['name']
        locationdata = search(location)
        if len(locationdata) > 0:
            friend['current_location']['latitude'] = locationdata[0]['geometry']['location']['lat']
            friend['current_location']['longitude'] = locationdata[0]['geometry']['location']['lng']
    if 'hometown_location' in friend:
        location = friend['hometown_location']['name']
        locationdata = search(location)
        if len(locationdata) > 0:
            friend['hometown_location']['latitude'] = locationdata[0]['geometry']['location']['lat']
            friend['hometown_location']['longitude'] = locationdata[0]['geometry']['location']['lng']
print json.dumps(data)

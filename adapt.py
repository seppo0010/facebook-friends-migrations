# encoding=utf8
import json
import hashlib
import sys

import math

def distance_on_unit_sphere(lat1, long1, lat2, long2):
    if lat1 == lat2 and long1 == long2: return 0
    degrees_to_radians = math.pi/180.0
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) +
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos(cos)
    return arc * 6378.1

with open('friends.json') as fp:
    data = json.loads(fp.read())

towns = []
edges = {}

def get_name(name):
    if name in (
            'Los Altos, California',
            'Oakland, California',
            'San Jose, California',
            'Greenbrae, California',
            'Fremont, California',
            'Saratoga, California',
            ): return 'San Francisco, California'

    if name in (
            u'San Telmo, Distrito Federal, Argentina',
            u'Caseros, Buenos Aires',
            u'Olivos, Buenos Aires',
            u'Merlo, Buenos Aires',
            u'Acassuso',
            u'Vicente López',
            u'Quilmes, Buenos Aires',
            u'Centro, Distrito Federal, Argentina',
            u'Temperley',
            u'Villa Crespo, Distrito Federal, Argentina',
            u'Almirante Brown, Buenos Aires, Argentina',
            u'Lanús, Argentina',
            u'Recoleta, Distrito Federal, Argentina',
            u'Boulogne, Buenos Aires, Argentina',
            u'Villa Adelina',
            u'Alberti, Buenos Aires',
            ): return u'Buenos Aires, Argentina'
    if name in (
            'Cerritos, California',
            ): return 'Los Angeles, California'
    if name in (
            'Brockton, Massachusetts',
            'Topsfield, Massachusetts',
            ): return 'Boston, Massachusetts'
    if name in (
            u'Concepción De La Sierra, Misiones, Argentina',
            ): return u'Estación Apóstoles, Misiones, Argentina'
    return name


for f in data['data']:
    hometown, currenttown = None, None
    if None in (f['hometown_location'], f['current_location']):
        continue
    if 'Llanfairpwllgwyngyllgogerychwyrndrobwllllantysilio, Gwynedd, United Kingdom' in (f['hometown_location']['name'], f['current_location']['name']):
        continue

    if f['hometown_location']['name'] == f['current_location']['name']:
        continue

    if f['hometown_location'] is not None:
        lat = f['hometown_location']['latitude']
        lon = f['hometown_location']['longitude']
        hometown = None
        for i, t in enumerate(towns):
            # d = distance_on_unit_sphere(lat, lon, t[0], t[1])
            if get_name(f['hometown_location']['name']) == get_name(t[2]['name']):
            # if d < 54 or f['hometown_location']['name'] == t[2]['name']:
                hometown = i
                break

        if hometown is None:
            hometown = len(towns)
            towns.append((lat, lon, f['hometown_location'], 0))

    if f['current_location'] is not None:
        lat = f['current_location']['latitude']
        lon = f['current_location']['longitude']
        currenttown = None
        for i, t in enumerate(towns):
            # d = distance_on_unit_sphere(lat, lon, t[0], t[1])
            if get_name(f['current_location']['name']) == get_name(t[2]['name']):
            # if d < 54 or f['current_location']['name'] == t[2]['name']:
                currenttown = i
                break

        if currenttown is None:
            currenttown = len(towns)
            towns.append((lat, lon, f['current_location'], 0))

    if None in (currenttown, hometown):
        continue

    if hometown not in edges:
        edges[hometown] = {}
    if currenttown not in edges[hometown]:
        edges[hometown][currenttown] = 0

    edges[hometown][currenttown] += 1
    towns[hometown] = tuple(towns[hometown][:3]) + ((towns[hometown][3] + 1),)

if sys.argv[1] == 'json':
    table = []
    for i in range(0, len(towns)):
        row = [0] * len(towns)
        if i in edges:
            for (dest, num) in edges[i].items():
                row[dest] = num
        table.append(row)
    print table
elif sys.argv[1] == 'csv':
    print 'name,latitude,longitude,population,color'
    print u'\n'.join((u'"{}","{}","{}","{}","#{}"'.format(
                    get_name(t[2]['name']),
                    # t[2]['name'],
                    t[0],
                    t[1],
                    t[3],
                    hashlib.md5(t[2]['name'].encode('utf8')).hexdigest()[:6],
                    ) for t in towns)).encode('utf8')
elif sys.argv[1] == 'flows.csv':
    print 'Origin,Dest,Friends Migrations'
    for i in range(0, len(towns)):
        if i in edges:
            for (dest, num) in edges[i].items():
                if num > 0:
                    print u'"{}","{}",{}'.format(towns[i][2]['name'],
                            towns[dest][2]['name'], num).encode('utf8')
elif sys.argv[1] == 'nodes.csv':
    print 'Code,Name,Lat,Lon'
    for t in towns:
        print u'"{}","{}",{}, {}'.format(t[2]['name'], t[2]['name'], t[0],
                t[1]).encode('utf8')

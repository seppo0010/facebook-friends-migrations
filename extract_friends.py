import json
import re
import subprocess
import sys

if len(sys.argv) != 3:
    print "Usage: {} <data> <curl command>".format(sys.argv[0])
    print "The curl command should look something like `curl https://facebook.com/{}`"
    sys.exit(1)

with open(sys.argv[1]) as fp:
    data = fp.read()

DEV_NULL = open('/dev/null', 'w')
CURL = sys.argv[2]

found = set(re.findall(r"facebook.com\\/(.+?)[\?\\/\"']", data))
found.remove('common')
found.remove('checkpoint')
found.remove('help')
found.remove('ajax')
found.remove('pages')
found.remove('photo.php')

found = found.union(set(re.findall(r"alias\"\:\"(.+?)\"", data)))
data = []
print '['
for friend in found:
    # print "// Fetching {}'s information".format(friend)
    output = subprocess.check_output(CURL.format(friend), shell=True, stderr=DEV_NULL)
    if output.count("Add Friend") > 1:
        # print "// skipping (not a friend)"
        continue

    fdata = {}
    livesin = re.search(r"[lL]ives in <a.+?>(.+?)</a>", output)
    if livesin:
        fdata['current_location'] = {'name': livesin.group(1)}
    isfrom = re.search(r"[fF]rom <a.+?>(.+?)</a>", output)
    if isfrom:
        fdata['hometown_location'] = {'name': isfrom.group(1)}

    if isfrom or livesin:
        data.append(fdata)
        print json.dumps(fdata)
    else:
        # print '// No information found'
        pass
print ']'

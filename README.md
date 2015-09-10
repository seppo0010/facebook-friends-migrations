# Facebook friends migration

Graphicate your Facebook Friends migrations. Where are they from and where they live now.

## Instructions

Extract a list of your friends identifiers by going to
https://facebook.com/<you>/friends, open your developer console, and scroll
all the way down until all your friends are visible. In the console, go
to the Network tab and filter by "AllFriendsApp" or "?filter". Copy all
response body in a temporary file and run "extract-friends.py" using that file
path as an argument. Save that as "friends-nolocation.json".

Run

    python add_locations.py friends-nolocation.json > friends.json
    python adapt.py json > public/d3chord/matrix.json && python adapt.py csv > public/d3chord/cities.csv

Then open public/d3chord/index.html

To get the map run

    python adapt.py flows.csv > public/jflowmap/flows.csv && python adapt.py nodes.csv > public/jflowmap/nodes.csv

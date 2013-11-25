Facebook friends migration
===

Graphicate your Facebook Friends migrations. Where are they from and where they live now.

Instructions
==

Run the following FQL query to get your friends' information. You can run the
query from this URL: https://developers.facebook.com/tools/explorer

    SELECT name, current_location, hometown_location FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())

Save that as "friends.json", and run

    python adapt.py json > public/d3chord/matrix.json && python adapt.py csv > public/d3chord/cities.csv

Then open public/d3chord/index.html

To get the map run

    python adapt.py flows.csv > public/jflowmap/flows.csv && python adapt.py nodes.csv > public/jflowmap/nodes.csv

My Facebook friends migration
===

FQL to get your friends' information:

    SELECT name, current_location, hometown_location FROM user WHERE uid IN (SELECT uid2 FROM friend WHERE uid1 = me())

Save that as "friends.json", and run

    python adapt.py json > public/matrix.json && python adapt.py csv > public/cities.csv

Then in public you should have everything you need.

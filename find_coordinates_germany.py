
import pandas as pd

    
jot_cities = pd.read_json("sf/citiesInJotDataset_germany.json", typ="series")

geonames = csv = pd.read_csv('sf/download.geonames.org-export-dump/DE.txt', sep='\t', header=None)

geoname_cities = []
for i in range(len(geonames)):
    if "P" == geonames.loc[i,6]:
        entry = {"name": geonames.loc[i,2].lower(), "lat": geonames.loc[i,4], "lon":geonames.loc[i,5], "idx": i}
        geoname_cities.append(entry)
    
one_equal_match = 0
several_equal_match = 0    
one_in_match = 0
several_in_match = 0
no_match = 0

print len(geoname_cities)
for jot in range(len(jot_cities)):
    jot_city = jot_cities.loc[jot]
    print jot_city
    found_match = 0
    for geo in range(len(geoname_cities)):
        if jot_city == geoname_cities[geo]["name"]:
            found_match += 1
            print "  EQ: %s 2:%s %f %f" % (jot_city, geoname_cities[geo]["name"], geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
            
    if found_match == 1: one_equal_match += 1
    if found_match > 1:  several_equal_match += 1
    if found_match == 0:           
        for geo in range(len(geoname_cities)):
            if jot_city in geoname_cities[geo]["name"]:
                found_match += 1
                print "    IN: %s 2:%s %f %f %d" % (jot_city, geoname_cities[geo]["name"], geoname_cities[geo]["lat"], geoname_cities[geo]["lon"], geoname_cities[geo]["idx"])
        if found_match == 1: one_in_match += 1
        if found_match > 1:  several_in_match += 1
    
    if found_match == 0:       
        print "  **** Not found"
        no_match += 1

print "one_equal_match %d" % one_equal_match
print "several_equal_match %d" % several_equal_match 
print "one_in_match %d" % one_in_match
print "several_in_match %d" % several_in_match
print "no_match %d" % no_match 


print 'Ending program'




import pandas as pd
import geopy.distance
    
jot_cities = pd.read_json("sf/citiesInJotDataset_germany.json", typ="series")

geonames = pd.read_csv('sf/download.geonames.org-export-dump/DE.txt', sep='\t', header=None)

geoname_cities = []
for i in range(len(geonames)):
    if "P" == geonames.loc[i,6]:
        entry = {"name": geonames.loc[i,2].lower(), "lat": geonames.loc[i,4], "lon":geonames.loc[i,5], "geonameid":geonames.loc[i,0]}
        geoname_cities.append(entry)
    
one_equal_match = 0
several_equal_match = 0    
one_in_match = 0
several_in_match = 0
no_match = 0

f_out= open("match.csv","w+")
#f_out.write('City,Latitude,Longitude\n')

print len(geoname_cities)
print"Matches\tSearch_type\tjot_city\tgeo_name_city\tlat\tlon\tdist_from_first\tgeonameid"
for jot in range(len(jot_cities)):
    jot_city = jot_cities.loc[jot]
    found_match = 0
    matches = []
    for geo in range(len(geoname_cities)):
        if jot_city == geoname_cities[geo]["name"]:
            found_match += 1
            match_coord = (geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
            if found_match == 1:
                first_coord = match_coord
                first_line = "%s,%f,%f\n" % (jot_city, geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
            distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
            s = "EQ:\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_cities[geo]["name"], geoname_cities[geo]["lat"], geoname_cities[geo]["lon"], distance_km, geoname_cities[geo]["geonameid"])
            matches.append(s)
            
    if found_match == 1: 
        one_equal_match += 1
        f_out.write(first_line)
    if found_match > 1:  several_equal_match += 1
    if found_match == 0:           
        for geo in range(len(geoname_cities)):
            if jot_city in geoname_cities[geo]["name"]:
                found_match += 1
                match_coord = (geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
                if found_match == 1:
                    first_coord = match_coord
                    first_line = "%s,%f,%f\n" % (jot_city, geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
                distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                s = "IN:\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_cities[geo]["name"], geoname_cities[geo]["lat"], geoname_cities[geo]["lon"], distance_km, geoname_cities[geo]["geonameid"])
                matches.append(s)
        if found_match == 1: 
            one_in_match += 1
            f_out.write(first_line)
        if found_match > 1:  several_in_match += 1
    
    if found_match == 0:       
        s = "No match: %s" % (jot_city)
        matches.append(s)
        no_match += 1

    for s in matches:
        print "(%d)\t%s" % (found_match, s)

print "one_equal_match %d" % one_equal_match
print "several_equal_match %d" % several_equal_match 
print "one_in_match %d" % one_in_match
print "several_in_match %d" % several_in_match
print "no_match %d" % no_match 


f_out.close()
print 'Ending program'



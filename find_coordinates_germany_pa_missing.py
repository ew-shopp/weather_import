
import pandas as pd
import geopy.distance
    
jot_cities = pd.read_csv("pa_missing.csv", sep=",", header=None)

geonames = pd.read_csv('sf/download.geonames.org-export-dump/DE.txt', sep='\t', header=None)

geoname_cities = []
geoname_region = []
for i in range(len(geonames)):
    entry = {"name": geonames.loc[i,2].lower(), "altname": geonames.loc[i,3].__str__().lower(), "lat": geonames.loc[i,4], "lon":geonames.loc[i,5], "geonameid":geonames.loc[i,0], "featureclass":geonames.loc[i,6]}
    if "P" == geonames.loc[i,6]:
        geoname_cities.append(entry)
    if "A" == geonames.loc[i,6]:
        geoname_region.append(entry)
    
one_equal_region_match = 0
one_equal_city_match = 0
several_equal_city_match = 0    
one_in_match = 0
several_in_match = 0
no_match = 0

f_out_city = open("pa_missing_eq_city_match.csv","w+")
f_out_region = open("pa_missing_eq_region_match.csv","w+")
f_out_missing = open("pa_missing_missing.csv","w+")

print len(geoname_cities)
print"Matches\tSearch_type\tjot_city\tgeo_name_city\tlat\tlon\tdist_from_first\tgeonameid"
for jot in range(len(jot_cities)):
    jot_city = jot_cities.loc[jot,0]
    jot_city_mod = jot_cities.loc[jot,1]
    found_city_match = 0
    found_region_match = 0 
    city_matches = []
    region_matches = []
    final_matches = []
    for geo in range(len(geoname_cities)):
        if jot_city_mod == geoname_cities[geo]["name"]:
            found_city_match += 1
            match_coord = (geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
            if found_city_match == 1:
                first_coord = match_coord
                first_line = "%s,%f,%f\n" % (jot_city, geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
            distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
            s = "EQ:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_cities[geo]["featureclass"], geoname_cities[geo]["name"], geoname_cities[geo]["lat"], geoname_cities[geo]["lon"], distance_km, geoname_cities[geo]["geonameid"])
            city_matches.append(s)
            
    if found_city_match == 1: 
        one_equal_city_match += 1
        final_matches += city_matches
        f_out_city.write(first_line)
    if found_city_match > 1:  
        for geo in range(len(geoname_region)):
            if jot_city_mod == geoname_region[geo]["name"]:
                found_region_match += 1
                match_coord = (geoname_region[geo]["lat"], geoname_region[geo]["lon"])
                distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                s = "EQ:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_region[geo]["featureclass"], geoname_region[geo]["name"], geoname_region[geo]["lat"], geoname_region[geo]["lon"], distance_km, geoname_region[geo]["geonameid"])
                region_matches.append(s)
        if found_region_match == 1: 
            one_equal_region_match += 1
            final_matches += region_matches
            f_out_region.write(first_line)
        else:  
            several_equal_city_match += 1
            final_matches += city_matches
            final_matches += region_matches
                
    if found_city_match == 0:          
        for geo in range(len(geoname_cities)):
            if jot_city_mod in geoname_cities[geo]["name"] or jot_city_mod in geoname_cities[geo]["altname"]:
                found_city_match += 1
                match_coord = (geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
                if found_city_match == 1:
                    first_coord = match_coord
                    first_line = "%s,%f,%f\n" % (jot_city, geoname_cities[geo]["lat"], geoname_cities[geo]["lon"])
                distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                s = "IN:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_cities[geo]["featureclass"], geoname_cities[geo]["name"], geoname_cities[geo]["lat"], geoname_cities[geo]["lon"], distance_km, geoname_cities[geo]["geonameid"])
                city_matches.append(s)
        if found_city_match == 1: 
            one_in_match += 1
            final_matches += city_matches
            f_out_city.write(first_line)
        if found_city_match > 1:  
            for geo in range(len(geoname_region)):
                if jot_city_mod == geoname_region[geo]["name"]:
                    found_region_match += 1
                    match_coord = (geoname_region[geo]["lat"], geoname_region[geo]["lon"])
                    distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                    s = "IN:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_region[geo]["featureclass"], geoname_region[geo]["name"], geoname_region[geo]["lat"], geoname_region[geo]["lon"], distance_km, geoname_region[geo]["geonameid"])
                    region_matches.append(s)
                if jot_city_mod in geoname_region[geo]["altname"]:
                    found_region_match += 1
                    match_coord = (geoname_region[geo]["lat"], geoname_region[geo]["lon"])
                    distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                    s = "IN:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_region[geo]["featureclass"], geoname_region[geo]["name"], geoname_region[geo]["lat"], geoname_region[geo]["lon"], distance_km, geoname_region[geo]["geonameid"])
                    region_matches.append(s)
            if found_region_match == 1: 
                one_equal_region_match += 1
                final_matches += region_matches
                f_out_region.write(first_line)
            else:  
                several_in_match += 1
                final_matches += city_matches
                final_matches += region_matches


            
    
    if found_city_match == 0:      
        s = "No match: %s" % (jot_city)
        city_matches.append(s)
        for geo in range(len(geoname_region)):
            if jot_city_mod == geoname_region[geo]["name"]:
                found_region_match += 1
                match_coord = (geoname_region[geo]["lat"], geoname_region[geo]["lon"])
                distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                s = "No match:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_region[geo]["featureclass"], geoname_region[geo]["name"], geoname_region[geo]["lat"], geoname_region[geo]["lon"], distance_km, geoname_region[geo]["geonameid"])
                region_matches.append(s)
            if jot_city_mod in geoname_region[geo]["altname"]:
                found_region_match += 1
                match_coord = (geoname_region[geo]["lat"], geoname_region[geo]["lon"])
                distance_km = geopy.distance.vincenty(first_coord, match_coord).km    
                s = "No match:\t%s\t%s\t%s\t%f\t%f\t%fkm\t%d" % (jot_city, geoname_region[geo]["featureclass"], geoname_region[geo]["name"], geoname_region[geo]["lat"], geoname_region[geo]["lon"], distance_km, geoname_region[geo]["geonameid"])
                region_matches.append(s)

        if found_region_match == 1: 
            one_equal_region_match += 1
            final_matches += region_matches
            f_out_region.write(first_line)
        else:  
            no_match += 1
            final_matches += city_matches
            final_matches += region_matches
            f_out_missing.write("%s,%s\n" % (jot_city, jot_city_mod))




    for s in final_matches:
        print "(%d)<%d>\t%s" % (found_city_match, found_region_match, s)

print "one_equal_city_match %d" % one_equal_city_match
print "several_equal_city_match %d" % several_equal_city_match 
print "one_in_match %d" % one_in_match
print "several_in_match %d" % several_in_match
print "no_match %d" % no_match 
print "one_equal_region_match %d" % one_equal_region_match


f_out_city.close()
f_out_region.close()
print 'Ending program'



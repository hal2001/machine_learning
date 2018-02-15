# -*- coding: utf-8 -*-
"""
Parses "Location History" (aka Timeline) from Google to enable importing to QGIS

Author: Aaron Penne

Reference: https://developers.google.com/kml/documentation/kmlreference

Example input Location History kml:
    <?xml version='1.0' encoding='UTF-8'?>
    <kml xmlns='http://www.opengis.net/kml/2.2' xmlns:gx='http://www.google.com/kml/ext/2.2'>
    	<Document>
    		<Placemark>
    			<open>1</open>
    			<gx:Track>
    				<altitudeMode>clampToGround</altitudeMode>
    				<when>2018-02-15T15:55:36Z</when>
    				<gx:coord>-130.1575804 25.7754855 9</gx:coord>
    				<when>2017-04-16T01:27:45Z</when>
    				<gx:coord>-120.15754439999999 10.7894186 0</gx:coord>
    				<when>2016-10-16T01:27:45Z</when>
    				<gx:coord>-100.15754439999999 45.7894186 0</gx:coord>
    			</gx:Track>
    		</Placemark>
    	</Document>
    </kml>
    
Example output:
    -130.1575804    25.7754855
    -120.15754439999999    10.7894186
    -100.15754439999999    45.7894186
"""

import re

# Hard coded file names for now
my_path = "C:/tmp/"
file_in = my_path + "Location History.kml"
file_out = my_path + "Location_History.txt"

# Open file with correct encoding
with open(file_in, "r", encoding="utf8") as f_in:
    with open(file_out, "w+", encoding="utf8") as f_out:
        f_out.write("{0}\t{1}\n".format("lon_x", "lat_y"))
        for line in f_in:
            match = re.findall(r'<gx:coord>(.*)</gx:coord>', line)
            if match:
                lon = match[0].split(' ')[0]
                lat = match[0].split(' ')[1]
                f_out.write("{0}\t{1}\n".format(lon, lat))
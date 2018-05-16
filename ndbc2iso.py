
from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
import csv
from csv import Dialect
from jinja2 import Environment, FileSystemLoader
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from dateparser.date import DateDataParser
import urllib2
import uuid
import ssl

def main():
    files = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\ndbc\\ndbc_historical_files.csv')
    stationList={}
    for f in files:
        station = f['Station']
        identifer = f['Filename']
        #fo = {identifer:f}
        if (stationList.has_key(station)):
            stationList[station].append(f)
        else:
            stationList[station] =[f]





    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    data = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\ndbc\\ndbc_historical.csv')
    base_path = './output/ndbc'
    base_name = "ndbc"
    template = cvs2meta.load_template('ndbc_metadata19115.xml',base_bath='./templates')

    #cvs2meta.render_output(out,template,'StationID_good', base_path="output/ndbc",base_name="ndbc")


    try:
        os.stat(base_path)
    except:
        os.mkdir(base_path)

    i = 0
    for d in data:
        template_values = {
            'row': d
            }
        if ( d['Metadata'].find("by") ):
             d["Organization"] = d['Metadata'].rsplit('by')[1]
        else:
            d["Organization"] = d['Metadata']

        fileList = stationList[station]

        if (  d['coords'].find('N/A') ==0 ):
            d['location'] = 'none'
        else:
            northI = d['coords'].find('N')
            southI = d['coords'].find('S')
            eastI = d['coords'].find('E')
            westI = d['coords'].find('W')
            if (southI > 0):
                latI = d['coords'].index('S')
                lat = '-' + d['coords'][:southI].strip()

            else:
                latI = d['coords'].index('N')
                lat = d['coords'][:northI].strip()

            if (westI > 0):
                lonI  = d['coords'].index('W')
                lon = '-' + d['coords'][latI+1:lonI].strip()
            else:
                lonI = d['coords'].index('E')
                lon = d['coords'][latI+1:lonI].strip()

            d["lat"] = lat
            d['lon'] = lon

        fileList = stationList[station]

        keywords = {}
        for fl in fileList:
            if (fl['folder'] == 'adcp'):
                keywords['adcp'] = 'Ocean Current Data.'
            if (fl['folder'] == 'adcp2'):
                keywords['adcp2'] = 'Ocean Current Data.'
            if (fl['folder'] == 'cwind'):
                keywords['cwind'] = 'Continuous Winds.'
            if (fl['folder'] == 'dart'):
                keywords['dart'] = 'DART (Tsunameters) Measurements. '
            if (fl['folder'] == 'mmbcur'):
                keywords['mmbcur'] = 'Marsh-McBirney Current Measurements.'
            if (fl['folder'] == 'ocean'):
                keywords['ocean'] = 'Oceanographic Data..'
            if (fl['folder'] == 'rain'):
                keywords['rain'] = 'Hourly Rain Accumulation'
            if (fl['folder'] == 'rain10'):
                keywords['rain10'] = '10-Minute Rain Rate.'
            if (fl['folder'] == 'rain24'):
                keywords['rain24'] = 'Percent Time Raining in 24-Hour Period Percentage .'
            if (fl['folder'] == 'srad'):
                keywords['srad'] = 'Solar Radiation Data. '
            if (fl['folder'] == 'supl'):
                keywords['supl'] = 'Supplemental Measurements Data. '

            if (fl['folder'] == 'swden'):
                keywords['swden'] = 'Spectral Wave Data. Spectral wave density'
            if (fl['folder'] == 'swdir'):
                keywords['swdir'] = 'Spectral Wave Data. Spectral wave direction '
            if (fl['folder'] == 'swdir2'):
                keywords['swdir2'] = 'Spectral Wave Data. Spectral wave direction '
            if (fl['folder'] == 'swr1'):
                keywords['swr1'] = 'Spectral Wave Data.  '
            if (fl['folder'] == 'swr2'):
                keywords['swr2'] = 'Spectral Wave Data.  '
            if (fl['folder'] == 'wlevel'):
                keywords['wlevel'] = 'Water Level.'


        try:
            #out = render_template(template_values, template)
            # need a remove bad XML chars from the row: https://gist.github.com/lawlesst/4110923
            #out = cvs2meta.render_template(d, template)
            ddp = DateDataParser()
            allKW = keywords.values() + keywords.keys()
            out = template.render(row=d, ddp=ddp, uuid=lambda b: cvs2meta.url2uuid(b),
                                   datetimefmt=lambda b: cvs2meta.datetimeformat(b)
                                  ,fileList=fileList, keywords=allKW)

            # d[id_field]) inlcudes colons... so bad filenames
            #f_out = open(base_path+"/%s_%s.xml" % (base_name , d[id_field]) , "w")
            f_out = open(base_path+"/%s_%s.xml" % (base_name , i) , "w")
            i +=1
            f_out.write(out)
            f_out.close()
        except Exception  as err:
            print ("exception: ",  err)
            print "row failed:" + str(d)

if __name__ == "__main__":
    main()
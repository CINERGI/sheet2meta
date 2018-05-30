
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
        instr = {}
        instr['adcp']= u"Ocean Current Data. DEP01,DEP02,... The distance from the sea surface to the middle of the depth cells, or bins, measured in meters. DIR01,DIR02,... The direction the ocean current is flowing toward. 0-360 degrees, 360 is due north, 0 means no measurable current. SPD01,SPD02,... The speed of the ocean current measured in cm/s."
        instr[
            'adcp2']=u"Ocean Current Data (Expanded ADCP format). Instrument Number Stations may have more than one ADCP instrument. This field distinguishes these instruments by number. Valid values are 0-9, with 0 being reserved for surface measurements. Bin The bin number, ranging from 1 to 128, where 1 is the bin closest to the transducer head. Depth The distance from the sea surface to the middle of the depth cells, or bins, measured in meters. Dir The direction the ocean current is flowing toward. 0-360 degrees, 360 is due north, 0 means no measurable current. Speed The speed of the ocean current measured in cm/s. ErrVl The error velocity measured in cm/s. VerVl The vertical velocity of the ocean current measured in cm/s. %Good3 The percentage of three-beam solutions that are good. %Good4 The percentage of four-beam solutions that are good. %GoodE The percentage of transformations rejected. EI1,EI2,EI3,EI4 The echo intensity values for the four beams. Valid values are 0 to 255. EI1 = Echo Intensity for beam #1; EI2 = Echo Intensity for beam #1; EI3 = Echo Intensity for beam #3; and EI4 = Echo Intensity for beam #4. CM1,CM2,CM3,CM4 The correlation magnitude values for the four beams. Valid values are 0 to 255. CM1 = Correlation Magnitude for beam #1; CM2 = Correlation Magnitude for beam #1; CM3 = Correlation Magnitude for beam #3; and CM4 = Correlation Magnitude for beam #4. Flags The nine quality flags represent the results of the following quality tests based on their position in the flags field.  Flag 1 represents the overall bin status. Flag 2 represents the ADCP Built-In Test (BIT) status. Flag 3 represents the Error Velocity test status. Flag 4 represents the Percent Good test status. Flag 5 represents the Correlation Magnitude test status. Flag 6 represents the Vertical Velocity test status. Flag 7 represents the North Horizontal Velocity test status. Flag 8 represents the East Horizontal Velocity test status. Flag 9 represents the Echo Intensity test status."
        instr[
            'cwind']= u"Continuous Winds. WDIR Ten-minute average wind direction measurements in degrees clockwise from true North. (DIR in Historical files) WSPD Ten-minute average wind speed values in m/s. (SPD in Historical files) GDR Direction, in degrees clockwise from true North, of the GST, reported at the last hourly 10-minute segment. GST Maximum 5-second peak gust during the measurement hour, reported at the last hourly 10-minute segment. GTIME The minute of the hour that the GSP occurred, reported at the last hourly 10-minute segment."
        instr[
            'dart']= u"DART (Tsunameters) Measurements. T (TYPE) Measurement Type: 1 = 15-minute measurement; 2 = 1-minute measurement; and 3 = 15-second measurement. HEIGHT Height of water column in meters. tt = Tsunami Trigger Time, see the Tsunami Detection Algorithm ts = data Time Stamp(s)"
        instr[
            'mmbcur']= u"Marsh-McBirney Current Measurements. DIR Direction the current is flowing TOWARDS, measured in degrees clockwise from North. SPD Current speed in cm/s."
        instr[
            'ocean']=  u"Oceanographic Data. Depth (DEPTH) Depth (meters) at which measurements are taken. Ocean Temperature (OTMP) The direct measurement (Celsius) of the Ocean Temperature (as opposed to the indirect measurement (see WTMP above)). Conductivity (COND) Conductivity is a measure of the electrical conductivity properties of seawater in milliSiemens per centimeter. Salinity (SAL) Salinity is computed by a known functional relationship between the measured electrical conductivity of seawater (CON), temperature (OTMP) and pressure. Salinity is computed using the Practical Salinity Scale of 1978 (PSS78) and reported in Practical Salinity Units. Oxygen Concentration (O2%) Dissolved oxygen as a percentage. Oxygen Concentration (O2PPM) Dissolved oxygen in parts per million. Chlorophyll Concentration (CLCON) Chlorophyll concentration in micrograms per liter (ug/l). Turbidity (TURB) Turbidity is an expression of the optical property that causes light to be scattered and absorbed rather than transmitted in straight lines through the sample (APHA 1980). Units are Formazine Turbidity Units (FTU). pH (PH) A measure of the acidity or alkalinity of the seawater. Eh (EH) Redox (oxidation and reduction) potential of seawater in millivolts."
        instr[
            'rain']=  u"10-Minute Rain Rate Rain rate in units of millimeters per hour on station over the 10-minute period from 5 minutes before to 4 minutes 59.99 seconds after the time with which it is associated. Hourly Rain Accumulation Total accumulation of precipitation in units of millimeters on station during the 60-minute period from minute 0 to minute 59:59.99 of the hour. 24-Hour Rain Rate Average precipitation rate in units of millimeters per hour over 24-hour period from 00:00 to 23:59.99 GMT. Percent Time Raining in 24-Hour Period Percentage of 144 ten-minute periods within a 24 hour period with a measurable accumulation of precipitation."
        instr[
            'rain10']= u"10-Minute Rain Rate Rain rate in units of millimeters per hour on station over the 10-minute period from 5 minutes before to 4 minutes 59.99 seconds after the time with which it is associated. Hourly Rain Accumulation Total accumulation of precipitation in units of millimeters on station during the 60-minute period from minute 0 to minute 59:59.99 of the hour. 24-Hour Rain Rate Average precipitation rate in units of millimeters per hour over 24-hour period from 00:00 to 23:59.99 GMT. Percent Time Raining in 24-Hour Period Percentage of 144 ten-minute periods within a 24 hour period with a measurable accumulation of precipitation."
        instr[
            'rain24']= u"10-Minute Rain Rate Rain rate in units of millimeters per hour on station over the 10-minute period from 5 minutes before to 4 minutes 59.99 seconds after the time with which it is associated. Hourly Rain Accumulation Total accumulation of precipitation in units of millimeters on station during the 60-minute period from minute 0 to minute 59:59.99 of the hour. 24-Hour Rain Rate Average precipitation rate in units of millimeters per hour over 24-hour period from 00:00 to 23:59.99 GMT. Percent Time Raining in 24-Hour Period Percentage of 144 ten-minute periods within a 24 hour period with a measurable accumulation of precipitation."
        instr[
            'srad']=  u"Solar Radiation Data. Shortwave Radiation (SRAD1, SWRAD) Average shortwave radiation in watts per square meter for the preceding hour. Sample frequency is 2 times per second (2 Hz). If present, SRAD1 is from a LI-COR LI-200 pyranometer sensor, and SWRAD is from an Eppley PSP Precision Spectral Pyranometer. Longwave Radiation (LWRAD) Average downwelling longwave radiation in watts per square meter for the preceding hour. Sample frequency is 2 times per second (2 Hz). If present, LWRAD is from an Eppley PIR Precision Infrared Radiometer."
        instr[
            'stdmet']=  u"WDIR Wind direction (the direction the wind is coming from in degrees clockwise from true N) during the same period used for WSPD. See Wind Averaging Methods WSPD Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for land stations. Reported Hourly. See Wind Averaging Methods. GST Peak 5 or 8 second gust speed (m/s) measured during the eight-minute or two-minute period. The 5 or 8 second period can be determined by payload, See the Sensor Reporting, Sampling, and Accuracy section. WVHT Significant wave height (meters) is calculated as the average of the highest one-third of all of the wave heights during the 20-minute sampling period. See the Wave Measurements section. DPD Dominant wave period (seconds) is the period with the maximum wave energy. See the Wave Measurements section. APD Average wave period (seconds) of all waves during the 20-minute period. See the Wave Measurements section. MWD The direction from which the waves at the dominant period (DPD) are coming. The units are degrees from true North, increasing clockwise, with North as 0 (zero) degrees and East as 90 degrees. See the Wave Measurements section. PRES Sea level pressure (hPa). For C-MAN sites and Great Lakes buoys, the recorded pressure is reduced to sea level using the method described in NWS Technical Procedures Bulletin 291 (11/14/80). ( labeled BAR in Historical files) ATMP Air temperature (Celsius). For sensor heights on buoys, see Hull Descriptions. For sensor heights at C-MAN stations, see C-MAN Sensor Locations WTMP Sea surface temperature (Celsius). For buoys the depth is referenced to the hull's waterline. For fixed platforms it varies with tide, but is referenced to, or near Mean Lower Low Water (MLLW). HEAT For more information on heat index, please see the NWS Heat Wave page. CHILL Please note that NDBC uses unadjusted winds to calculate wind chill. The winds are calculated at anemometer height. For more information on wind chill, please see the NWS Wind Chill Temperature Index. ICE Estimated ice accretion in inches per hour based on an algorithm developed by Overland and Pease at the Pacific Marine Environmental Laboratory in the mid-1980s. The algorithm relates icing to the presently observed wind speed, air temperature, and sea surface temperature. The method is designed for trawlers in the 20 to 75 meter length range, underway at normal speeds in open seas and not heading downwind. In general, NWS forecasters translate ice accretion rates to the following categories: light: 0.0 to 0.24 inches of ice accretion/hour; moderate: 0.25 to 0.8 inches/hour; and heavy: greater than 0.8 inches/hour. WSPD10 The estimation of Wind Speed (WSPD) measurement raised or lowered to a height of 10 meters. NDBC uses the method of Liu et al., 1979: Bulk parameterization of air-sea exchanges in heat and water vapor including molecular constraints at the interface, Journal of Atmospheric Science, 36, pp. 1722-1735. WSPD20 The estimation of Wind Speed (WSPD) measurement raised or lowered to a height of 20 meters. NDBC uses the method of Liu et al., 1979: Bulk parameterization of air-sea exchanges in heat and water vapor including molecular constraints at the interface, Journal of Atmospheric Science, 36, pp. 1722-1735. DEWP Dewpoint temperature taken at the same height as the air temperature measurement. VIS Station visibility (nautical miles). Note that buoy stations are limited to reports from 0 to 1.6 nmi. PTDY Pressure Tendency is the direction (plus or minus) and the amount of pressure change (hPa)for a three hour period ending at the time of observation. (not in Historical files) TIDE The water level in feet above or below Mean Lower Low Water (MLLW)."
        instr['supl']=  u"Supplemental Measurements Data. Lowest 1 minute pressure Lowest recorded atmospheric pressure for the hour to the nearest 0.1 hPa and the time at which it occurred (hour and minute). Highest 1 minute wind speed Highest recorded wind speed for the hour to the nearest 0.1 m/s, its corresponding direction to the nearest degree, and the time at which it occurred (hour and minute). WDIR Wind direction (the direction the wind is coming from in degrees clockwise from true N) during the same period used for WSPD. See Wind Averaging Methods WSPD Wind speed (m/s) averaged over an eight-minute period for buoys and a two-minute period for land stations. Reported Hourly. See Wind Averaging Methods."
        instr['swden']=  u"Spectral Wave Data.Sep_Freq The Separation Frequency is the frequency that separates wind waves (WWH, WWP, WWD) from swell waves (SWH, SWP,SWD). NDBC inserts the value 9.999 if Sep_Freq is missing. Spectral wave density Energy in (meter*meter)/Hz, for each frequency bin (typically from 0.03 Hz to 0.40 Hz). Spectral wave direction Mean wave direction, in degrees from true North, for each frequency bin. A list of directional stations is available. Directional Wave Spectrum = C11(f) * D(f,A), f=frequency (Hz), A=Azimuth angle measured clockwise from true North to the direction wave is from. D(f,A) = (1/PI)*(0.5+R1*COS(A-ALPHA1)+R2*COS(2*(A-ALPHA2))). R1 and R2 are the first and second normalized polar coordinates of the Fourier coefficients and are nondimensional. ALPHA1 and ALPHA2 are respectively mean and principal wave directions."
        instr['swdir']=  u"Spectral Wave Data.Sep_Freq The Separation Frequency is the frequency that separates wind waves (WWH, WWP, WWD) from swell waves (SWH, SWP,SWD). NDBC inserts the value 9.999 if Sep_Freq is missing. Spectral wave density Energy in (meter*meter)/Hz, for each frequency bin (typically from 0.03 Hz to 0.40 Hz). Spectral wave direction Mean wave direction, in degrees from true North, for each frequency bin. A list of directional stations is available. Directional Wave Spectrum = C11(f) * D(f,A), f=frequency (Hz), A=Azimuth angle measured clockwise from true North to the direction wave is from.D(f,A) = (1/PI)*(0.5+R1*COS(A-ALPHA1)+R2*COS(2*(A-ALPHA2))). R1 and R2 are the first and second normalized polar coordinates of the Fourier coefficients and are nondimensional. ALPHA1 and ALPHA2 are respectively mean and principal wave directions."
        instr['swdir2']=  u"Spectral Wave Data.Sep_Freq The Separation Frequency is the frequency that separates wind waves (WWH, WWP, WWD) from swell waves (SWH, SWP,SWD). NDBC inserts the value 9.999 if Sep_Freq is missing. Spectral wave density Energy in (meter*meter)/Hz, for each frequency bin (typically from 0.03 Hz to 0.40 Hz). Spectral wave direction Mean wave direction, in degrees from true North, for each frequency bin. A list of directional stations is available. Directional Wave Spectrum = C11(f) * D(f,A), f=frequency (Hz), A=Azimuth angle measured clockwise from true North to the direction wave is from.D(f,A) = (1/PI)*(0.5+R1*COS(A-ALPHA1)+R2*COS(2*(A-ALPHA2))). R1 and R2 are the first and second normalized polar coordinates of the Fourier coefficients and are nondimensional. ALPHA1 and ALPHA2 are respectively mean and principal wave directions."
        instr['swr1']=  u"Spectral Wave Data.Sep_Freq The Separation Frequency is the frequency that separates wind waves (WWH, WWP, WWD) from swell waves (SWH, SWP,SWD). NDBC inserts the value 9.999 if Sep_Freq is missing. Spectral wave density Energy in (meter*meter)/Hz, for each frequency bin (typically from 0.03 Hz to 0.40 Hz). Spectral wave direction Mean wave direction, in degrees from true North, for each frequency bin. A list of directional stations is available. Directional Wave Spectrum = C11(f) * D(f,A), f=frequency (Hz), A=Azimuth angle measured clockwise from true North to the direction wave is from.D(f,A) = (1/PI)*(0.5+R1*COS(A-ALPHA1)+R2*COS(2*(A-ALPHA2))). R1 and R2 are the first and second normalized polar coordinates of the Fourier coefficients and are nondimensional. ALPHA1 and ALPHA2 are respectively mean and principal wave directions."
        instr['swr2']= u"Spectral Wave Data.Sep_Freq The Separation Frequency is the frequency that separates wind waves (WWH, WWP, WWD) from swell waves (SWH, SWP,SWD). NDBC inserts the value 9.999 if Sep_Freq is missing. Spectral wave density Energy in (meter*meter)/Hz, for each frequency bin (typically from 0.03 Hz to 0.40 Hz). Spectral wave direction Mean wave direction, in degrees from true North, for each frequency bin. A list of directional stations is available. Directional Wave Spectrum = C11(f) * D(f,A), f=frequency (Hz), A=Azimuth angle measured clockwise from true North to the direction wave is from. D(f,A) = (1/PI)*(0.5+R1*COS(A-ALPHA1)+R2*COS(2*(A-ALPHA2))). R1 and R2 are the first and second normalized polar coordinates of the Fourier coefficients and are nondimensional. ALPHA1 and ALPHA2 are respectively mean and principal wave directions."
        instr['wlevel']=  u"Water Level. TG01, TG02,...,TG10 Six-minute water levels representing the height, in feet, of the water above or below Mean Lower Low Water (MLLW), offset by 10 ft. to prevent negative values. Please subtract 10 ft. from every value to obtain the true water level value, in reference to MLLW."

        abstract = 'Site '+ d['StationID_good'] +' from National Data Buoy Center. Station Managed by '+\
                   d['Metadata'] +'\n Abstract enhanced with instrument information:\n'
        for a  in keywords.keys():
            if instr.has_key(a):
                try:
                    abstract += instr[a] +'\n'
                except Exception  as err:
                    print ("exception: ", err)
        d['abstract']= abstract
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
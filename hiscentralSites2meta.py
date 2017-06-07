__author__ = 'valentin'

import sys
import suds
from suds.client import Client
import ulmo.cuahsi.his_central as his
import ulmo.util as util

from ulmo.cuahsi.his_central import core

from resource import cvs2meta

reload(sys)
sys.setdefaultencoding('utf-8')
import os
from dateparser.date import DateDataParser

HIS_CENTRAL_WSDL_URL = 'http://hiscentral.cuahsi.org/webservices/hiscentral.asmx?WSDL'

# {'abstract': "The goal of NLDAS is to construct quality-controlled, and spatially and "
#              " 'service_description_url': 'http://hiscentral.cuahsi.org/pub_network.aspx?n=274',
#  'organization_website': 'http://disc.sci.gsfc.nasa.gov/hydrology/data-holdings',
#  'service_status': None,
#  'variable_count': 5,
#  'network_name': 'NLDAS_NOAH',
#  'min_x': -124.9375,
# 'min_y': 25.0625,
#  'title': 'NLDAS Hourly NOAH Data',
#  'value_count': 2147483647,
#  'service_url': 'http://hydro1.sci.gsfc.nasa.gov/daac-bin/his/1.0/NLDAS_NOAH_002.cgi?WSDL',
#  'site_count': 103936,
#  'email': 'gsfc-help-disc@lists.nasa.gov',
#  'max_x': -67.0625, 'max_y': 52.9375,
#  'citation': 'Mitchell, K.E., D. Lohmann, P.R. Houser, E.F. Wood, J.C. Schaake, A. Robock, B.A. Cosgrove, J. Sheffield, Q. Duan, L. Luo, R.W. Higgins, R.T. Pinker, J.D. Tarpley, D.P. Lettenmaier, C.H. Marshall, J.K. Entin, M. Pan, W. Shi, V. Koren, J. Meng, B. H. Ramsay, and A.A. Bailey (2004), The multi-institution North American Land Data Assimilation System (NLDAS): Utilizing multiple GCIP products and partners in a continental distributed hydrological modeling system, J. Geophys. Res., 109, D07S90, doi:10.1029/2003JD003823.',
#  'phone': '301-614-5224',
#  'service_id': 274,
#  'organization': 'NASA Goddard Earth Sciences (GES) Data and Information Services Center'}
def main():
    suds_client = suds.client.Client(HIS_CENTRAL_WSDL_URL)
#           GetSeriesCatalogForBox2(xs:double xmin, xs:double xmax, xs:double ymin, xs:double ymax, xs:string conceptKeyword, xs:string networkIDs, xs:string beginDate, xs:string endDate)
    bbox = [-94, 28, -89, 34]
   # bbox = [-90, 33, -89, 34]

    if bbox is None:
        exit()
    else:
        x_min, y_min, x_max, y_max = bbox
        series = suds_client.service.GetSeriesCatalogForBox2(
            xmin=x_min,  xmax=x_max,ymin=y_min, ymax=y_max,
            conceptKeyword="", networkIDs="",
            beginDate="01/01/2000",endDate="01/01/2017")
        #GetSitesInBox2(xs:double xmin, xs:double xmax, xs:double ymin, xs:double ymax, xs:string conceptKeyword, xs:string networkIDs, )
    services = suds_client.service.GetWaterOneFlowServiceInfo()
    # an array is fine. not using it to find anything
    series = [
         _series_dict(series_info)
        for series_info in series.SeriesRecord
        ]

    print len(series)
    services = {
        service_info.NetworkName: core._service_dict(service_info)
        for service_info in services.ServiceInfo
        }
    print list(services.keys())

    #wof_vars = wof.get_variable_info(  out[0]['service_url'] )
    #print wof_vars
    template = cvs2meta.load_template('hiscentral_series19115.xml',base_bath='./templates')
    id_field = 'network_name'
    base_path="output/his_series"
    base_name="ddh_series"

    try:
        os.stat(base_path)
    except:
        os.mkdir(base_path)

    i = 0
    for d in series:

        try:
            #out = render_template(template_values, template)
            ddp = DateDataParser()
          #  if (d['end_date']):
          #      end_date = ddp.getDateData(d['end_date']).date()
            service_info = services[d['serv_code']]
            seriesCode = "HISSeries_%s__%s__%s__%s"% (d['serv_code'], d['location'] , d['var_code'], d['datatype'])
            out = template.render(row=d, ddp=ddp, service_info=service_info, seriesCode=seriesCode)
            # d[id_field]) inlcudes colons... so bad filenames
            #f_out = open(base_path+"/%s_%s.xml" % (base_name , d[id_field]) , "w")
            f_out = open(base_path+"/%s_%s.xml" % (base_name , i) , "w")
            i +=1
            f_out.write(out)
            f_out.close()
        except:
            e = sys.exc_info()[0]
            print  e
            print "row failed:" + str(d)



def _series_dict(series_info):
    """converts a ServiceInfo etree object into a service info dict"""
    change_keys = [
        #(old_key, new_key)
        ('aabstract', 'abstract'),
        ('maxx', 'max_x'),
        ('maxy', 'max_y'),
        ('minx', 'min_x'),
        ('miny', 'min_y'),
        ('orgwebsite', 'organization_website'),
        ('serv_url', 'service_url'),
        ('sitecount', 'site_count'),
        ('valuecount', 'value_count'),
        ('variablecount', 'variable_count'),
    ]

    series_dict = dict([
        (util.camel_to_underscore(key), core._cast_if_text(value))
        for key, value in dict(series_info).iteritems()
    ])

    for old_key, new_key in change_keys:
        if old_key in series_dict:
            series_dict[new_key] = series_dict[old_key]
            del series_dict[old_key]

    return series_dict

if __name__ == "__main__":
    main()
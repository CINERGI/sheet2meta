__author__ = 'valentin'

import sys

import ulmo.cuahsi.his_central as his

import ulmo.cuahsi.wof as wof

from resource import cvs2meta

reload(sys)
sys.setdefaultencoding('utf-8')
import os
from dateparser.date import DateDataParser



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

    services = his.get_services()
    #wof_vars = wof.get_variable_info(  out[0]['service_url'] )
    #print wof_vars
    template = cvs2meta.load_template('hiscentral_metadata19115.xml',base_bath='./templates')
    id_field = 'network_name'
    base_path="output/cuahsi"
    base_name="cuahsi"

    try:
        os.stat(base_path)
    except:
        os.mkdir(base_path)

    i = 0
    for d in services:

        try:
            #out = render_template(template_values, template)
            ddp = DateDataParser()
            service_variables = []
            wof_vars = wof.get_variable_info(  d['service_url'] )
            for sv  in wof_vars.items():
                vname= sv[1]['name']
                service_variables.append(vname)
            out = template.render(row=d, ddp=ddp, wof_vars=service_variables)
            # d[id_field]) inlcudes colons... so bad filenames
            #f_out = open(base_path+"/%s_%s.xml" % (base_name , d[id_field]) , "w")
            f_out = open(base_path+"/%s_%s.xml" % (base_name , i) , "w")
            i +=1
            f_out.write(out)
            f_out.close()
        except:
            print "row failed:" + str(d)

if __name__ == "__main__":
    main()
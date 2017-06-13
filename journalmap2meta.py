__author__ = 'valentin'

import sys

import ulmo.cuahsi.his_central as his

import ulmo.cuahsi.wof as wof

from resource import cvs2meta

reload(sys)
sys.setdefaultencoding('utf-8')
import os
from dateparser.date import DateDataParser
import ssl
import urllib2
import uuid
import json
import time

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

    #baseurl = "https://www.journalmap.org/api/articles.json?key=QLT-2Xqqorgxhz3pF_cN&page=%s"
    search_url = "https://www.journalmap.org/articles/search?key=QLT-2Xqqorgxhz3pF_cN&page=%s"
    article_url =  "https://www.journalmap.org/api/articles/%s.json?key=QLT-2Xqqorgxhz3pF_cN"
    #wof_vars = wof.get_variable_info(  out[0]['service_url'] )
    #print wof_vars
    template = cvs2meta.load_template('journalmap_metadata19115.xml',base_bath='./templates')
    id_field = 'if'
    base_path="output/journalmap"
    base_name="journalmap"

    try:
        os.stat(base_path)
    except:
        os.mkdir(base_path)
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.options &= ~ssl.OP_NO_SSLv3



    i = 1
    max_pages = 1000000
    while i < max_pages:
        try:
            url_search=   search_url % i
            resp =  urllib2.urlopen(url_search, context=context)
            search = json.load(resp)
            max_pages = search['meta']['total_pages']
            if (i > max_pages):
                exit(0)
            articles = search['articles']
            #out = render_template(template_values, template)
            ddp = DateDataParser()

            for a  in articles:
                try:
                    url_article = article_url % a['id']
                    resp = urllib2.urlopen(url_article, context=context)
                    an_article = json.load(resp)
                except urllib2.HTTPError as ex:
                    if (ex.code == 403):
                        print "403 article id:" +str(a['id']) +" page:"+ str(i)+ ex.msg
                        time.sleep(30)
                    elif (ex.code == 500):
                        print "500 article: " +str(a['id']) +" page:"+ str(i)+ ex.msg
                    else:
                        print "http error article:"  +str(a['id'])  +" page:"+ str(i)+ ex.message

                if an_article['authors']:
                    authors= an_article['authors']
                if an_article['locations']:
                    locations=an_article['locations']
                try:
                    out = template.render(a=a, authors=authors,locations=locations, article=an_article, ddp=ddp)
                    # d[id_field]) inlcudes colons... so bad filenames
                    #f_out = open(base_path+"/%s_%s.xml" % (base_name , d[id_field]) , "w")
                    f_out = open(base_path+"/%s_%s.xml" % (base_name , a["id"]) , "w")

                    f_out.write(out)
                    f_out.close()
                except Exception as ex:
                    print "error in template article id: " + str(a["id"])
                time.sleep(0.25)

            i += 1
            time.sleep(1)
        except urllib2.HTTPError as ex:
            if (ex.code == 403):
                print "403 search: "+" page:"+ str(i) + ex.msg
                time.sleep(30)
            elif (ex.code == 500):
                print "500 search: "+" page:"+ str(i) + ex.msg
            else:
                print " http error search:"+"  "+" page:"+ str(i)  + ex.message
        except Exception as ex:
            print "error:" + ex.message
            i += 1
    print "ended"

if __name__ == "__main__":
    main()
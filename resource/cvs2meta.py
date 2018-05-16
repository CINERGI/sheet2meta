__author__ = 'valentin'

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

def read_url(url_file , context=None ):
    if (context == None ):
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        context.options &= ~ssl.OP_NO_SSLv3
    url_file_v = urllib2.urlopen(url_file , context=context)
    #dialect = csv.Sniffer().sniff(url_file_v.read(1024))
    #url_file_v.seek(0)
    #reader = csv.DictReader(url_file_v, dialect=dialect)
    reader = csv.DictReader(url_file_v, dialect=Dialect.doublequote)
    return reader

def read_input(csvfile , ):
    csvfile_v = open(csvfile, "rb")
    #dialect = csv.Sniffer().sniff(csvfile_v.read(1024))
    csvfile_v.seek(0)
    #reader = csv.DictReader(csvfile_v, dialect=dialect)
    reader = csv.DictReader(csvfile_v, dialect=Dialect.doublequote)
    return reader

def load_template(template_name, base_bath= '.'):
    loader = FileSystemLoader(base_bath)
    env = Environment(loader=loader, autoescape=True)
    env.globals['uuid'] = url2uuid
    template = env.get_template(template_name)

    return template

def url2uuid( b):
     u = uuid.uuid3(uuid.NAMESPACE_URL, b)
     return u.get_hex()

def datetimeformat(b, format='%Y-%m-%d'):
    from dateutil import parser
    dt = parser.parse(b)
    return dt.strftime(format)

def render_template(row, template):
    ddp = DateDataParser()

    return template.render(row=row, ddp=ddp, uuid=lambda b: url2uuid( b), datetimefmt=lambda b: datetimeformat( b))

def render_output(data,template,id_field, base_path='.',base_name=""):
    # base_name = template.name[0:template.name.index('.xml')]
    try:
        os.stat(base_path)
    except:
        os.mkdir(base_path)

    i = 0
    for d in data:
        template_values = {
            'row': d
            }
        try:
            #out = render_template(template_values, template)
            # need a remove bad XML chars from the row: https://gist.github.com/lawlesst/4110923
            out = render_template(d, template)
            # d[id_field]) inlcudes colons... so bad filenames
            #f_out = open(base_path+"/%s_%s.xml" % (base_name , d[id_field]) , "w")
            f_out = open(base_path+"/%s_%s.xml" % (base_name , i) , "w")
            i +=1
            f_out.write(out)
            f_out.close()
        except Exception  as err:
            print ("exception: ",  err)
            print "row failed:" + str(d)



def test_read_input():
    out = read_input('D:\dev_earthcube\sheet2meta\SEN CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    assert out != None
    for r in out:
        print r

def test_render_output():
    out = read_input('D:\dev_earthcube\sheet2meta\SEN CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    template = load_template('metadata19115_template_2.xml')
    render_output(out,template,'ID#info')

if __name__ == '__main__':
    test_render_output()
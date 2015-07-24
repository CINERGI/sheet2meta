__author__ = 'valentin'

import json
from jinja2 import Environment, FileSystemLoader
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
from dateparser.date import DateDataParser
import urllib2
import uuid

def read_url(url_file , ):
    url_file_v = urllib2.urlopen(url_file)
    #dialect = csv.Sniffer().sniff(url_file_v.read(1024))
    #url_file_v.seek(0)
    #reader = csv.DictReader(url_file_v, dialect=dialect)
    reader = json.load(url_file_v)
    return reader

def read_input(jsonfile , ):
    jsonfile_v = open(jsonfile, "rb")
    #dialect = csv.Sniffer().sniff(jsonfile_v.read(1024))
    jsonfile_v.seek(0)
    #reader = csv.DictReader(jsonfile_v, dialect=dialect)
    reader = json.load(jsonfile_v)
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

def render_template(row, template):
    ddp = DateDataParser()

    return template.render(row=row, ddp=ddp, uuid=lambda b: url2uuid( b))

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
            out = render_template(d, template)
            # d[id_field]) inlcudes colons... so bad filenames
            #f_out = open(base_path+"/%s_%s.xml" % (base_name , d[id_field]) , "w")
            f_out = open(base_path+"/%s_%s.xml" % (base_name , i) , "w")
            i +=1
            f_out.write(out)
            f_out.close()
        except:
            print "row failed:" + str(d)



def test_read_input():
    out = read_input('D:\dev_earthcube\sheet2meta\files\scraper\SPIDER_METADATA_4.json')
    assert out != None
    for r in out:
        print r

def test_render_output():
    out = read_input('D:\dev_earthcube\sheet2meta\files\scraper\SPIDER_METADATA_4.json')
    template = load_template('scraper_metadata19115.xml')
    render_output(out,template,'ID#info')

if __name__ == '__main__':
    test_render_output()
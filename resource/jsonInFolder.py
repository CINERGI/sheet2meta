from __future__ import absolute_import
import json
import sys

from jinja2 import Environment, FileSystemLoader

reload(sys)
sys.setdefaultencoding('utf-8')
import os
from dateparser.date import DateDataParser
import urllib2
import uuid
import ssl
from pprint import pprint

#with open('data.json') as data_file:
#    data = json.load(data_file)

def read_url(url_file , context=None ):
    url_file_v = urllib2.urlopen(url_file , context=context)

    reader = data = json.load(url_file_v)
    return reader

def read_input(jsonfile, ):
    with open(jsonfile) as data_file:
        data = json.load(data_file)

    return data

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
            # need a remove bad XML chars from the row: https://gist.github.com/lawlesst/4110923
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
    out = read_input('D:\dev_earthcube\sheet2meta\files\metpetdb\1986-086927.json')
    assert out != None
    for r in out:
        print r

def test_render_output():
    out = read_input('D:\dev_earthcube\sheet2meta\files\metpetdb\1986-086927.json')
    template = load_template('metadata19115_template_2.xml')
    render_output(out,template,'ID#info')

if __name__ == '__main__':
    test_render_output()
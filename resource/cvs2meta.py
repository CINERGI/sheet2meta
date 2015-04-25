__author__ = 'valentin'

import csv
from jinja2 import Environment, FileSystemLoader

def read_input(csvfile , ):
    csvfile_v = open(csvfile, "rb")
    dialect = csv.Sniffer().sniff(csvfile_v.read(1024))
    csvfile_v.seek(0)
    reader = csv.DictReader(csvfile_v, dialect=dialect)
    return reader

def load_template(template_name, base_bath= '.'):
    loader = FileSystemLoader(base_bath)
    env = Environment(loader=loader)
    template = env.get_template(template_name)
    return template

def render_output(data,template,id_field):
    # base_name = template.name[0:template.name.index('.xml')]
    base_name='sen'
    i = 0
    for d in data:

        out = template.render(d)
       # f_out = open("%s_%s.xml" % (base_name , d[id_field]) , "w")
        f_out = open("%s_%s.xml" % (base_name , i) , "w")
        i +=1
        f_out.write(out)
        f_out.close()



def test_read_input():
    out = read_input('D:\dev_earthcube\sheet2meta\SEN CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    assert out != None
    for r in out:
        print r

def test_render_output():
    out = read_input('D:\dev_earthcube\sheet2meta\SEN CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    template = load_template('metadata19115_template_2.xml')
    render_output(out,template,'ID#info')
__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheet/pub?key=1AZ48wUbN5xKXmctlCi7kQYDnTa8CtKQ2CYhCO-45OFo&gid=1581112451&single=true&output=csv')
    template = cvs2meta.load_template('hli_component_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/ci",base_name="hli")

if __name__ == "__main__":
    main()
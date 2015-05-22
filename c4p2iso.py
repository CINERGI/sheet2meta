__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/c4p from excel - PaleoResource 07-21-2014.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheet/pub?key=1A3_NYGBfD8r8lGXZzwupNA1OZwld7dQdb0Gmd36_hEQ&gid=486248522&single=true&output=csv')
    template = cvs2meta.load_template('c4p_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/c4p",base_name="c4p")

if __name__ == "__main__":
    main()
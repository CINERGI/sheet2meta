__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/ECOGEO CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheet/pub?key=1jlybj09_nJ-jb7Shb-U9Xm0NYooSI0qEJTxfm4CEi3E&gid=2041766188&single=true&output=csv')
    template = cvs2meta.load_template('generic_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/ecogeo",base_name="ecogeo")

if __name__ == "__main__":
    main()
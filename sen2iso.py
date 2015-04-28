__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():
    out = cvs2meta.read_input('files/SEN CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    template = cvs2meta.load_template('sen_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/sen",base_name="sen")

if __name__ == "__main__":
    main()
__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/c4p from excel - PaleoResource 07-21-2014.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheets/d/1QD2zJ1U0kfAvWuBwqy9fD_UM-19CVnKYQ_7_pxnaUcs/pub?gid=0&single=true&output=csv')
    template = cvs2meta.load_template('crescynt_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/crescynt",base_name="crescynt")

if __name__ == "__main__":
    main()
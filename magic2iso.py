__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    out = cvs2meta.read_input('files/zaslavsk_MagIC_Contribution_Summaries.csv')
    #out = cvs2meta.read_url('https://docs.google.com/spreadsheets/d/1QD2zJ1U0kfAvWuBwqy9fD_UM-19CVnKYQ_7_pxnaUcs/pub?gid=0&single=true&output=csv')
    template = cvs2meta.load_template('earthref_magic_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/earthref_magic",base_name="earthref_magic")

if __name__ == "__main__":
    main()
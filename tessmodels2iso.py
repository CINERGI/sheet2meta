__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    out = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\models\\Tess_models3_b_pivots2.csv')
    template = cvs2meta.load_template('tessmodels_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'Model Abbreviated Name#info', base_path="output/tess_models",base_name="tessmodels")

if __name__ == "__main__":
    main()
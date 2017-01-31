__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    out = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\models\\NOAA_Models_pdf_pivot.csv')
    template = cvs2meta.load_template('noaamodels_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'Number #', base_path="output/noaa_models",base_name="noaamodels")

if __name__ == "__main__":
    main()
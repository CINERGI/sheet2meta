__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    out = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\use case records to register in Cinergi - Sheet1.csv')
    template = cvs2meta.load_template('usecasedatasets_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID', base_path="output/usecaseDS",base_name="usecaseDS")

if __name__ == "__main__":
    main()
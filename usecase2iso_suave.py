__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    out = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\zaslavsk_EC_Use_Cases.csv')
    template = cvs2meta.load_template('usecase_metadata19115_suave.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'Internal ID', base_path="output/usecase_save",base_name="usecase")

if __name__ == "__main__":
    main()
__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/hli_pivot - Components.csv')
    out = cvs2meta.read_input('D:\\dev_earthcube\\sheet2meta\\files\\Use Case Summary Matrix_dwv - Combined Summaries_mod.csv')
    template = cvs2meta.load_template('usecase_metadata19115_clean.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'Internal ID (from List of Completed)', base_path="output/usecase",base_name="usecase")

if __name__ == "__main__":
    main()
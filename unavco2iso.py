__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    out = cvs2meta.read_input('files/archive_gnss.csv')
    #out = cvs2meta.read_url('https://docs.google.com/spreadsheet/pub?key=12Jpab0Bo2bOdRwQvcORFyq5sLxzavA_Njs4VJUKByVM&gid=1313886870&single=true&output=csv')
    template = cvs2meta.load_template('unavco_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'identifier', base_path="output/unavco",base_name="unavco")

if __name__ == "__main__":
    main()
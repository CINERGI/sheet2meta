__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/Databib - Repositories.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheet/pub?key=13fo2f3EyHTXauo71-EdoHzGzcF4f-OFnwo1izvl0lNg&gid=0&single=true&output=csv')
    template = cvs2meta.load_template('databib_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'URL', base_path="output/databib",base_name="databib")

if __name__ == "__main__":
    main()
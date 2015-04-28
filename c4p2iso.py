__author__ = 'valentin'

from resource import cvs2meta

def main():
    out = cvs2meta.read_input('files/c4p from excel - PaleoResource 07-21-2014.csv')
    template = cvs2meta.load_template('c4p_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/c4p",base_name="c4p")

if __name__ == "__main__":
    main()
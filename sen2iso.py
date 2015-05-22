__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():
    #out = cvs2meta.read_input('files/SEN CINERGI-ResourceInventoryTemplate - Basic Metadata Template.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheet/pub?key=1QQJaW15AfHwelthpgVFvEYbHCKIYsZtA0NfVK4Bx9vI&gid=464725857&single=true&output=csv')
    template = cvs2meta.load_template('sen_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/sen",base_name="sen")

if __name__ == "__main__":
    main()
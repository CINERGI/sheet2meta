__author__ = 'valentin'

from resource import cvs2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/CIComponentReview - Components.csv')
    out = cvs2meta.read_url('https://docs.google.com/spreadsheets/d/1dLIDidPAmOhTUSXy8klemB5M5-Xzbuf6xWTrLalzM0U/pub?gid=2041766188&single=true&output=csv')
    template = cvs2meta.load_template('streaming_metadata19115.xml',base_bath='./templates')
    cvs2meta.render_output(out,template,'ID#info', base_path="output/streaming",base_name="streaming")

if __name__ == "__main__":
    main()
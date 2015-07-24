__author__ = 'valentin'

from resource import scraper2meta
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

def main():

    #out = cvs2meta.read_input('files/c4p from excel - PaleoResource 07-21-2014.csv')
    out = scraper2meta.read_input('files/scraper/SPIDER_METADATA_4.json')
    template = scraper2meta.load_template('templates/scraper_metadata19115.xml',base_bath='./templates')
    scraper2meta.render_output(out,template,'catalogItem', base_path="output/scraper",base_name="scraper")

if __name__ == "__main__":
    main()
__author__ = 'valentin'
import unittest

from resource import cvs2meta

class TestStringMethods(unittest.TestCase):

    def test_render_template(self):
        out = cvs2meta.read_input('onerow.csv')
        template = cvs2meta.load_template('metadata19115_template_2.xml',base_bath='../')
        for d in out:
            template_values = {
            'row': d
            }
            rendered = cvs2meta.render_template(template_values,template)
            #print rendered
            self.assertIsNotNone(rendered)

    def test_render_oneouput(self):
        out = cvs2meta.read_input('onerow.csv')
        template = cvs2meta.load_template('metadata19115_template_2.xml',base_bath='../')
        for d in out:
            template_values = {
            'row': d
            }
            cvs2meta.render_output(template_values,template,'ID#info')



if __name__ == '__main__':
    unittest.main()
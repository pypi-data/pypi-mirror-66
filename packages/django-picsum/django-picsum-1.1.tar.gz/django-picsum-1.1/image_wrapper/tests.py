from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase

def render_template(content, **context_args):

    template = Template("{% load image_wrapper %}" + content)
    return template.render(Context(context_args))


class TemplateTagTest(TestCase):
    def test_picsum_tag(self):
        res = render_template("{% pic_rand height=300  pic_id=237 %}")
        self.assertHTMLEqual(
            res, '<img src="https://picsum.photos//id/237/300/">')

        with self.assertRaises(TemplateSyntaxError):
            """
            Width  is mandatory for the tag
            """
            res = render_template('{% pic_rand %}')

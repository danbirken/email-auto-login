import urllib

import jinja2

@jinja2.contextfilter
def login_code(context, value):
    url_parts = list(urllib.parse.urlparse(value))
    qs = dict(urllib.parse.parse_qsl(url_parts[4]))
    qs['auto_login_code'] = context.get('auto_login_code')
    url_parts[4] = urllib.parse.urlencode(qs)
    return urllib.parse.urlunparse(url_parts)

class TemplateManager():
    def __init__(self, template_location, base_url):
        self.base_url = base_url
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_location),
            autoescape=True,
        )

        self.jinja_env.filters['full_url'] = lambda x: base_url + x
        self.jinja_env.filters['login_code'] = login_code

    def render(self, template_name, values=None, auto_login_code=None):
        if values is None:
            values = {}

        values['auto_login_code'] = auto_login_code
        template = self.jinja_env.get_template(template_name)
        return template.render(**values)

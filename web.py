from werkzeug import exceptions, routing, utils, wrappers

class Website():
    def __init__(self, template_manager, email_auth, sender):
        self.template_manager = template_manager
        self.email_auth = email_auth
        self.sender = sender

        self.url_map = routing.Map([
            routing.Rule('/', endpoint='home'),
            routing.Rule('/email', methods=('POST',), endpoint='email'),
        ])

    def on_home(self, request, email):
        return self.render_template('home.html', values=
            {
                'email': email,
                'sent': 'sent' in request.args,
            }
        )

    def on_email(self, request, email):
        code = self.email_auth.generate_code(request.form['email'])
        email_html = self.render_template('email.html', auto_login_code=code)
        if self.sender:
            self.sender.send(
                request.form['email'], email_html.get_data(as_text=True)
            )
            return utils.Redirect('/?sent=1')
        else:
            return email_html

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)

        try:
            endpoint, values = adapter.match()
        except exceptions.NotFound:
            return wrappers.Response('Not Found', status=404)

        # Look for our special auto_login_code in the URL.  If there,
        # attempt to automatically log in
        email = None
        if 'auto_login_code' in request.args:
            email = self.email_auth.validate_code(
                request.args['auto_login_code']
            )

        return getattr(self, 'on_' + endpoint)(request, email, **values)

    def render_template(self, template, values=None, auto_login_code=None):
        return wrappers.Response(
            self.template_manager.render(
                template, values=values, auto_login_code=auto_login_code
            ),
            content_type='text/html'
        )

    def __call__(self, environ, start_response):
        request = wrappers.Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

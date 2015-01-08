#!/usr/bin/env python3

import argparse

from werkzeug import serving

import auth
import email_sender
import template_manager
import web

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--base-url', default='http://localhost:5005',
    help='URL to access the main page of the app')
parser.add_argument('-l', '--listen', default='localhost',
    help='Interface to listen on')
parser.add_argument('-e', '--template-dir', default='templates',
    help='Directory where templates are located')
parser.add_argument('-p', '--port', type=int, default=5005,
    help='Port to listen on')
parser.add_argument('-s', '--smtp-server',
    help='SMTP server to use for sending email.  If no SMTP server is given '
         'the emails will just be displayed in the web browser')
OPTIONS = parser.parse_args()

email_auth = auth.EmailCodeAuth(auth.KeyValueStore())

if OPTIONS.smtp_server:
    sender = email_sender.EmailSender(OPTIONS.smtp_server)
else:
    sender = None

website = web.Website(
    template_manager.TemplateManager(OPTIONS.template_dir, OPTIONS.base_url),
    email_auth,
    sender
)

serving.run_simple(
    OPTIONS.listen,
    OPTIONS.port,
    website,
    use_debugger=True,
    use_reloader=True
)

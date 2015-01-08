#!/usr/bin/env python3

import smtplib

from email.mime import multipart, text

class EmailSender():
    def __init__(self, smtp_server, from_address='me@localhost'):
        self.smtp_server = smtp_server
        self.from_address = from_address

    def send(self, to_address, html):
        msg = multipart.MIMEMultipart('alternative')
        msg['Subject'] = 'Auto Login Link'
        msg['From'] = self.from_address
        msg['To'] = to_address
        html = text.MIMEText(html, 'html')
        msg.attach(html)

        s = smtplib.SMTP(self.smtp_server)
        s.sendmail(self.from_address, to_address, msg.as_string())
        s.quit()

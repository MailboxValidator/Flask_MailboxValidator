from flask import current_app, Flask
from wtforms import ValidationError
import http.client
import urllib
import hashlib
import json


class SingleValidation:
    def __init__(self, apikey):
        self.apikey = apikey

    def ValidateEmail(self, email):
        p = { 'key': self.apikey, 'format': 'json', 'email': email }

        try:
            conn = http.client.HTTPConnection("api.mailboxvalidator.com")
            conn.request("GET", "/v1/validation/single?" + urllib.parse.urlencode(p))
            res = conn.getresponse()
            # print res.read()
            return json.loads(res.read())
        except:
            return None

    def DisposableEmail(self, email):
        p = { 'key': self.apikey, 'format': 'json', 'email': email }

        try:
            conn = http.client.HTTPConnection("api.mailboxvalidator.com")
            conn.request("GET", "/v1/email/disposable?" + urllib.parse.urlencode(p))
            res = conn.getresponse()
            # print res.read()
            return json.loads(res.read())
        except:
            return None

    def FreeEmail(self, email):
        p = { 'key': self.apikey, 'format': 'json', 'email': email }

        try:
            conn = http.client.HTTPConnection("api.mailboxvalidator.com")
            conn.request("GET", "/v1/email/free?" + urllib.parse.urlencode(p))
            res = conn.getresponse()
            # print res.read()
            return json.loads(res.read())
        except:
            return None

# Class to validate the email from form

class EmailValidation(object):
    # see http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code
    def __init__(self, apikey, app=None, message=None):
        self.apikey = apikey
        SingleValidation(self.apikey)
        self.app = app
        if app is not None:
            self.init_app(app)
        if not message:
            message = 'Error: Email is not valid.'
        self.message = message

    def init_app(self, app):
        # See http://flask.pocoo.org/docs/0.12/extensiondev/#the-extension-code
        # Perform Class type checking
        if not isinstance(app, Flask):
            raise TypeError("flask_MailboxValidator.EmailValidation.init_app(): Parameter 'app' is an instance of class '%s' "
                            "instead of a subclass of class 'flask.Flask'."
                            % app.__class__.__name__)

        # Bind Flask-User to app
        app.user_manager = self

    def __call__(self, form, field):
        email = field.data
        email_result = SingleValidation.ValidateEmail(self,email)
        # check disposable
        if email_result['is_disposable']:
            print ('is_disposable: ' + email_result['is_disposable'])
            if email_result['is_disposable'] == 'True':
                raise ValidationError('Error: You should not use the disposable email from ' + email_result['domain'] + ' to register.')
        # check email syntax
        elif email_result['is_syntax']:
            print ('is_syntax: ' + email_result['is_syntax'])
            if email_result['is_syntax'] == 'False':
                raise ValidationError('Error: You should enter email with valid syntax.')
        # check email MX record
        elif email_result['is_domain']:
            print ('is_domain: ' + email_result['is_domain'])
            if email_result['is_domain'] == 'False':
                raise ValidationError('Error: The email address do not have valid MX record in its DNS entries.')
        # check email server is respond to the server or not
        elif email_result['is_smtp']:
            print ('is_smtp: ' + email_result['is_smtp'])
            if email_result['is_smtp'] == 'False':
                raise ValidationError('Error: The email address do not have valid MX record in its DNS entries.')
        # check email is actually exists or not:
        elif email_result['is_verified']:
            print ('is_verified: ' + email_result['is_verified'])
            if email_result['is_verified'] == 'False':
                raise ValidationError('Error: The email address do not have valid MX record in its DNS entries.')
        # check if the email is blacklisted by MBV or not
        elif email_result['is_suppressed']:
            print ('is_suppressed: ' + email_result['is_suppressed'])
            if email_result['is_suppressed'] == 'False':
                raise ValidationError('Error: The email address do not have valid MX record in its DNS entries.')
        # check whether the email is belongs to role based email or not
        elif email_result['is_role']:
            print ('is_role: ' + email_result['is_role'])
            if email_result['is_role'] == 'False':
                raise ValidationError('Error: The email address do not have valid MX record in its DNS entries.')
        # check whether the email contains high risk keywords or not
        elif email_result['is_high_risk']:
            print ('is_high_risk: ' + email_result['is_high_risk'])
            if email_result['is_high_risk'] == 'False':
                raise ValidationError('Error: The email address do not have valid MX record in its DNS entries.')
        else:
            print ('MBV Error:' + email_result['error_message'])

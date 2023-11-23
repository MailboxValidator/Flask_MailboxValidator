MailboxValidator Flask Python Module
==============================

This Flask Python module enables user to easily validate if an email address is valid, a type of disposable email or free email.

This module can be useful in many types of projects, for example

 - to validate an user's email during sign up
 - to clean your mailing list prior to email sending
 - to perform fraud check
 - and so on



Installation
============

To install this module type the following:

	pip install flask_MailboxValidator



Dependencies
============

An API key is required for this module to function. Go to https://www.mailboxvalidator.com/plans#api to sign up for FREE API plan and you'll be given an API key.

In order to use this module to validate email from form, WTForms and Flask-WTF need to be installed. Also, nose2 need to be installed in order to run the test file.



Functions
=========

## SingleValidation (api_key)

Creates a new instance of the MailboxValidator object with the API key.

## ValidateEmail (email_address)

Performs email validation on the supplied email address.

### Return Fields

| Field Name             | Description                                                  |
| ---------------------- | ------------------------------------------------------------ |
| email_address          | The input email address.                                     |
| domain                 | The domain of the email address.                             |
| is_free                | Whether the email address is from a free email provider like Gmail or Hotmail. Return values: True, False |
| is_syntax              | Whether the email address is syntactically correct. Return values: True, False |
| is_domain              | Whether the email address has a valid MX record in its DNS entries. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_smtp                | Whether the mail servers specified in the MX records are responding to connections. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_verified            | Whether the mail server confirms that the email address actually exist. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_server_down         | Whether the mail server is currently down or unresponsive. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_greylisted          | Whether the mail server employs greylisting where an email has to be sent a second time at a later time. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_disposable          | Whether the email address is a temporary one from a disposable email provider. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_suppressed          | Whether the email address is in our blacklist. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_role                | Whether the email address is a role-based email address like admin@example.net or webmaster@example.net. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_high_risk           | Whether the email address contains high risk keywords. Return values: True, False, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| is_catchall            | Whether the email address is a catch-all address. Return values: True, False, Unknown, -&nbsp;&nbsp;&nbsp;(- means not applicable) |
| mailboxvalidator_score | Email address reputation score. Score > 0.70 means good; score > 0.40 means fair; score <= 0.40 means poor. |
| time_taken             | The time taken to get the results in seconds.                |
| status                 | Whether our system think the email address is valid based on all the previous fields. Return values: True, False |
| credits_available      | The number of credits left to perform validations.           |
| error_code             | The error code if there is any error. See error table in the below section. |
| error_message          | The error message if there is any error. See error table in the below section. |

## DisposableEmail (email_address)

Check if the supplied email address is from a disposable email provider.

### Return Fields

| Field Name        | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| email_address     | The input email address.                                     |
| is_disposable     | Whether the email address is a temporary one from a disposable email provider. Return values: True, False |
| credits_available | The number of credits left to perform validations.           |
| error_code        | The error code if there is any error. See error table in the below section. |
| error_message     | The error message if there is any error. See error table in the below section. |

## FreeEmail (email_address)

Check if the supplied email address is from a free email provider.

### Return Fields

| Field Name        | Description                                                  |
| ----------------- | ------------------------------------------------------------ |
| email_address     | The input email address.                                     |
| is_free           | Whether the email address is from a free email provider like Gmail or Hotmail. Return values: True, False |
| credits_available | The number of credits left to perform validations.           |
| error_code        | The error code if there is any error. See error table in the below section. |
| error_message     | The error message if there is any error. See error table below. |



# Usage for validate email from form

*Note: WTForms and Flask-WTF must be installed before using this features.*

This Flask Python module had three different validator for different uses: EmailValidation for validating email address by all parameters, DisposableEmailValidation for validating disposable email address, and FreeEmailValidation for validating free email address.

1. Import the validator class from the package. For example: `from flask_MailboxValidator.SingleValidation import EmailValidation`
2. Call the validator in validator array along with your API key. For example: `email = StringField('Email:', validators=[validators.InputRequired(), EmailValidation(apikey='Your_API_Key')])`


Sample Codes
============

## Validate email

```python
import flask_MailboxValidator
from flask import Flask
from flask import jsonify

app = Flask(__name__)

mbv = flask_MailboxValidator.SingleValidation('PASTE_API_KEY_HERE')
results = mbv.ValidateEmail('example@example.com')

@app.route('/')
def display_result():
	if results is None:
		return("Error connecting to API.\n")
	elif 'error' not in results:
		return (jsonify(results))
	else:
		return('error_message = ' + results['error']['error_message'] + "\n")
```


Check if an email is from a disposable email provider
-------------------------------------------------------------------

```python
import flask_MailboxValidator
from flask import Flask
from flask import jsonify

app = Flask(__name__)

mbv = flask_MailboxValidator.SingleValidation('PASTE_API_KEY_HERE')
results = mbv.DisposableEmail('example@example.com')

@app.route('/')
def display_result():
	if results is None:
		return("Error connecting to API.\n")
	elif 'error' not in results:
		return (jsonify(results))
	else:
		return('error_message = ' + results['error']['error_message'] + "\n")
```


Check if an email is from a free email provider
------------------------------------------------------------

```python
import flask_MailboxValidator
from flask import Flask
from flask import jsonify

app = Flask(__name__)

mbv = flask_MailboxValidator.SingleValidation('PASTE_API_KEY_HERE')
results = mbv.FreeEmail('example@example.com')

@app.route('/')
def display_result():
	if results is None:
		return("Error connecting to API.\n")
	elif 'error' not in results:
		return (jsonify(results))
	else:
		return('error_message = ' + results['error']['error_message'] + "\n")
```

# Test

To run the test file, you will first need to replace the 'PASTE_API_KEY_HERE' with your API key in the test file(Located at test directory). After that, run this command in terminal: `python setup.py test`


Errors
======

| error_code | error_message |
| ---------- | ------------- |
| 10000 | Missing parameter. |
| 10001 | API key not found. |
| 10002 | API key disabled. |
| 10003 | API key expired. |
| 10004 | Insufficient credits. |
| 10005 | Unknown error. |

Copyright
=========

Copyright (C) 2018-2023 by MailboxValidator.com, support@mailboxvalidator.com

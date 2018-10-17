import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(
	name="flask_MailboxValidator",
	version="1.0.0",
	author="MailboxValidator.com",
	author_email="support@mailboxvalidator.com",
	description="Email verification module for Flask using MailboxValidator API. It validates if the email is valid, from a free provider, contains high-risk keywords, whether it\'s a catch-all address and so much more.",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/MailboxValidator/mailboxvalidator-python",
	packages=setuptools.find_packages(),
	classifiers=(
		"Development Status :: 5 - Production/Stable",
		"Intended Audience :: Developers",
		"Topic :: Software Development :: Libraries :: Python Modules",
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	),
	zip_safe=False,
	install_requires=[
		'Flask>=1.0.2',
		'Flask-WTF>=0.14.2',
		# 'nose2>=0.8.0',
		'WTForms>=2.2.1',
	],
	extras_require={
		'tests': [
			'nose2',],
		'docs': [
			'sphinx >= 1.8.1',
			'Pallets-Sphinx-Themes']
	},
	test_suite='nose2.collector.collector',
)
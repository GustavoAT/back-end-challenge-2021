""" Environment settings

Edit database credentials
user, password, host and database on the url, 
the APIkey and so on, then
rename the file to 'settings.py'.
The url is for MySQL, to use other database engines,
search documentation on SQLAlchemy:
https://docs.sqlalchemy.org/en/14/dialects/index.html
"""

#Use format:
#mysql+pymysql://[user]:[password]@[host][/database][?options]

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:rootpass@db/backendchallenge'

API_KEY = 'mysecretapikey'
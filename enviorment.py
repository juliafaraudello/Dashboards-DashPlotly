import os
os.environ['FLASK_SECRET_KEY'] = 'f7dd03a712516f3368104bad5bf1129d'
os.environ['GOOGLE_AUTH_URL'] = 'https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent'
os.environ['GOOGLE_AUTH_SCOPE'] = 'email'
os.environ['GOOGLE_AUTH_TOKEN_URI'] = 'https://oauth2.googleapis.com/token'
os.environ['GOOGLE_AUTH_REDIRECT_URI'] = 'http://localhost:8822/login/callback'
os.environ['GOOGLE_AUTH_USER_INFO_URL'] = 'https://www.googleapis.com/userinfo/v2/me'
os.environ['GOOGLE_AUTH_CLIENT_ID'] = '376810677009-5cbgb7okb91tg0skgoucjaptcsph5c76.apps.googleusercontent.com'
os.environ['GOOGLE_AUTH_CLIENT_SECRET'] = 'xxxxxx'
os.environ['OAUTHLIB_INSECURE_TRANSPORT']  = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE']='0'
os.environ['FLASK_APP'] = 'main.py'
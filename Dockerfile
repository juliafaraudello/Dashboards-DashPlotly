FROM python:3.6
USER root
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
ENV FLASK_SECRET_KEY "f7dd03a712516f3368104bad5bf1129d"
ENV GOOGLE_AUTH_URL https://accounts.google.com/o/oauth2/v2/auth?access_type=offline&prompt=consent
ENV GOOGLE_AUTH_SCOPE "email"
ENV GOOGLE_AUTH_TOKEN_URI https://oauth2.googleapis.com/token
ENV GOOGLE_AUTH_REDIRECT_URI http://localhost:8822/login/callback
ENV GOOGLE_AUTH_USER_INFO_URL https://www.googleapis.com/userinfo/v2/me
ENV GOOGLE_AUTH_CLIENT_ID "376810677009-5cbgb7okb91tg0skgoucjaptcsph5c76.apps.googleusercontent.com"
ENV GOOGLE_AUTH_CLIENT_SECRET "SvoeptnXsqeirAMctcU-LarF"
ENV OAUTHLIB_INSECURE_TRANSPORT '1'
ENV OAUTHLIB_RELAX_TOKEN_SCOPE '0'
ENV FLASK_APP app.py
EXPOSE 5000
CMD ["python3", "app.py"]


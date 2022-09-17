from flask import redirect, url_for
from flask import current_app as app
from flask.globals import session 
from flask_dance.contrib.google import make_google_blueprint, google
from dashboards.benchmarkingms import benchmarkingms 

'''
    Configuracion de blueprint
    redirect_to /connected.
'''
google_blueprint = make_google_blueprint(
        client_id = "376810677009-5cbgb7okb91tg0skgoucjaptcsph5c76.apps.googleusercontent.com",
        client_secret = "SvoeptnXsqeirAMctcU-LarF",
        scope=['https://www.googleapis.com/auth/userinfo.email','openid','https://www.googleapis.com/auth/userinfo.profile'],
               redirect_to = 'connected', 
        offline = True, reprompt_consent = True)
#app.register_blueprint(google_blueprint)

@app.route('/benchmarkingms/<string:token>')
def dashbenchmarking(token): 
    with app.app_context():
        session['token'] = token
        return redirect("/dashMS/" + token, code=302, Response=None)
        #return redirect(location = "/dashMS/" + token)

@app.route('/checkService')
def checkService():
    return 'Alive'
    
@app.route('/tendencia')
def tendencia():
    return redirect(location = "/dashTendencia", code=302, Response=None)

@app.route('/otros')
def otros():
    return redirect(location = "/dashOtros", code=302, Response=None)

@app.route('/connected')
def connected():
    return redirect(location = "/benchmarkms", code=302, Response=None)



'''
    @app.route('/') 
    def googleLogin():
        user_info_endpoint = '/oauth2/v2/userinfo'
        if google.authorized:
            google_data = google.get(user_info_endpoint).json()
            return redirect("/dashBenchmarkingMS", code = 302, Response=None)
    else:
        return redirect("/google", code = 302, Response=None)
    Esto es cuando se redirigue despues de conectarse con Google.
    se define el endpont /Googles
'''
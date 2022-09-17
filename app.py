from flask import Flask, g, session
from werkzeug.middleware.proxy_fix import ProxyFix
app = Flask(__name__, instance_relative_config=False, template_folder="templates")

def init_app():
    """Construct core Flask application with embedded Dash app."""
    app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
    with app.app_context():
        import routes
        from dashboards.benchmarkingms import benchmarkingms 
        from dashboards.otros import otros 
        from dashboards.tendencias import tendencias 
        benchmarkingD = benchmarkingms.benchmarkingms(flaskApp = app)
        otrosD = otros.createDash(app)
        tendenciasD = tendencias.createDash(app)
            
    return app

app = init_app()
app.config.from_object('config')

if __name__ == "__main__":
    app.run(host='0.0.0.0',  port=5000)

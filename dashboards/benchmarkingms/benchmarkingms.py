import dash
import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
from dashboards.benchmarkingms import callbacks

class benchmarkingms:

    def __init__(self, **args):
        app = args['flaskApp']
        self.app = app
        self.dash_app = dash.Dash(__name__, url_base_pathname='/dashMS/', server = app, 
                                    external_stylesheets = [dbc.themes.BOOTSTRAP,
                                    'https://use.fontawesome.com/releases/v5.11.2/css/all.css',
                                    {'href': 'https://fonts.googleapis.com/icon?family=Material+Icons',
                                    'rel':'stylesheet'}])
        self.flaskApp = self.app
        self.dash_app.title = "Benchmark de lotes"
        self.dash_app.css.config.serve_locally = False
        self.dash_app.scripts.config.serve_locally = False        
     
        self.buttomClicks = {"rs":0, "ts":0, "avg":0,"std":0,"sum":0}
        self.dash_app.layout = self.setLayout()
        callbacks.defineGlobalcallback(self)


    def setLayout(self):
        return html.Div([
            
            self.componentNavBar(),
            self.componentTarjetaBenvenida(),
            html.Br(),
            html.Div([
                    dcc.Loading(
                        id = "loadingScreen",
                        children = [html.Div(children = html.Div([""]), id = "screen")],
                        type = "circle",
                    )
            ], className='w-100 p-3')
        ], className='w-100 p-3', style = {'WebkitBoxShadow': '0px 5px 5px 0px rgba(100, 100, 100, 0.1)',
                                          'margin-left':'0','width':'100%'})
     
    def componentNavBar(self):
        return dbc.Navbar([
               html.A(
                        dbc.Row([
                        dbc.Col(html.Img(src = self.dash_app.get_asset_url("icon.png"),
                                         height="50px", style={'stroke': '#508caf'})),], align = "center", no_gutters = True),
                                        href = 'www.geoagro.com'
               ),
               dbc.Container([
                            dbc.Button("Resumen", id = "resumenBT", color = "warning", outline = True, className = "mr-1", style={'border':'solid 0.15vw #F6C54C', 'color':'black', 'border-radius':'5%','font_family':"Roboto"}),
                            dbc.Button("Serie Temporal", id = "serietemporalBT", color = "warning", outline=True, className="mr-1", style={'border':'solid 2px #F6C54C','color':'black','border-radius':'5%','font_family':"Roboto"}),
                            dbc.DropdownMenu(label= "Ranking", children= [
                                dbc.DropdownMenuItem("Indice Medio", id = "avgBT"), 
                                dbc.DropdownMenuItem("Indice Acumulado", id = "IntegralBT"),
                                dbc.DropdownMenuItem("Desvío Estándar", id = "desvioBT")
                            ], color = "white", right = True, style = {'border':'solid 0.15vw #F6C54C','border-radius':'5%','color':'black','font_family':"Roboto"})
               ], style = {'display':'flex', 'flex-direction':'row', 'justify-content':'right', 'margin-left':'60vw','gap':'0.5vw'})
               ], sticky = "top", className = 'mb-4 bg-white', style = {'WebkitBoxShadow':'0px 5px 5px 0px rgba(100, 100, 100, 0.1)'})

    def dropdownFarm(self):
        options = []
        options.append({"label":"Todos", "value":"Todos"})
        options = options + [{"label":farm, "value":farm} for farm in set(self.df["farmname"].values)]
        return dcc.Dropdown(
                              id = 'farms',
                              options = options,
                              clearable = False,
                              searchable = True,
                              placeholder = "Filtro por establecimiento",
                              style = {'width':'18vw'}
                            )
  
    def componentTarjetaBenvenida(self):
        return dbc.Alert(children=[
            # html.Img(src = self.dash_app.get_asset_url("img.png"), height = "60px", style = {'color':'grey'}),
            html.Br(),
            html.Br(),
            html.H3("Benchmarking de tu Espacio de Trabajo"), 
            html.Br(),
            html.H5("Compara tus lotes utilizando un indice como benchmark."),
            html.Br(),
            html.Br(),
            html.A( "Para mas información consulte el manual de uso.", 
                    href = "https://support.geoagro.com/es/kb/benchmarking-de-tu-espacio-de-trabajo/", 
                    className = "alert-link",target='_blank'),
            html.Br(),
            html.Br(),
        ],
        id = "alert-fade",
        dismissable = True,
        is_open = True,
        style = {"z-index":"10", "left":"70vw", "position":"absolute",
                 'color':'#575050', 'background-color': '#F2C43E',
                 'font_family':"Roboto","border-radius":"1vw",'margin-right':'0.5vw'})

    def componentMenu(self):
        return  dbc.Tabs(
                [
                    dbc.Tab(label="Resumen", id = "tableresumen", tab_id = "tableresumen"),
                    dbc.Tab(label="Indice medio", id = "ndvi", tab_id = "ndvi",label_style = {"color": "black"}),
                    dbc.Tab(label="Series temporales", id = "seriestemporales", tab_id = "seriestemporales"),
                    dbc.Tab(label="Ranking", id = "ranking", tab_id = "ranking"),
                    dbc.Tab(label="Desvío Estándar", id="desvio", tab_id = "desvio"),
                ],
                id = "tabs",
                active_tab = "firstCall")

    def getDash(self):
        return self.dash_app
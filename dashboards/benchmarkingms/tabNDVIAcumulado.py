import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
from dashboards.benchmarkingms import SharedComponent
from dashboards.benchmarkingms.helper import utils

def tabNDVI(self):
        return html.Div([
                                SharedComponent.searchFarms(self),
                                html.Br(),                  
                                componentDistribucionNDVI(self),
                                html.Br(),
                                componentComparacionNDVI(self),
                                html.Br(),
                                componentDescriptiontabNDVI(self)
                        ], style={'width':'100%'})
 

def componentDistribucionNDVI(self):
        fig = SharedComponent.createMap(df = self.datasource.getFiltered_df(), featuresCollection = self.featuresCollection, type = "ndviavg",  centroid = utils().calcularCentroid(self.datasource.getFiltered_df()))
        return html.Div([
                    dbc.Card([
                            dbc.CardHeader( ("Distribución de índice medio"), style = {'background-color':'#648A5F', 'border-radius':'3%', 'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                            dbc.CardBody(
                            [
                                    dcc.Graph(
                                        figure = fig,
                                        id = "ndvimap"
                                    )
                            ], style = {'border-radius':'3%'})
                        ])
                        ])
                
def componentComparacionNDVI(self):
        fig = SharedComponent.scatterChart(self, "ndviavg")
        return html.Div([
                dbc.Card([
                            dbc.CardHeader(("Ranking por índice medio"), style= {'background-color':'#648A5F', 'border-radius':'3%', 'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"} ),
                            dbc.CardBody(
                            [
                                html.Div([
                                    dcc.Graph(figure = fig)
                                ])
                            ], style={'border-radius':'3%'})
                ])])
                
def componentDescriptiontabNDVI(self):
        return  html.Div([
                    dbc.Alert(
                        [
                            "El índice medio es calculado a partir del valor del índice para cada lote en el período de análisis seleccionado, permite identificar de manera expeditiva los lotes de mayor nivel de biomasa en el período. Se aconseja utilizar filtros de cultivos, híbrido y fecha de simebra para un correcto análisis.",
                            # html.A("base de conocimiento.", href="https://www.google.com.ar", className="alert-link"),
                        ],
                            color = "info",
                            style = {'background-color':'#F6C54C', 'opacity':'95%', 'color':'black', 'border-radius':'3%', 'margin-top': '1.5vw','font-size':'0.85vw','font_family':"Roboto"}
                        ),
                ])


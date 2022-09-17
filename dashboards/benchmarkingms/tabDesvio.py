import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
from dashboards.benchmarkingms import SharedComponent
from dashboards.benchmarkingms.helper import utils

def tabDesvio(self):
        return html.Div([
                            SharedComponent.searchFarms(self),
                            html.Br(),
                            componentNdviDs(self),
                            html.Br(),
                            componentRankinDS(self),
                            html.Br(),
                            componentDescripcionDesvio()
                        ], style={'width':'100%'})

def componentNdviDs(self):
        fig = SharedComponent.createMap(df = self.datasource.getFiltered_df(), featuresCollection = self.featuresCollection, type = "ndvistd", centroid=utils().calcularCentroid(self.datasource.getFiltered_df()))
        return html.Div([
            dbc.Card([
                        dbc.CardHeader(("Distribución del Desvío Estándar"), style =
                         {'background-color':'#648A5F',
                          'border-radius':'3%', 'color':'white', 
                          'font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                        dbc.CardBody(
                        [
                            dcc.Graph(
                                figure = fig,
                                id = "mapndvistd"
                            )
                        ], style = {'border-radius':'3%'})
                ])
            ])
                

def componentRankinDS(self):
        fig =  SharedComponent.scatterChart(self, "ndvistd")
        return html.Div([
                        dbc.Card([
                                dbc.CardHeader(("Rankig por Desvío Estándar"),
                                style = {'background-color':'#648A5F', 'border-radius':'3%', 
                                        'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                                dbc.CardBody(
                                [
                                        html.Div([
                                                dcc.Graph(figure = fig)
                                        ])
                                ], style = {'border-radius':'3%'})
                        ])
                ])

def componentDescripcionDesvio():
        return html.Div([
                        dbc.Alert(
                        [
                                "El desvio estandar, indica la variabilidad de los lotes de tu espacio de trabajo en el período de análisis. Permite identificar si el desarrollo de los cultivos fue de manera estable a lo largo del ciclo o presentan alteraciones.",
                                # html.A( "base de conocimiento.", href = "https://www.google.com.ar", className = "alert-link"),
                        ],
                                color = "info",
                                style = {'background-color':'#F6C54C', 'opacity':'95%', 'color':'black', 'border-radius':'3%', 'margin-top': '1.5rems','font-size':'0.85rems','font_family':"Roboto"}
                        ),
                        ])
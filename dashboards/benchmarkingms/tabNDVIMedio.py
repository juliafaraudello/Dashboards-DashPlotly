import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
from dashboards.benchmarkingms import SharedComponent
from dashboards.benchmarkingms.helper import utils

def tabRanking(self):
    return  html.Div([
                    SharedComponent.searchFarms(self),
                    html.Br(),
                    componentMapNDVIAcum(self),
                    html.Br(),
                    componentNdviAcum(self),
                    html.Br(),
                    componentDescripcionRanking(self)
                    ], style = {'width':'100%'}),


def componentMapNDVIAcum(self):
    fig = SharedComponent.createMap(df = self.datasource.getFiltered_df(), 
                                    featuresCollection = self.featuresCollection,
                                     type = "ndvisum",
                                     centroid = utils().calcularCentroid(self.datasource.getFiltered_df())) 
    return html.Div([
        dbc.Card([
                    dbc.CardHeader(("Distribución del índice acumulado"),
                                   style = {'background-color':'#648A5F', 'border-radius':'3%',
                                            'color':'white','font-weight': 'bold',
                                            'font-size':'0.80vw','font_family':"Roboto"}),
                    dbc.CardBody(
                    [
                        dcc.Graph(
                            figure = fig,
                            id = "mapndvisum"
                        )
                    ],style={'border-radius':'3%'})
        ])])


def componentNdviAcum(self):
    fig = SharedComponent.scatterChart(self, "ndvisum")
    return html.Div([
            dbc.Card([
                    dbc.CardHeader(("Ranking por índice acumulado"), 
                                        style = {'background-color':'#648A5F',
                                                'border-radius':'3%', 'color':'white',
                                                'font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                    dbc.CardBody(
                    [
                        html.Div([
                            dcc.Graph(figure = fig)
                        ])
                    ],style = {'border-radius':'3%'})
             ])])   

def componentDescripcionRanking(self):
        return html.Div([
                        dbc.Alert(
                                [
                                    "La serie temporal del índice nos permite obtener un ranking del índice acumulado en el período de análisis. De manera sencilla podes conocer los lotes de mayor nivel de biomasa y su ubicacion en relación a los otros lotes de tu espacio de trabajo. Conocer los lotes de mejor desempeño permite identificar buenas prácticas o factores que alteran el cultivo.",
                                ],
                                    color="info",
                                    style = {'background-color':'#F6C54C', 'opacity':'95%',
                                     'color':'black', 'border-radius':'3%',
                                    'margin-top': '1.5vw','font-size':'0.85vw','font_family':"Roboto"}
                                ),
                        ])
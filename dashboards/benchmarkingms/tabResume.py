import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
from dashboards.benchmarkingms import SharedComponent
from dashboards.benchmarkingms.helper import utils
import plotly.express as px

def tabResumen(self):
    Firstscreen = dbc.Row([
        dbc.Col(children=componentDistribucionCultivos(self), id = "mapaCultivos" ,style = {'margin':'0'}),
        dbc.Col([
                    componentInfoGeneral(self),
                    componentEstablecimientoSeleccionado(self),
                ]
                ,style={'margin':'0','display':'flex',
                        'flex-direction':'column','justify-content':'center',
                        'align-items':'center','width':'100%','gap':'2vw'})
        ],style= {'margin':'0','display':'flex','flex-direction':'row',
                 'justify-content':'center',
                'width':'100%','gap':'0.5 vw'})
    
    SecondScreen =  dbc.Row([
                dbc.Col(children=componentSuperficieHibrido(self), style = {'margin':'0'}),
                dbc.Col(children=componentSuperficiesiembra(self), style = {'margin':'0'}),
            ],style={'margin':'0','display':'flex','flex-direction':'row',
            'justify-content':'center','width':'100%','gap':'3vw'})
    
    Description = dbc.Row([
            dbc.Alert(
                        [
                            "Se representa información sobre los Establecimientos y Lotes seleccionados, como la superficie a analizar y los cultivos. En el mapa se visualiza la distribución de los cultivos por Establecimiento, y en el Piechart la superficie por cultivo e híbrido.",
                            # html.A("manual de uso.", href="https://support.geoagro.com/es/", className="alert-link", target='_blank'),
                        ],
                        style = {'background-color':'#F2C43E', 'color':'black', 'border-radius':'3%',
                                'margin-top': '1.5vw','width':'93vw','font-size':'0.85vw','font_family':"Roboto"}),
            ], style = {'margin':'0','display':'flex','flex-direction':'row',
                       'justify-content':'center','width':'100%','gap':'15px'})
    
    return html.Div([
                    Firstscreen,
                    html.Br(),
                    SecondScreen,
                    Description,
                ], className = 'w-100 p-3', style = {'margin':'0'}),

def componentDistribucionCultivos(self):
        fig = SharedComponent.createMap(df = self.datasource.getFiltered_df(), 
        featuresCollection = self.featuresCollection, type = "crop_color",
        centroid = utils().calcularCentroid(self.datasource.getFiltered_df()))
        
        return dbc.Card([
            dbc.CardHeader(("Distribución de cultivos"), style={'background-color':'#648A5F',
                                                                 'border-radius':'3%',
                                                                 'color':'white','font-weight': 'bold',
                                                                 'font-size':'0.80vw','font_family':"Roboto"}),
            dbc.CardBody([  
                        dcc.Graph(
                                    figure=fig,
                                    id="mapndvicrop"
                                 )
                        ])
            ], style={'width': "60vw",
                      'border-radius':'3%',
                      'margin-left':'0%',
                      'padding':'0'})
    

def componentInfoGeneral(self):
        tothect = round(self.datasource.getFiltered_df()['has'].sum(), 2)
        start_date = "2020-10-20"
        end_date = "2021-10-20" 
        return dbc.Card([
                dbc.CardBody(
                [           html.Br(),
                            html.H5(("Información General"), style = {'font-weight': 'bold','font-size': '1vw','color':'black','font_family':"Roboto"}),
                            #html.Br(),
                            #html.H6(("Espacio de Trabajo: harcode"), style = {'font-weight': 'bold','font-size': '0.85vw'}),
                            html.H6(("Fecha de análisis: " + start_date + " - " + end_date), style = {'font-size': '0.85vw','font_family':"Roboto"}),
                            html.H6(("Campaña: 2021-2022 | Superficie total [ha]: " + str(tothect)), id='has', style={'font-size': '0.85vw','font_family':"Roboto"}),
                            html.Br(),
                ], style={'display':'flex','flex-direction':'column','justify-content':'center','align-items':'center','gap':'0.5vw','border-radius':'3%'})
        ], style = {'width':'29vw','border-radius':'3%'})


def componentEstablecimientoSeleccionado(self):
    return  dbc.Card([
                dbc.CardBody(
                [
                    html.Br(),
                    html.H5(("Seleccione un Establecimiento"), style = {'font-weight': 'bold','font-size': '1vw','color':'black','font_family':"Roboto"}),
                    dropdownFarm(self),
                    html.Br(),
                    html.H5(("Lotes seleccionados"), style = {'font-weight': 'bold',
                                                              'font-size': '1vw',
                                                              'color':'black','font_family':"Roboto"}),
                    dcc.Loading(
                        id="loading-2",
                        children = [html.Div([html.Div(id = "loadFields")])],
                        type="circle",
                    ),
                    html.Br(),
                ], style={'display':'flex','flex-direction':'column','justify-content':'center', 
                        'align-items':'center', 'gap':'0.5vw', 'border-radius':'3%'})
            ], style={'width':'29vw','border-radius':'3%'})


def componentSuperficieHibrido(self):
    
        dfFiltered = self.datasource.getFiltered_df().groupby(["crop_name", "hibrido"]).agg(has=('has', 'sum')).reset_index()
        dfFiltered = dfFiltered[dfFiltered["crop_name"].str.contains("-Not assigned-") == False]
        dfFiltered = dfFiltered[dfFiltered["crop_name"].str.contains("-No asignado-") == False]
        cultivos, hibridos, values = [], [], []
        cultivos_has = {}
        for index, row  in dfFiltered.iterrows():
            hibridos = hibridos + [row['hibrido']]
            cultivos = cultivos + [row['crop_name']]
            if row['crop_name'] in cultivos_has:
                cultivos_has[row['crop_name']] += row["has"]
            else:
                cultivos_has[row['crop_name']] = row["has"]
            values = values + [row["has"]]

        cultivosSet = list(set(cultivos))
        cultivos_values = [cultivos_has[element] for element in cultivosSet]
        character = ["Cultivo"] + cultivosSet +  hibridos
        parent = [""] + ["Cultivo"]*len(cultivosSet) + cultivos
        values  = [sum(values)] + cultivos_values + values 
        data = dict(
            character = character,
            parent = parent,
            value = values
        )
        fig = px.sunburst(data, names = 'character', parents = 'parent', values = 'value', color_discrete_sequence=["#477442", "#648A5F"])
        fig.update_layout(showlegend=True, margin={"r":0,"t":0,"l":0,"b":0}, font_family="Roboto") 
        fig.update_traces(hovertemplate = '%{parent} <br><br>Superficie [ha]: %{value:.2f}')       
        return dbc.Card([
                            dbc.CardHeader(("Superficie de híbrido por cultivo"), style = 
                            {'background-color':'#648A5F', 'border-radius':'3%',
                            'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                            dbc.CardBody(
                            [
                                dcc.Graph(
                                            figure=fig,
                                            id="sunbrust"
                                         )
                            ])
                        ], style= {'width':'41vw','border-radius':'3%'})

def componentSuperficiesiembra(self):
        df = self.datasource.getFiltered_df()
        filtered =  df.dropna(axis=0, subset=['crop_date']) 
        groupF = filtered.groupby(["crop_date"]).agg(has=('has', 'sum')).reset_index()
        dates = groupF["crop_date"].values
        has = groupF["has"].values
        try:
            fig = px.line(x = dates, y = has, labels={"x": "Fecha de Siembra","y": "Superficie [ha]"})
            fig.update_layout(showlegend = True, margin = {"r":0,"t":0,"l":0,"b":0}, bargap = 0.05, paper_bgcolor = 'white', font_family = "Roboto", font_color = '#393d42', title_font_family = "Roboto", title_font_color = '#393d42', legend_title_font_color = '#393d42', plot_bgcolor = 'rgb(243, 243, 243)')
            fig.update_traces(hovertemplate = "Fecha de Siembra: %{x}<br>" + "Superficie: %{y:.2f} ha<br>", marker_color='#477442', marker=dict(opacity=0.8),font_family = "Roboto")
            return dbc.Card([
                        dbc.CardHeader(("Superficie por fecha de siembra"),style={'background-color':'#648A5F', 'border-radius':'3%', 'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                        dbc.CardBody(
                            [
                                dcc.Graph(
                                            figure=fig,
                                            id="chartSiembra"
                                        )
                            ])
                        ],style= {'width':'41vw','border-radius':'3%'})
        except:
            return dbc.Card([
                        dbc.CardHeader(("Superficie por fecha de siembra"), style = 
                                       {'background-color':'#648A5F',
                                        'border-radius':'3%',
                                        'color':'white',
                                        'font-weight': 'bold','font_family':"Roboto"}),
                        dbc.CardBody(
                        [
                                html.Div(["No hay datos suficientes para crear el grafico"])
                        ])
            ], style= {'width':'41vw','border-radius':'3%'})

def dropdownFarm(self):
    options = []
    options.append({"label":"Todos", "value":"Todos"})
    df = self.datasource.getFiltered_df()
    options = options + [{"label":farm, "value":farm} for farm in set(df["farmname"].values)]
    return dcc.Dropdown(
                            id = 'farms',
                            options = options,
                            clearable = False,
                            searchable = True,
                            placeholder = "Filtro por establecimiento",
                            style = {'width':'18vw','font_family':"Roboto"}
                       )
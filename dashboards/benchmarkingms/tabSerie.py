import dash_bootstrap_components as dbc
import dash_html_components as html 
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go

def tabTimeSerie(self):
    return html.Div([
                    html.Br(),                       
                    componentserieTemporal(self),
                    html.Br(),       
                    componentheatmap(self),
                    html.Br(),
                    componentdescriptionTS(self)], style={'width':'100%'})
def toggleST(self):          
    return dbc.Checklist(
                options=[
                    {"label": "Dias Despues de Siembra", "value": 1},
                        ],
                        id = "switches-input",
                        switch = True,
                        style = {'margin-left':'85vw','color':'black','font-size':'0.80vw','font_family':"Roboto"}
                )


def componentserieTemporal(self):
        df = self.datasource.getFiltered_df()
        labels, dates, ndvi = [], [], []
        for index, row in df.iterrows():
            for dateNDVI in row["seriendvi"]:
                labels = labels + ([row["name"]] * len(row["seriendvi"]))
                dates = dates + [datetime.strptime(ndvidate["date"], "%Y-%m-%d") for ndvidate in row["seriendvi"]]
                ndvi = ndvi + [float(ndvidate["value"]) for ndvidate in row["seriendvi"]]
            
        serie = pd.DataFrame.from_dict({'Fechas': dates, 'NDVI' : ndvi, 'Lotes' : labels})
        serie = serie.sort_values(by="Fechas")
        figSeries = px.line(serie, x = "Fechas", y = "NDVI", color = 'Lotes', color_discrete_sequence = px.colors.qualitative.Prism, range_y = ["0","1"])
        figSeries.update_traces(visible = "legendonly",mode="markers+lines", hovertemplate ='<br>Indice medio: %{y:.2f}'+'<br>Fecha: %{x}<br>')
        figSeries.update_layout(margin = dict(l = 35,r = 20,b = 20,t = 50,), height = 450,  paper_bgcolor = 'white', font_family = "Roboto", font_color = '#393d42', title_font_family = "Roboto", title_font_color = '#393d42', legend_title_font_color = '#393d42', plot_bgcolor = 'rgb(243, 243, 243)')
        figSeries.update_xaxes(title_font = dict(size = 15, family = 'Roboto', color = '#393d42'))       
        return  html.Div([
                            dbc.Card([
                            dbc.CardHeader(("Serie temporal"), style= {'background-color':'#648A5F', 'border-radius':'3%', 'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                            dbc.CardBody(
                            [
                                    dcc.Graph(
                                        figure = figSeries,
                                        id = "seriesgraph"
                                    )
                                ], style = {'border-radius':'3%'})
                            ])
                        ])  


def componentheatmap(self):
        labels, dates, ndvi = [], [], []
        df = self.datasource.getFiltered_df()
        dates = {}
        for index, row in df.iterrows():
            for ndvidate in row["seriendvi"]:
                if ndvidate["date"] not in dates:
                    dates[ndvidate["date"]] = {row["name"]:ndvidate["value"]}
                else:
                    if row['name'] not in dates[ndvidate["date"]]:
                        dates[ndvidate["date"]][row["name"]] = ndvidate["value"]
        datesdf = pd.DataFrame.from_dict(dates)
        datesdf = datesdf.interpolate(method ='linear', limit_direction = 'forward')
        datesdf = datesdf.reindex(sorted(datesdf.columns), axis=1)
        columns = datesdf.columns.tolist()
        
        dates = []
        ndvi = []
        labels = []
        for index, row  in datesdf.iterrows():
            dates = dates + columns
            labels = labels + [index] * len(columns)
            ndvi = ndvi + row.tolist()
            
        fig = go.Figure(data=go.Heatmap(
                        z=ndvi,
                        x=dates,
                        y=labels,
                        autocolorscale = False,
                        hoverongaps = False,
                        hovertemplate ='<br>Lote: %{y}<extra></extra>'+'<br>Indice medio: %{z:.2f}'+'<br>Fecha: %{x}<br>',
                        colorscale=[[0, "#000000"],[0.03, "#A0522D"],[0.07, "#94723C"],[0.1, "#a4824c"],[0.13, "#b4966c"],[0.17, "#c4baa4"],[0.2, "#94b614"],[0.25, "#80aa11"],[0.3, "#6c9f0e"],[0.35, "#58930c"],[0.4, "#448809"],[0.45, "#307d06"],[0.5, "#1c7204"],[0.55, "#467b2d"],[0.60, "#388457"],[0.65, "#2a8e81"],[0.7, "#1c97ab"],[0.75, "#0ea0d5"],[0.8, "#00aaff"],[0.85, "#157fdf"],[0.9, "#3343b2"],[0.95, "#3f2a9f"],[1, "#55007f"]],zmin=0,zmax=1),)
        fig.update_layout(margin=dict(l=50, r=0, b=10, t=20,),xaxis_nticks=36,hovermode = 'closest',paper_bgcolor='rgb(243, 243, 243)',plot_bgcolor='rgb(243, 243, 243)',showlegend=False,font_family="Roboto",font_color='#393d42',title_font_family="Roboto",title_font_color='#393d42',legend_title_font_color='#393d42',yaxis=dict(showgrid=True, zeroline=True, showticklabels=True),xaxis=dict(showgrid=True, zeroline=True, showticklabels=True)),
        fig.update_xaxes(title_font=dict(size = 15, family = 'Roboto', color='#393d42'),type = 'category')
          
        return  html.Div([
                  dbc.Card([
                        dbc.CardHeader(("Heatmap"), style={'background-color':'#648A5F', 'border-radius':'3%', 'color':'white','font-weight': 'bold','font-size':'0.80vw','font_family':"Roboto"}),
                        dbc.CardBody(
                        [
                                dcc.Graph(
                                    figure = fig,
                                    id = "headmap"
                                )
                        ],style = {'border-radius':'3%'})
                  ])])

def componentdescriptionTS(self):
        return html.Div([
                    dbc.Alert(
                                [
                                    "La serie temporal se utiliza para comparar la evolución o performance de un mismo cultivo en diferentes lotes de tu Espacio de Trabajo. Analizar el desarrollo del cultivo nos permite corroborar el impacto de cualquier incidencia o labor realizado, compararlo con otros lotes permite planificar el orden de cosecha o identificar buenas prácticas.",                                    
                                ],
                                    color="info",
                                    style={'background-color':'#F6C54C', 'opacity':'95%', 'color':'black', 'border-radius':'3%', 'margin-top': '1.5vw','font-size':'0.85vw','font_family':"Roboto"}
                            ),
                ])

                
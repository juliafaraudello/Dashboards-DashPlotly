import plotly.express as px
import pandas as pd
from math import nan
import plotly.graph_objects as go
import dash_core_components as dcc

def createMap(**args):
        api_token = open("dashboards/benchmarkingms/mapbox_token").read() # you will need your own token
        df = args['df']
        df = df.set_index("id")
        color_dict = {}

        if(args['type'] == 'ndvisum' or args['type'] == 'ndvistd'):
            color_dict["scale"]=  "Sunsetdark"
            color_dict["type"] = "continuous"
            color_dict["color"] = args['type']

        if(args['type'] == 'ndviavg'):
            color_dict["scale"] = [[0, "#000000"], [0.03, "#A0522D"], [0.07, "#94723C"], [0.1, "#a4824c"], [0.13, "#b4966c"],[0.17, "#c4baa4"],[0.2, "#94b614"],[0.25, "#80aa11"], [0.3, "#6c9f0e"], [0.35, "#58930c"], [0.4, "#448809"], [0.45, "#307d06"], [0.5, "#1c7204"], [0.55, "#467b2d"], [0.60, "#388457"],[0.65, "#2a8e81"],[0.7, "#1c97ab"],[0.75, "#0ea0d5"], [0.8, "#00aaff"], [0.85, "#157fdf"], [0.9, "#3343b2"], [0.95, "#3f2a9f"], [1, "#55007f"]]
            color_dict["type"] = "continuous"
            color_dict["color"] = args['type']

        if(args['type']== 'crop_color'):
            dict_crops = pd.Series(df["crop_color"].values, index = df["crop_name"].values).replace(nan,'#FFFFFF').to_dict()
            color_dict["scale"] = dict_crops
            color_dict["type"] = "discrete"
            color_dict["color"] = df['crop_name']

        fig = px.choropleth_mapbox(df,
                geojson = args['featuresCollection'], 
                color_continuous_scale = color_dict["type"] if 'continuous' in color_dict["scale"] else None, 
                color_discrete_map = color_dict["scale"] if 'discrete' in color_dict["type"] else None,
                locations = df.index, 
                featureidkey = "properties.id", 
                color = color_dict['color'], 
                zoom = 14.3, 
                center = args['centroid'])
        fig.update_geos(fitbounds = "locations", visible = False, projection_type = "mercator")
        fig.update_traces(hovertemplate= 
        "<b>Lote: %{properties.name} </b><br><br> Indice Acumulado: %{properties.ndvisum:.2f}" + 
        "<extra></extra>",marker  = dict(opacity = 0.5, line = dict(width = 3, color = '#F6C54C')))
        fig.update_layout(showlegend = True, mapbox_accesstoken = api_token, mapbox_style = "mapbox://styles/julifaraudello/ckrxkm2cq25k718qgq3j2sdi8", margin = {"r":0, "t":0, "l":0, "b":0}, height = 700,legend = dict(x=0.01, y=0.99, bgcolor = 'rgba(255,255,255,0.4)'),legend_title_text = 'Cultivo')
        return fig

       
def scatterChart(self, column):
        subject, score, nombreLotes= [], [], []
        for index, row in self.datasource.getFiltered_df().iterrows():
            subject.append(row["farmname"])
            score.append(row[column])
            nombreLotes.append(row["name"])
        data = [dict(
            type = 'scatter',
            x = subject,
            y = score,
            customdata = nombreLotes,
            mode = 'markers',
            marker=dict(symbol = 'star', size = 13, 
                        line = dict(color = 'white', width = 1.5),
                        color = '#3e703f'))]
        fig = go.Figure(data = data)
        fig.update_traces(
            hovertemplate = 'Lote: %{customdata} <br>Valor: %{y:.2f}<extra></extra>'
        )
        fig.update_layout(
            hoverlabel=dict(
                font_size = 16,
                font_family = "Roboto"
            ), margin=dict(l=0, r=0, b=0, t=0),font=dict(size=13)
        )
        return fig

def searchFarms(self):
    options = []
    options.append({"label":"Todos", "value":"Todos"})
    df = self.datasource.getFiltered_df()
    options = options + [{"label": farm, "value": farm} for farm in set(df["farmname"].values)]
    return dcc.Dropdown(
                            id = 'farms',
                            options = options,
                            clearable = False,
                            searchable = True,
                            placeholder = "Seleccione un establecimiento",
                            style = {'width':'14vw',
                                     'display':'block','font_family':"Roboto"}
                        )
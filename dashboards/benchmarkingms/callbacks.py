import dash
import urllib
import dash_html_components as html 
import dash_core_components as dcc
from dash.exceptions import PreventUpdate
from flask.globals import session
from dashboards.benchmarkingms import SharedComponent
from dashboards.benchmarkingms import tabDesvio
from dashboards.benchmarkingms import tabNDVIAcumulado
from dashboards.benchmarkingms import tabNDVIMedio
from dashboards.benchmarkingms import tabResume
from dashboards.benchmarkingms import tabSerie
from dashboards.benchmarkingms.helper import utils
from dashboards.benchmarkingms.DataSource import DataSource
import json

def sublist(lst1,lst2):
    for item in lst2:
        try:
            lst1.index(item)
        except ValueError:
            return False
        return True

def readS3File(token):
        infoLink = "https://dashinputdata.s3.amazonaws.com/dashboardMSinputdata/"+token+".json"
        downloadWSData = urllib.request.urlopen(infoLink).read()
        return json.loads(downloadWSData)


def defineGlobalcallback(self):
        
        @self.dash_app.callback(
            [
                dash.dependencies.Output("loadFields", "children"),
                dash.dependencies.Output("mapndvicrop", "figure")
            ],            
            [
                dash.dependencies.Input('farms', 'value'),
                dash.dependencies.Input({'type': 'filter-dropdown', 'index': dash.dependencies.ALL}, 'value')  
            ])
        def filter(farm, fieldsFilter):
            dfFiltered = self.datasource.resetFilters()
            ctx = dash.callback_context
            if not ctx.triggered:
                raise PreventUpdate
            else:
                if farm != 'Todos':
                    dfFiltered = self.datasource.resetFilters()
                    try:
                        if(len(fieldsFilter)!=0):
                            if(len(fieldsFilter[0])!=0):
                                df = self.datasource.resetFilters()
                                dfFiltered = df[df['farmname'] == farm] #filter by farm and check if fieldsFilter is subset of list of fields.
                                fields = list(set(dfFiltered["name"].values))
                                if (sublist(fields, fieldsFilter[0])):
                                    dfFiltered = dfFiltered[dfFiltered['name'].isin(fieldsFilter[0])]
                    except Exception as e:
                        print("Filter problem")
                        print(e)   
            self.datasource.setFilter(dfFiltered) 
            fields = list(set(dfFiltered["name"].values))
            options = [{"label":field, "value":field} for field in fields]
            map = SharedComponent.createMap(df = dfFiltered, featuresCollection = self.featuresCollection, type = "crop_color", centroid = utils().calcularCentroid(dfFiltered))    
            return  html.Div([
                            dcc.Dropdown(
                                    id={
                                        'type': 'filter-dropdown',
                                        'index': farm
                                    },
                                    value = fields,
                                    options = options,
                                    clearable = False,
                                    multi = True,
                                    searchable = True,
                            )]), map

       
        @self.dash_app.callback(
        dash.dependencies.Output("screen", "children"),
        [
            dash.dependencies.Input("resumenBT", "n_clicks"),
            dash.dependencies.Input("serietemporalBT", "n_clicks"),
            dash.dependencies.Input("avgBT", "n_clicks"),
            dash.dependencies.Input("IntegralBT", "n_clicks"),
            dash.dependencies.Input("desvioBT", "n_clicks"),
        ])
        def render(rs, ts, avbt, ibt, dbt):
            ctx = dash.callback_context
            changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
            
            if 'resumenBT' in changed_id:
                return tabResume.tabResumen(self)
            
            elif 'serietemporalBT' in changed_id:
                return tabSerie.tabTimeSerie(self)
            
            elif 'refreshDash' in changed_id:
                return tabResume.tabResumen(self)
            
            elif 'avgBT' in changed_id:
                return tabNDVIAcumulado.tabNDVI(self)
            
            elif 'IntegralBT' in changed_id:
                return tabNDVIMedio.tabRanking(self)
            
            elif 'desvioBT' in changed_id:
                return tabDesvio.tabDesvio(self)
            else:
                if 'token' in session:
                    self.datasource = DataSource(readS3File(session['token']))
                    self.df, self.featuresCollection = self.datasource.initDF_FC()
                return tabResume.tabResumen(self)
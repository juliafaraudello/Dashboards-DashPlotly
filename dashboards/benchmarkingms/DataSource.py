import requests
from threading import *
import geopandas as gpd
import numpy as np
import json

class getFarm:
    def __init__(self, **args):
        self.id = args['id']

    def get_result(self):
        self.urlApi = "https://huutfpyv75egfiat4e6jas5fym.appsync-api.us-west-2.amazonaws.com/graphql"
        self.header =  {"x-api-key": "da2-y3ywvj3f55g5bpb5v3xtyq6yye"}
        query = """
            query MyQuery {
                GetFarmInfo(FARMID: %s, lang: "es") {
                    id
                    name
                }
            } """ % self.id
        request = requests.post(self.urlApi, json={'query': query}, headers = self.header)
        self.result = request.json()
        return self.result


class getField(Thread):
    def __init__(self, **args):
        Thread.__init__(self)
        self.id = args['id']
        self.start_date = args['start_date']
        self.end_date = args['end_date']
        self.urlApi = "https://huutfpyv75egfiat4e6jas5fym.appsync-api.us-west-2.amazonaws.com/graphql"
        self.header = {"x-api-key": "da2-y3ywvj3f55g5bpb5v3xtyq6yye"}

    def run(self):
        query = """query MyQuery {
                    GetFieldInfo(FIELDID: %s, lang: "es", start_date: "%s", end_date: "%s") {
                        crop_id
                        geometry
                        geometryWKB
                        has
                        hybrid {
                            id
                            name
                        }
                        hybrid_id
                        id
                        crop_date
                        index {
                            date
                            dds
                            name
                            png
                            value
                            std
                        }
                        name
                        str_geojson_region
                        crop {
                            color
                            id
                            name
                        }
                    }
                    }
                    """ % (self.id, self.start_date , self.end_date)
        request = requests.post(self.urlApi, json={'query': query}, headers = self.header)
        self.result = request.json()

    def get_result(self):          
        Thread.join(self) # Wait for the thread to finish executing
        try:
            return self.result
        except Exception:
            return None

class DataSource:
    def __init__(self, input360):
        self.input = input360
        self.featuresCollection = None  #start without features collection
        self.filteredDF = gpd.GeoDataFrame([]) #this dataframe can be filtered.
        self.originalDF = gpd.GeoDataFrame([]) #this dataframe is inmutable.
        self.processes = self.processInput()

    def initDF_FC(self):
        rows, fc = [], {"type":"FeatureCollection", "features":[]}
        for process in self.processes:
            fieldData = process["process"].get_result()
            farmData = process["farm"]
            
            if fieldData["data"]["GetFieldInfo"] is not None:
                fieldData = fieldData["data"]["GetFieldInfo"]
                ws = "harcode"
                farmid = farmData["id"]
                crop_date = fieldData['crop_date']
                crop_name = fieldData['crop']['name']
                has = fieldData['has']
                farmname = farmData["name"]
                id = fieldData['id']  
                geometry = fieldData['geometry']
                name = fieldData['name']
                hibrido = fieldData['hybrid']['name']
                color = fieldData['crop']['color']
                crop_id = fieldData['crop']['id']
                seriendvi = fieldData['index']
                ndvipts = [pt["value"] for pt in seriendvi]
                ndvisum = np.sum(ndvipts)
                ndviavg = np.average(ndvipts)
                ndvistd = np.std(ndvipts)
                ndvimax = np.max(ndvipts)
                ndvimin = np.min(ndvipts)
                row = {'ws': ws,
                       'farmid': farmid,
                       'crop_date': crop_date,
                       'crop_color':color,
                       'crop_name' : crop_name,
                       'geometry': json.loads(geometry),
                       'has': has,
                       'farmname': farmname,
                       'id': id,
                       'name': name,
                       'hibrido': hibrido,
                       'seriendvi': seriendvi,
                       'color': color,
                       'crop_id': crop_id,
                       'ndvipts': ndvipts,
                       'ndvisum': ndvisum,
                       'ndviavg': ndviavg,
                       'ndvistd': ndvistd,
                       'ndvimax': ndvimax,
                       'ndvimin': ndvimin}
                feature = {}
                feature["type"] = "Feature"
                feature["geometry"] = json.loads(geometry)
                feature["properties"] = { "id" : id,
                                          "ndvisum" : ndvisum,
                                          "ndviavg" : ndviavg,
                                          "ndvistd": ndvistd,
                                          "name" : name,
                                          "crop_name" : crop_name,
                                          "crop_color" : color}
                fc["features"].append(feature)
                rows.append(row)
                
        self.filteredDF = gpd.GeoDataFrame(rows) #this dataframe can be filtered.
        self.originalDF = gpd.GeoDataFrame(rows) #this dataframe is inmutable.
        self.featuresCollection = fc
        return self.originalDF, self.featuresCollection

    def setFilter(self, df):
        self.filteredDF = df
        return self.filteredDF

    def resetFilters(self): #This method reset the DF to the original one.
        self.filteredDF = self.originalDF.copy()
        return self.filteredDF

    def getOrigin_df(self):
        return self.originalDF

    def getFeaturesCollection(self):
        return self.featuresCollection

    def getFiltered_df(self):
        return self.filteredDF

    def processInput(self):
        start_date = self.input['start_date']
        end_date = self.input['end_date']
        processes = []
        for farm in self.input["Farms"]:
            farmData = getFarm(id = farm["id"]).get_result()
            try:
                farmData = farmData["data"]["GetFarmInfo"]
                for field in farm["fieldFilters"]:
                    process = getField(id = field, start_date = start_date, end_date = end_date)
                    process.start()
                    processes.append({"process": process, "farm": {"name": farmData["name"], "id": farmData["id"]}})
            except:
                print("Error")
        return processes
import geopandas
import shapely
import json

class utils:        
    def calcularCentroid(self, df = None):
        if(len(df)==0) : return {"lat":0, "lon":0}
        featuresCollection  =  {"type":"FeatureCollection", "features":[]}
        for index, row in df.iterrows():
            feature = {}
            feature["type"]= "Feature"
            feature["geometry"] = row["geometry"]
            feature["properties"] = {"id":row["id"], "name":row["name"]}
            featuresCollection["features"].append(feature)
        element = geopandas.GeoDataFrame.from_features(featuresCollection["features"])
        element = shapely.geometry.mapping(element["geometry"].centroid[0])["coordinates"]
        lat = element[1]
        lon = element[0]
        return {"lat":lat, "lon":lon}

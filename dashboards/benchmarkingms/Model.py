class farmModel:
    def __init__(self,**args):
        self.name = args.get('name', None)
        self.id = args.get('id', None)

class loteModel:
    def __init__(self, **args):
        self.crop_id = args.get('crop_id', None)
        self.cropdate = args.get('cropdate', None)
        self.geometry = args.get('geometry', None)
        self.has = args.get('has', None)
        self.geometryWKB = args.get('geometryWKB', None)
        self.hybrid = args.get('hybrid', None)
        self.name = args.get('name', None)
        self.id = args.get('id', None)
        
    @property
    def crop_id(self):
        return self._crop_id

    @crop_id.setter
    def crop_id(self,value):
        self._crop_id = value

    @property
    def cropdate(self):
        return self._cropdate

    @cropdate.setter
    def cropdate(self,value):
        self._cropdate = value
    
    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self,value):
        self._geometry = value

    @property
    def has(self):
        return self._has

    @has.setter
    def has(self,value):
        self._has = value

    @property
    def geometryWKB(self):
        return self._geometryWKB

    @geometryWKB.setter
    def geometryWKB(self,value):
        self._geometryWKB = value

    @property
    def hybrid(self):
        return self._hybrid

    @hybrid.setter
    def hybrid(self,value):
        self._hybrid = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def id(self):
        return self._id
        
    @id.setter
    def id(self, value):
        self._id = value
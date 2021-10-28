"""
Mock common arcpy
"""
from typing import Union, List
from unittest.mock import MagicMock
from .geometries import Geometry

# pylint: disable=C0103,R0913,R0902,R0903


class MockArcpyArray:
    """
    Mock for an arcpy array
    """
    # pylint: disable=C0103,R0913
    def __init__(self, points: Union[None, List]=None):
        if points:
            self._points = points
        else:
            self._points = list()

    def __iter__(self):
        return iter(self._points)

    def add(self, point):
        """Adds a point or array object to the end of the array"""
        self._points.append(point)

    def append(self, point):
        """Appends an object to the array in the last position."""
        self._points.append(point)

    def getObject(self, index):
        """Returns the object at the given index position in the array."""
        return self._points[index]

    @property
    def count(self):
        """ The element count of the array. Integer"""
        return len(self._points)


class MockArcpyCursor:
    """
    Mock for an arcpy cursor
    """
    def __init__(self, featclass=None, fields=None):
        self.fields = fields
        self.featclass = featclass
        self.features = []
        self.insertRow = MagicMock()
        self.insertRow.side_effect = self.insert_row


    def insert_row(self, row):
        """add a feature"""
        if row[len(row) - 1] is None:
            raise ValueError("arcpy error insertRow")
        if self.featclass and self.featclass.fields:
            if isinstance(row[-1], Geometry):
                if len(self.featclass.fields) != (len(row) -1):
                    raise ValueError("arcpy error insertRow invalid number of fields")
                    # now check the fields. We don't want any string values going into doubles as this
                    # can cause parse errors when in Norwegian/Norway settings
            for i, field in enumerate(self.featclass.fields):
                if field.type == 'DOUBLE':
                    if type(row[i]) is not float:
                        message = "Error floats must be parsed before inserting into cursors to prevent issues " \
                                  "when parsing data under Norwegian settings. " \
                                  "Field '{0}' has a type of {1}".format(field.name, type(row[i]))
                        raise Exception(message)

        self.features.append(row)

    def getObject(self, index):
        """
        Returns the object at the given index position in the array.
        this is not on the cursor, just used for testing
        DW I regret adding this the mock shouldn't have different methods to the
        real class. What was I thinking?! Please don't use it
        """
        return self.features[index]



class Editor:
    """
    Mock for an arcpy editor
    """
    # pylint: disable=C0103,R0913,too-few-public-methods
    def __init__(self, featclass=None):
        self.featclass = featclass
        # allows is to count calls to start/stop editing
        self.stopEditing = MagicMock()
        self.startEditing = MagicMock()


class Parameter:
    """
    Mock for parameters
    """
    # pylint: disable=C0103,R0913,too-few-public-methods
    def __init__(self, **kwargs):
        self.displayName = kwargs.get("displayName", '')
        self.name = kwargs.get("name", '')
        self.datatype = kwargs.get("datatype", 'String')
        self.parameterType = kwargs.get("parameterType", 'Required')
        self.direction = kwargs.get("direction", 'Input')
        self.filter = Filter()
        self.filters = []
        self._value = ""
        self.valueAsText = ""
        self.errorMessage = ""
        self.warningMessage = ""
        self._columns = []
        self.altered = True
        self.hasBeenValidated = False
        self.enabled = True
        self._values = []

    @property
    def value(self):
        """
        This simple class doesn't really support value, it is just text
        it needs to set the value as text to the same when it is updated
        """
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self.valueAsText = val

    @property
    def values(self)-> List[str]:
        """
        This simple class doesn't really support values, it is just text
        returns the list of filters
        """
        if len(self._values) > 0:
            return self._values
        return self.filter.list

    @values.setter
    def values(self, val):
        self._values = val

    @property
    def columns(self):
        return self._columns

    @columns.setter
    def columns(self, val):
        self._columns = val
        for col in self._columns:
            self.filters.append(Filter())

    def setErrorMessage(self, message):
        """Mock set error"""
        self.errorMessage = message

    def setWarningMessage(self, message):
        """Mock set warning"""
        self.warningMessage = message

    def hasError(self):
        return self.errorMessage != ""

    def hasWarning(self):
        return self.warningMessage != ""


class Filter:
    """parameter filter"""
    def __init__(self):
        self.list = []
        self.type = ""


class MockDescribe:
    """
    mock the describe object.
    this will need expanding
    """
    def __init__(self, obj):
        self.fidset = ""
        self.shapeType = "Polygon"
        self.catalogPath = obj
        self.noDataValue = -9999
        self.hasM = False
        self.name = "MockedName"
        self.spatialReference = MockSpatialReference()
        self.fields = []
        if type(obj) is MockFeatureClass:
            self.fields = obj.fields


class MockSpatialReference:
    """
    mocks a sr. at present only takes a limited codes
    and allows strings to be returned
    """
    def __init__(self, code=0):
        self.factoryCode = code
        self.linearUnitName = "Meter"
        self.name = "WGS_1984_Web_Mercator_Auxiliary_Sphere"
        self.projectionCode = code

    def exportToString(self):
        # pylint: disable=line-too-long
        """ sr as string """
        if self.factoryCode == 102100:
            s_prj = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]];-20037700 -30241100 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"  # noqa
        elif self.factoryCode == 23029:
            s_prj = "PROJCS['ED_1950_UTM_Zone_29N',GEOGCS['GCS_European_1950',DATUM['D_European_1950',SPHEROID['International_1924',6378388.0,297.0]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-9.0],PARAMETER['Scale_Factor',0.9996],PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]];-5121200 -9998400 10000;-100000 10000;-100000 10000;0.001;0.001;0.001;IsHighPrecision"  # noqa
        else:
            s_prj = 'PROJCS["ED_1950_UTM_Zone_31N",GEOGCS["GCS_European_1950",DATUM["D_European_1950",SPHEROID["International_1924",6378388.0,297.0]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",3.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]'  # noqa
        return s_prj

    def loadFromString(self, str_prj):
        """load string prj"""
        if "WGS_1984_Web_Mercator_Auxiliary_Sphere" in str_prj:
            self.factoryCode = 102100
        elif "ED_1950_UTM_Zone_31N" in str_prj:
            self.factoryCode = 23031
        elif "ED_1950_UTM_Zone_29N" in str_prj:
            self.factoryCode = 23029

    def __eq__(self, other):
        """
        Define equality method

        :param other:
        :return:
        """
        if self.factoryCode == other.factoryCode:
            return True
        else:
            return False


class MockField:
    """
    mock an arcpy field
    """
    def __init__(self, aliasName="", name="", field_type=""):
        self.aliasName = aliasName
        self.name = name
        self.type = field_type


# noinspection PyPep8Naming
class MockArcGISProject:
    def __init__(self):
        self.homeFolder = "c:\\temp"
        self.activeMap = MockArcGISMap()

    def listMaps(self):
        return [MockArcGISMap(), MockArcGISMap()]


# noinspection PyPep8Naming,PyMethodMayBeStatic
class MockArcGISMap:
    def __init__(self):
        pass

    def insertLayer(self, lyr, lyr2):
        pass

    def removeLayer(self, lyr):
        pass

    def addDataFromPath(self, path):
        return MagicMock()

    def addLayer(self, layer):
        return MagicMock()

    def listLayers(self, name):
        return MagicMock()

    def addLayerToGroup(self, group_layer, layer):
        pass


class MockLayer:
    def listLayers(self):
        return [MagicMock()]

    def save(self):
        pass

class GetCount_management():
    def __init__(self, in_fc):
        pass

    @staticmethod
    def getOutput(self):
        return 1


def ValidateFieldName(name, workspace=None):
    return name


class messages():
    @staticmethod
    def addMessage(message):
        print(message)

    @staticmethod
    def addErrorMessage(message):
        print(message)

    @staticmethod
    def addWarningMessage(message):
        print(message)


class MockRaster:
    def __init__(self):
        pass

    @staticmethod
    def save(self):
        pass


class MockFeatureClass:
    def __init__(self, out_path=None, out_name=None,
                 geometry_type=None, template=None, has_m=None, has_z=None, spatial_reference=None):
        self.out_path = out_path
        self.out_name = out_name
        self.geometry_type = geometry_type
        self.template = template
        self.has_m = has_m
        self.has_z = has_z
        self.spatial_reference = spatial_reference

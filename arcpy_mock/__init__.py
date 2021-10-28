"""
Mock out arcpy and add some functions.
"""
import sys
from unittest.mock import Mock, MagicMock

from .geometries import Multipoint, Point, Polyline, Polygon
from .mock_arcpy import MockArcpyArray, MockArcpyCursor, Editor, Parameter, MockDescribe, \
    MockSpatialReference, GetCount_management, ValidateFieldName, MockArcGISProject, MockLayer, MockFeatureClass, \
    MockField

arcpy = Mock()  # pylint: disable=invalid-name
arcpy.Point = Point
arcpy.Multipoint = Multipoint
arcpy.Polyline = Polyline
arcpy.Polygon = Polygon
arcpy.Array = MockArcpyArray
arcpy.da.InsertCursor = MagicMock().side_effect = lambda fc, f: MockArcpyCursor(fc, f)

arcpy.da.Editor = Editor
arcpy.GetInstallInfo = lambda: {"Version": "2.5.3"}
arcpy.Parameter = Parameter
arcpy.Describe = MockDescribe

arcpy.ListTransformations = lambda a, b: ['123', '456']
arcpy.SpatialReference = MockSpatialReference
arcpy.GetCount_management = lambda fc: GetCount_management
arcpy.ValidateFieldName = ValidateFieldName
arcpy.mp.ArcGISProject = lambda a: MockArcGISProject()
arcpy.mp.LayerFile = lambda a: MockLayer()
arcpy.CreateScratchName = lambda a, data_type, workspace: r"c:\temp\da"
arcpy.CheckExtension = lambda a: "Available"
arcpy.CreateFeatureclass_management = lambda a, b, c, d, e, f, g: MockFeatureClass(a, b, c, d, e, f, g)
arcpy.ValidateTableName = lambda a, b="": a


def AddFields_management(fc, flist):
    out = []
    for item in flist:
        out.append(MockField(item[0], item[2], item[1]))
    fc.fields = out


def ListFields(fc):
    if fc is None:
        return []
    if fc.fields:
        return fc.fields


arcpy.ListFields = ListFields

arcpy.AddFields_management = AddFields_management

def enable():
    """replace arcpy"""
    sys.modules['arcpy'] = arcpy

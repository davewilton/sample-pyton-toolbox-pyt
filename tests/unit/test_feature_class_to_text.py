import arcpy
from pathlib import Path
from unittest.mock import MagicMock


from tools.feature_class_to_text_tool import ExportFeatureClassToTextWorker

addin_dir = str(Path(Path(__file__)).parent.parent.parent)
source_dir = str(Path(Path(__file__)).parent)


def test_format_point():
    mock_point = arcpy.Point(368263.800100, 468263.800100, 10.1)
    s_point = ExportFeatureClassToTextWorker.format_point(mock_point)
    assert s_point == "368263.800100 468263.800100 10.100000"

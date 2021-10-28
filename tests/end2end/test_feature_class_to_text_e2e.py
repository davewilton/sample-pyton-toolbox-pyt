import filecmp
from pathlib import Path

import arcpy
import pytest

from tools.feature_class_to_text_tool import FeatureClassToTextTool

addin_dir = str(Path(Path(__file__)).parent.parent.parent)
source_dir = str(Path(Path(__file__)).parent)


def add_toolbox():
    arcpy.env.overwriteOutput = True
    arcpy.AddToolbox(addin_dir + r"/sample-addin.pyt")


@pytest.mark.parametrize('toolbox', [True, False])
def test_parameters_export(toolbox: bool):

    input_fc = source_dir + r"\Fixtures\test_data.gdb\polygonFC"
    out_file = source_dir + r"\Output\output.txt"
    params = [input_fc, out_file]

    if toolbox:
        add_toolbox()
        arcpy.SampleAddin.FeatureClassToTextTool(input_fc, out_file)
    else:
        tool = FeatureClassToTextTool()
        tool.execute(params, None)

    expected = source_dir + r"\Expected\polygonFC.txt"
    assert Path(out_file).exists()
    assert filecmp.cmp(out_file, expected)


# same test running multiple inputs and outputs

inputs = [
    [
        source_dir + r"\Fixtures\test_data.gdb\polygonFC",
        source_dir + r"\Output\output.txt",
        source_dir + r"\Expected\polygonFC.txt"
     ],
    [
        source_dir + r"\Fixtures\test_data.gdb\polylineFC",
        source_dir + r"\Output\output.txt",
        source_dir + r"\Expected\polylineFC.txt"
    ]
]


@pytest.mark.parametrize('input_fc, out_file, expected', inputs)
def test_parameters_export_multiple(input_fc, out_file, expected):

    add_toolbox()
    arcpy.SampleAddin.FeatureClassToTextTool(input_fc, out_file)

    assert Path(out_file).exists()
    assert filecmp.cmp(out_file, expected)

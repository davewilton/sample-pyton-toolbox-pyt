from typing import Dict, Any, List

import arcpy

from tools.util import get_param_as_text, write_message
from .feature_class_to_text_worker import ExportFeatureClassToTextWorker


# noinspection PyMethodMayBeStatic
class FeatureClassToTextTool:
    """The base class for the exporter"""

    label = 'Feature Class To Text'
    description = "A longer description"
    category = "sub folder"
    export_geometries = ["POLYLINE", "POLYGON"]

    # noinspection PyPep8Naming
    def getParameterInfo(self):
        """
        *ArcPy required. Do not rename.*
        """

        # Input fc
        param_in = arcpy.Parameter(
            displayName="Input features",
            name="input_fc",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        param_in.filter.list = self.export_geometries

        # output file
        param_out = arcpy.Parameter(
            displayName="Output file",
            name="output_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")

        params = [param_in, param_out]

        return params

    def parse_parameters(self, parameters: List[arcpy.Parameter]) -> Dict[str, Any]:
        """
        Get values for parameters to pass to exporters as named dictionary
        Named parameters are much easier to work with that using the array of parameters

        :param parameters: arcpy parameters
        :return: dict providing kwargs for exporters
        """
        input_fc = get_param_as_text(parameters[0])
        output_file = get_param_as_text(parameters[1])
        return {
            'input_fc': input_fc,
            'output_file': output_file,
        }

    # noinspection PyPep8Naming
    def isLicensed(self) -> bool:
        """
        *ArcPy required. Do not rename.*

        Set whether tool is licensed to execute.

        :return: True if Licensed, False if not.
        """
        return True

    # noinspection PyPep8Naming
    def updateMessages(self, parameters) -> None:
        """
        *ArcPy required. Do not rename.*
        Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

    def execute(self, parameters: List[arcpy.Parameter], messages) -> None:
        """
        Execute the tool.

        :param parameters:
        :param messages:
        :return:
        """
        try:

            parsed_params = self.parse_parameters(parameters)
            worker = ExportFeatureClassToTextWorker(  # type: ignore
                    messages,
                    **parsed_params
                )
            worker.execute()

        except Exception as ex:
            write_message(messages, "An unknown error occurred:: " + str(ex), 2)

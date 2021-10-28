from tools.feature_class_to_text_tool import FeatureClassToTextTool

class Toolbox(object):
    """The main toolbox"""
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the.pyt file)."""
        self.label = "sample python addin"
        self.alias = "SampleAddin"  # this will be the name of the tool for use in python/cli

        self.tools = [FeatureClassToTextTool]

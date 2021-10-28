import arcpy


class ExportFeatureClassToTextWorker:
    """
    Exporter to text
    """

    def __init__(self, messages, input_fc: str, output_file: str) -> None:
        """Define the tool (tool name is the name of the class)."""
        self.message = messages
        self.input_fc = input_fc
        self.output_file = output_file
        self.exported_features = 0 # count the features

    def execute(self) -> None:
        """
        Export to CPS3 Culture format
        """
        with open(self.output_file, "w", encoding="utf-8") as f:
            # don't know what the header means apart from the last line means no data value
            f.write('Header\n')

            features = self.fc_to_geom_arr(self.input_fc)
            self.exported_features = len(features)
            for i, feat in enumerate(features, 1):
                f.write("->{0}\n".format(i))
                for pnt in feat:
                    f.write(self.format_point(pnt) + "\n")

        self.exported_features = i

    @staticmethod
    def format_point(pnt) -> str:
        """
        Format the point into a string

        :param pnt: input point
        :return: space delimited point values
        """
        return "{:.6f} {:.6f} {:.6f}".format(pnt.X, pnt.Y, 0 if pnt.Z is None else pnt.Z)

    @staticmethod
    def fc_to_geom_arr(fc):
        """
        takes a feature class and turns it into an array. Deals with donuts/multi-part
        by making them separate features. This is used by culture exports
        :param fc:
        :return:
        """

        feature_array = []
        for feat_count, row in enumerate(arcpy.da.SearchCursor(fc, ["SHAPE@"])):
            geom = row[0]
            if geom is not None:
                for part in geom:
                    coord_arr = []
                    for coord_counter, pnt in enumerate(part):
                        if pnt is not None:
                            coord_arr.append(pnt)
                        else:
                            feature_array.append(coord_arr)
                            coord_arr = []

            feature_array.append(coord_arr)

        return feature_array

from cicada.preprocessing.convert_to_nwb import ConvertToNWB
import yaml
import numpy as np
import os

def read_cell_type_categories_yaml_file(yaml_file, using_multi_class):
    """
    Read cell type categories from a yaml file. If more than 2 type cells are given, then a multi-class
    classifier will be used. If 2 type cells are given, then either it could be multi-class or binary classifier,
    then this choice should be given in the parameters of CinacModel.
    If 2 cell-type are given, for binary classifier, it should be precised which cell type should be predicted
    if we get more than 0.5 probability.
    Args:
        yaml_file:
        using_multi_class: int, give the default parameters used

    Returns: cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg
    cell_type_from_code_dict: dict, key is an int, value is the cell_type
    cell_type_to_code_dict: dict, key is a string, value is the code of the cell_type. A code can have more than one
    string associated, but all of them represent the same cell_type defined in cell_type_from_code_dict
    multi_class_arg: is None if no multi_class_arg was given in the yaml_file, True or False, if False means we want
    to use a binary classifier

    """

    cell_type_from_code_dict = dict()
    cell_type_to_code_dict = dict()

    with open(yaml_file, 'r') as stream:
        yaml_data = yaml.load(stream, Loader=yaml.FullLoader)

    multi_class_arg = None
    n_cell_categories = 0
    category_code_increment = 0
    # sys.stderr.write(f"{analysis_args_from_yaml}")
    for arg_name, args_content in yaml_data.items():
        if arg_name == "config":
            if isinstance(args_content, dict):
                if "multi_class" in args_content:
                    multi_class_arg = bool(args_content["multi_class"])

        if arg_name == "cell_type_categories":
            n_cell_categories = len(args_content)
            # if multi_class == 1, then we need a predicted_cell_type which will have the value 1
            predicted_cell_type = None
            if (multi_class_arg is None and using_multi_class == 1) or (multi_class_arg is False):
                for cell_type_category, category_dict in args_content.items():
                    if "predicted_celll_type" in category_dict:
                        predicted_cell_type = cell_type_category
            for cell_type_category, category_dict in args_content.items():
                if (predicted_cell_type is not None) and (predicted_cell_type == cell_type_category) and \
                        (n_cell_categories <= 2):
                    cell_type_from_code_dict[1] = cell_type_category
                    cell_type_code = 1
                else:
                    cell_type_from_code_dict[category_code_increment] = cell_type_category
                    cell_type_code = category_code_increment
                    category_code_increment += 1
                    if (category_code_increment == 1) and (predicted_cell_type is not None) and \
                            (n_cell_categories <= 2):
                        category_code_increment += 1
                cell_type_to_code_dict[cell_type_category] = cell_type_code
                if "keywords" in category_dict:
                    for keyword in category_dict["keywords"]:
                        cell_type_to_code_dict[keyword] = cell_type_code

    return cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg


class ConvertCellTypeToNWB(ConvertToNWB):
    """Class to convert Calcium Imaging movies to NWB"""
    def __init__(self, nwb_file):
        """
        Initialize some parameters
        Args:
             nwb_file (NWB.File) : NWB file object
        """
        super().__init__(nwb_file)
        # array of length the number of cell, and value an int representing a cell type
        self.cell_type_codes = None
        # array of length the number of cell, and value a string representing a cell type
        self.cell_type_names = None

    def convert(self, **kwargs):
        """Convert the data and add to the nwb_file

        Args:
            **kwargs: arbitrary arguments
        """
        super().convert(**kwargs)

        # ### setting parameters ####
        cell_type_predictions_file = kwargs.get("cell_type_predictions_file", None)

        if cell_type_predictions_file is None:
            print(f"No cell type predictions file in {self.__class__.__name__}")
            return

        predictions_threshold = kwargs.get("predictions_threshold", 0.5)

        cell_type_config_file = kwargs.get("cell_type_config_file", None)
        if cell_type_config_file is None:
            print(f"No cell type config file in {self.__class__.__name__}")
            return

        cell_type_predictions = np.load(cell_type_predictions_file)
        binary_cell_type_predictions = np.zeros(cell_type_predictions.shape, dtype="int8")
        binary_cell_type_predictions[cell_type_predictions > predictions_threshold] = 1

        cell_type_from_code_dict, cell_type_to_code_dict, multi_class_arg = \
            read_cell_type_categories_yaml_file(yaml_file=cell_type_config_file, using_multi_class=2)

        # cell_type_from_code_dict: key int representing the code of the cell type, value str representing the cell type
        # print(f"ConvertCellTypeToNWB cell_type_from_code_dict {cell_type_from_code_dict}")

        # cell_type_to_code_dict: has a key cell type name and as value their code (int).
        # Several names can have the same code
        # print(f"ConvertCellTypeToNWB cell_type_to_code_dict {cell_type_to_code_dict}")

        self.cell_type_codes = []
        # array of length the number of cell, and value a string representing a cell type
        self.cell_type_names = []

        for cell_index in np.arange(len(cell_type_predictions)):
            # if the code is superior to the number of code, then it means the cell type is unknown
            code = cell_type_predictions.shape[1]
            for code_index in np.arange(cell_type_predictions.shape[1]):
                if cell_type_predictions[cell_index, code_index] == 1:
                    code = code_index

            self.cell_type_codes.append(code)
            self.cell_type_names.append(cell_type_from_code_dict.get(code, "unknown"))

        # need to be an uint8 type to be put in NWB
        self.cell_type_codes = np.asarray(self.cell_type_codes, dtype="uint8")
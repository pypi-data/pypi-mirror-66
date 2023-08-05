from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.display.cells_map_utils import CellsCoord, get_coords_from_caiman_format_file
import sys
from time import sleep, time
import os
import numpy as np
import matplotlib.cm as cm
from cicada.utils.display.colors import BREWER_COLORS
import matplotlib.colors as plt_colors
from cicada.utils.cell_assemblies.malvache.utils import load_cell_assemblies_data
from cicada.utils.display.videos import load_tiff_movie


class CicadaSplittingCellsAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Splitting cells", family_id="Pre-processing",
                                short_description="Split cells' contours",
                                long_description="When a specific segmentation has been done (for ex Gad-cre), allows "
                                                 "remove from a more general segmentation so cells",
                                config_handler=config_handler)

    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        super().check_data()

        if self._data_format != "nwb":
            self.invalid_data_help = "Non NWB format compatibility not yet implemented"
            return False

        if len(self._data_to_analyse) != 1:
            self.invalid_data_help = "This analysis works only if 1 session is selected"
            return False

        for data in self._data_to_analyse:

            segmentations = data.get_segmentations()

            # we need at least one segmentation
            if (segmentations is None) or len(segmentations) == 0:
                self.invalid_data_help = "No segmentation data available"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_segmentation_arg_for_gui()

        segmentation_file_arg = {"arg_name": "segmentation_data_file", "value_type": "file",
                                 "extensions": ["mat", "npz"],
                                 "mandatory": True,
                                 "short_description": "File containing the segmentation to extract",
                                 "long_drescription": "So far only CaImAn type of format is accepted"}
        self.add_argument_for_gui(**segmentation_file_arg)

        self.add_choices_arg_for_gui(arg_name="extracted_cell_type", choices=["interneuron", "pyramidal"],
                                     default_value="interneuron", short_description="Cell type of the extracted cell",
                                     multiple_choices=False,
                                     family_widget="cell_type")

        self.add_choices_arg_for_gui(arg_name="other_cell_type", choices=["interneuron", "pyramidal"],
                                     default_value="pyramidal", short_description="Cell type of the other cells",
                                     multiple_choices=False,
                                     family_widget="cell_type")

        # TODO: Add choices regarding the format, also a checkbox for the matlab indexing

        matlab_indexation_arg = {"arg_name": "matlab_indexation", "value_type": "bool",
                                 "default_value": False, "short_description": "Matlab indexation ?"}

        self.add_argument_for_gui(**matlab_indexation_arg)

        remove_loaded_one_arg = {"arg_name": "remove_loaded_one", "value_type": "bool",
                                 "default_value": True, "short_description":
                                     "Remove cells that has been loaded ? ",
                                 "long_description": "If set to False, it means the cells already in the session "
                                                     "file will be removed from the one loaded."}

        self.add_argument_for_gui(**remove_loaded_one_arg)

        max_dist_bw_centroids_arg = {"arg_name": "max_dist_bw_centroids", "value_type": "int",
                                     "min_value": 1, "max_value": 10,
                                     "long_description": "Max distance between 2 centroids in pixels",
                                     "default_value": 3, "short_description": "Max distance between 2 centroids",
                                     "family_widget": "image_format"}

        self.add_argument_for_gui(**max_dist_bw_centroids_arg)

        invert_xy_coord_arg = {"arg_name": "invert_xy_coord", "value_type": "bool",
                               "default_value": True, "short_description": "Invert xy coords",
                               "long_description": "Could be useful if the coordinates are inverted,"
                                                   " do it for the loaded contours"}

        self.add_argument_for_gui(**invert_xy_coord_arg)

        verbose_arg = {"arg_name": "verbose", "value_type": "bool",
                       "default_value": True, "short_description": "Verbose",
                       "long_description": "If selected, some information might be printed during the analysis."}

        self.add_argument_for_gui(**verbose_arg)

    def update_original_data(self):
        """
        To be called if the data to analyse should be updated after the analysis has been run.
        :return: boolean: return True if the data has been modified
        """
        pass

    def run_analysis(self, **kwargs):
        """
        test
        :param kwargs:
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        n_sessions = len(self._data_to_analyse)

        segmentation_dict = kwargs['segmentation']

        matlab_indexation = kwargs["matlab_indexation"]

        remove_loaded_one = kwargs["remove_loaded_one"]

        max_dist_bw_centroids = kwargs["max_dist_bw_centroids"]

        invert_xy_coord = kwargs.get("invert_xy_coord", True)

        verbose = kwargs.get("verbose", True)

        extracted_cell_type = kwargs.get("extracted_cell_type")

        other_cell_type = kwargs.get("other_cell_type")

        dpi = kwargs.get("dpi", 200)

        session_data = self._data_to_analyse[0]
        session_identifier = session_data.identifier
        if verbose:
            print(f"-------------- {session_identifier} -------------- ")
        if isinstance(segmentation_dict, dict):
            segmentation_info = segmentation_dict[session_identifier]
        else:
            segmentation_info = segmentation_dict
        pixel_mask = session_data.get_pixel_mask(segmentation_info=segmentation_info)

        if pixel_mask is None:
            print(f"pixel_mask not available in for {session_data.identifier} "
                  f"in {segmentation_info}")
            self.update_progressbar(self.analysis_start_time, 100)
            return

        # pixel_mask of type pynwb.core.VectorIndex
        # each element of the list will be a sequences of tuples of 3 floats representing x, y and a float between
        # 0 and 1 (not used in this case)
        pixel_mask_list = [pixel_mask[cell] for cell in range(len(pixel_mask))]
        # TODO: get the real movie dimensions if available
        cells_coord = CellsCoord(pixel_masks=pixel_mask_list, from_matlab=False, invert_xy_coord=False)
        if verbose:
            print(f"N cells: {cells_coord.n_cells}")

        segmentation_data_file = kwargs["segmentation_data_file"]
        coords_loaded = get_coords_from_caiman_format_file(file_name=segmentation_data_file)
        cells_coord_loaded = CellsCoord(coords=coords_loaded, from_matlab=matlab_indexation,
                                        invert_xy_coord=invert_xy_coord)

        if not remove_loaded_one:
            # then we exchange
            cells_coord_loaded_tmp = cells_coord_loaded
            cells_coord_loaded = cells_coord
            cells_coord = cells_coord_loaded_tmp

        contours_mapping = cells_coord.match_cells_indices(cells_coord_loaded,
                                                           max_dist_bw_centroids=max_dist_bw_centroids,
                                                           path_results=self.get_results_path(),
                                                           plot_result=True,
                                                           plot_title_opt=session_identifier,
                                                           take_the_biggest=True)
        cells_to_remove = []

        for cell_mapped in contours_mapping:
            if cell_mapped < 0:
                # meaning the cell from the data loaded has no match
                continue
            cells_to_remove.append(cell_mapped)
        # print(f"len(contours_mapping) {len(contours_mapping)}")

        cell_type_predictions = np.zeros((cells_coord.n_cells, 2), dtype='int8')
        if extracted_cell_type == "interneuron":
            cell_type_predictions[np.array(cells_to_remove), 0] = 1
            cell_type_predictions[:, 1] = 1
            cell_type_predictions[np.array(cells_to_remove), 1] = 0
        else:
            cell_type_predictions[np.array(cells_to_remove), 1] = 1
            cell_type_predictions[:, 0] = 1
            cell_type_predictions[np.array(cells_to_remove), 0] = 0
        np.save(os.path.join(self.get_results_path(), f"{session_identifier}_cell_type_predictions.npy"),
                cell_type_predictions)

        # cells_to_remove correspond to the cell extracted

        new_cells_coord = cells_coord.remove_cells(cells_to_remove=cells_to_remove)
        print(f"new_cells_coord.n_cells  {new_cells_coord.n_cells}")
        file_name = os.path.join(self.get_results_path(), f"{session_identifier}_new_cells_coord")
        new_cells_coord.save_coords(file_name=file_name)

        # cells_coord.plot_cells_map(path_results=self.get_results_path(),
        #                            data_id=session_identifier, show_polygons=show_polygons,
        #                            fill_polygons=fill_polygons,
        #                            use_pixel_masks=use_pixel_masks,
        #                            title_option=title_option, connections_dict=None,
        #                            use_welsh_powell_coloring=(not cell_assemblies_on) and
        #                                                      use_welsh_powell_coloring,
        #                            verbose=verbose,
        #                            cells_groups=cells_groups,
        #                            cells_groups_colors=cells_groups_colors,
        #                            img_on_background=avg_cell_map_img,
        #                            real_size_image_on_bg=real_size_image_on_bg,
        #                            cells_groups_edge_colors=None,
        #                            with_edge=True, cells_groups_alpha=None,
        #                            dont_fill_cells_not_in_groups=dont_fill_cells_not_in_groups,
        #                            with_cell_numbers=with_cell_numbers, save_formats=save_formats,
        #                            dpi=dpi,
        #                            save_plot=True, return_fig=False, **args_to_add)

        if verbose:
            print(" ")
        self.update_progressbar(self.analysis_start_time, 100)

        print(f"Cells map analysis run in {time() - self.analysis_start_time} sec")

from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.graphs.utils_graphs import build_connectivity_graphs
from cicada.utils.graphs.utils_graphs import detect_hub_cells
import os
import networkx as nx


class CicadaHubsAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        A list of
        :param data_to_analyse: list of data_structure
        :param family_id: family_id indicated to which family of analysis this class belongs. If None, then
        the analysis is a family in its own.
        :param data_format: indicate the type of data structure. for NWB, NIX
        """
        super().__init__(name="Hub cells", family_id="Connectivity",
                         short_description="Find out about hub cells", config_handler=config_handler)

    def check_data(self):
        """
        Check the data given one initiating the class and return True if the data given allows the analysis
        implemented, False otherwise.
        :return: a boolean
        """
        super().check_data()

        # self.invalid_data_help = "Not implemented yet"
        # return False

        if self._data_format != "nwb":
            self.invalid_data_help = "Non NWB format compatibility not yet implemented"
            return False

        for data_to_analyse in self._data_to_analyse:
            roi_response_series = data_to_analyse.get_roi_response_series()
            if len(roi_response_series) == 0:
                self.invalid_data_help = f"No roi response series available in " \
                                         f"{data_to_analyse.identifier}"
                return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use", long_description=None)

        self.add_int_values_arg_for_gui(arg_name="time_delay", min_value=100, max_value=1500,
                                        short_description="Time delay in ms to look for connected cells ",
                                        default_value=500, family_widget="figure_config_delay")

        self.add_bool_option_for_gui(arg_name="save_graphs", true_by_default=True,
                                     short_description="Save graph",
                                     family_widget="figure_config_data")

        self.add_int_values_arg_for_gui(arg_name="prctile_connection_intra_session", min_value=1, max_value=100,
                                        short_description="Minimal degree of intra-session connectivity of a hub cell (%)",
                                        default_value=5, family_widget="figure_config_threshold")

        self.add_int_values_arg_for_gui(arg_name="prctile_of_higly_connected_inter_session", min_value=1, max_value=100,
                                        short_description="Top connected cells inter-session (%)",
                                        long_description="The cell has to be in the 'value' % most connected cells",
                                        default_value=15, family_widget="figure_config_threshold")

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
        :return:
        """

        CicadaAnalysis.run_analysis(self, **kwargs)

        verbose = kwargs.get("verbose", True)

        roi_response_series_dict = kwargs["roi_response_series"]

        time_delay = kwargs.get("time_delay")

        save_graphs = kwargs.get("save_graphs")

        path_results = self.get_results_path()

        prctile_connection_intra_session = kwargs.get("prctile_connection_intra_session")

        prctile_of_higly_connected_inter_session = kwargs.get("prctile_of_higly_connected_inter_session")

        print("Hubs detection: coming soon...")

        # Create saving folder for graphs if necessary
        tmp_path = os.path.dirname(path_results)
        folder_to_save_graphs = "Connectivity_graphs"
        path_to_graphs = os.path.join(f'{tmp_path}', f'{folder_to_save_graphs}')
        if os.path.isdir(path_to_graphs) is False:
            os.mkdir(path_to_graphs)
            if verbose:
                print(f"No directory found to save the graphs, create directory at : {path_to_graphs}")
        else:
            if verbose:
                print(f"Folder to save graph already here, save the graphs in : {path_to_graphs}")

        out_connectivity_graphs_dict = dict()
        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            session_identifier = session_data.identifier
            animal_id = session_data.subject_id
            animal_age = int(session_data.age)
            animal_weight = session_data.weight

            if verbose:
                print(f" ------------ ONGOING SESSION: {session_identifier}---------------")

            # Get Data
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            # Get Data Timestamps
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps) - 1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            [n_cells, n_frames] = raster_dur.shape

            samp_r = n_frames / duration_s

            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            # Get Cell-type Data
            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)
            pyramidal_indexes = cell_indices_by_cell_type.get('pyramidal', [])
            interneuron_indexes = cell_indices_by_cell_type.get('interneuron', [])
            n_ins = len(interneuron_indexes)
            n_pyr = len(pyramidal_indexes)

            # Building Cell-type list
            cell_type_list = []
            for cell in range(n_cells):
                cell_type_list.append("Unclassified")
            for pyramide in range(n_pyr):
                tmp_ind = pyramidal_indexes[pyramide]
                cell_type_list[tmp_ind] = "Pyramidal"
            for interneuron in range(n_ins):
                tmp_ind = interneuron_indexes[interneuron]
                cell_type_list[tmp_ind] = "Interneuron"

            # Check if graphs are already built
            filename = session_identifier + "_connectivity_graphs"
            path_to_graph_in_graphml = os.path.join(f'{path_to_graphs}', f'{filename}_in.graphml')
            path_to_graph_out_graphml = os.path.join(f'{path_to_graphs}', f'{filename}_out.graphml')

            files_check = [os.path.isfile(path_to_graph_in_graphml), os.path.isfile(path_to_graph_out_graphml)]

            if all(files_check) is True:
                if verbose:
                    print(f"All graphs files are already computed, just load them")
                graph_in = nx.read_graphml(path=path_to_graph_in_graphml, node_type=int)
                graph_out = nx.read_graphml(path=path_to_graph_out_graphml, node_type=int)
            else:
                if verbose:
                    print(f"Graphs files are not found")
                    print(f"Starting to build the connectivity graphs")
                [graph_in, graph_out] = build_connectivity_graphs(raster_dur, sampling_rate=samp_r,
                                                                  time_delay=time_delay,
                                                                  save_graphs=save_graphs,
                                                                  path_results=path_to_graphs,
                                                                  filename=session_identifier + "_connectivity_graphs",
                                                                  with_timestamp_in_file_name=False,
                                                                  verbose=verbose)
                if verbose:
                    print(f"Connectivity graphs are built")

            out_connectivity_graphs_dict[session_identifier] = graph_out

        if verbose:
            print(f"---------- NOW LOOK FOR HUB CELLS WITH CRITERIA BASED ON ALL SELECTED SESSIONS ----------")

        hubs_dict = detect_hub_cells(graphs_to_analyse=out_connectivity_graphs_dict,
                                     cell_connectivity_threshold=prctile_connection_intra_session,
                                     top_connected_cells=prctile_of_higly_connected_inter_session,
                                     verbose=verbose)

        if verbose:
            print(f"Analysis done: Hub-cells are")
            print(f"{hubs_dict}")


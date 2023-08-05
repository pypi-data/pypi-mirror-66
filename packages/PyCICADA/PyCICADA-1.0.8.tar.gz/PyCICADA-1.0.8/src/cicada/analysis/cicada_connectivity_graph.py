from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
import numpy as np
from cicada.utils.graphs.utils_graphs import build_connectivity_graphs
from cicada.utils.graphs.utils_graphs import plot_graph
from cicada.utils.graphs.utils_graphs import plot_connectivity_graphs
import os
import networkx as nx
import matplotlib.colors


class CicadaConnectivityGraph(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """

        CicadaAnalysis.__init__(self, name="Connectivity graph", family_id="Connectivity",
                                short_description="Build connectivity graph", config_handler=config_handler)

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

        self.add_bool_option_for_gui(arg_name="plot_them_all", true_by_default=True,
                                     short_description="Do a figure with all graphs",
                                     family_widget="figure_config_data")

        self.add_bool_option_for_gui(arg_name="do_plot_graphs", true_by_default=True,
                                     short_description="Plot the graphs",
                                     family_widget="figure_config_data")

        self.add_bool_option_for_gui(arg_name="specify_ins", true_by_default=True,
                                     short_description="Highlight interneurons",
                                     family_widget="figure_config_data")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_edgecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure edge color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes label color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="ticks_labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes ticks labels color",
                                   long_description=None, family_widget="figure_config_color")

        policies = ["Arial", "Cambria", "Rosa", "Times", "Calibri"]
        self.add_choices_arg_for_gui(arg_name="font_type", choices=policies,
                                     default_value="Arial", short_description="Font type",
                                     multiple_choices=False,
                                     family_widget="figure_config_label")

        weights = ["light", "normal", "bold", "extra bold"]
        self.add_choices_arg_for_gui(arg_name="fontweight", choices=weights,
                                     default_value="normal", short_description="Font Weight",
                                     multiple_choices=False,
                                     family_widget="figure_config_label")

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

        start_time = time()

        roi_response_series_dict = kwargs["roi_response_series"]

        verbose = kwargs.get("verbose", True)

        time_delay = kwargs.get("time_delay")

        save_graphs = kwargs.get("save_graphs")

        do_plot_graphs = kwargs.get("do_plot_graphs")

        plot_them_all = kwargs.get("plot_them_all")

        fig_facecolor = kwargs.get("fig_facecolor")
        figure_facecolor = matplotlib.colors.to_hex(fig_facecolor, keep_alpha=False)

        fig_edgecolor = kwargs.get("fig_edgecolor")
        figure_edgecolor = matplotlib.colors.to_hex(fig_edgecolor, keep_alpha=False)

        background_color = kwargs.get("background_color")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        path_results = self.get_results_path()

        print("Connectivity graphs: coming soon...")
        n_sessions = len(self._data_to_analyse)

        if verbose:
            print(f"{n_sessions} sessions to analyse")

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

        session_id_list = []
        fig_facecolor_list = [[] for session in range(n_sessions)]
        for session_index, session_data in enumerate(self._data_to_analyse):
            session_identifier = session_data.identifier
            session_id_list.append(session_identifier)
            specify_ins = kwargs.get("specify_ins")

            if verbose:
                print(f" ------------ ONGOING SESSION: {session_identifier}---------------")

            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict
            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps)-1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            [n_cells, n_frames] = raster_dur.shape

            samp_r = n_frames / duration_s

            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                   roi_response_serie_info)

            pyramidal_indexes = cell_indices_by_cell_type.get('pyramidal', [])
            interneuron_indexes = cell_indices_by_cell_type.get('interneuron', [])
            n_ins = len(interneuron_indexes)
            n_pyr = len(pyramidal_indexes)
            if specify_ins and n_ins > 1:
                figure_facecolor = ["#a9a7a7" for neuron in range(n_cells)]
                for pyramide in range(n_pyr):
                    tmp_index = pyramidal_indexes[pyramide]
                    figure_facecolor[tmp_index] = "#435fec"
                for interneuron in range(n_ins):
                    tmp_index = interneuron_indexes[interneuron]
                    figure_facecolor[tmp_index] = "#e9473f"
            else:
                figure_facecolor = figure_facecolor

            fig_facecolor_list[session_index] = figure_facecolor

            # Check if graphs are already built
            filename = session_identifier + "_connectivity_graphs"
            path_to_graph_in_graphml = os.path.join(f'{path_to_graphs}', f'{filename}_in.graphml')
            path_to_graph_out_graphml = os.path.join(f'{path_to_graphs}', f'{filename}_out.graphml')
            # path_to_graph_in_gexf = os.path.join(f'{path_to_graphs}', f'{filename}_in.gexf')
            # path_to_graph_out_gexf = os.path.join(f'{path_to_graphs}', f'{filename}_out.gexf')

            files_check = [os.path.isfile(path_to_graph_in_graphml), os.path.isfile(path_to_graph_out_graphml)]

            if all(files_check) is True:
                if verbose:
                    print(f"All graphs files are already computed, just load them")
                graph_in = nx.read_graphml(path=path_to_graph_in_graphml, node_type=int)
                graph_out = nx.read_graphml(path=path_to_graph_out_graphml, node_type=int)
                # graph_in = nx.read_gexf(path=path_to_graph_in_gexf, node_type=int)
                # graph_out = nx.read_gexf(path=path_to_graph_out_gexf, node_type=int)
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

            if do_plot_graphs:
                if verbose:
                    print(f"Plot Out-connectivity graph")
                plot_graph(graph_out,  with_fa2=False, randomized_positions=True,
                           filename=session_identifier + "_connectivity_graph_out", iterations=2000,
                           node_color=figure_facecolor, edge_color=figure_edgecolor, background_color=background_color,
                           with_labels=False, title=session_identifier + "  Out-connectivity", ax_to_use=None,
                           save_formats=save_formats, save_figure=save_figure,
                           path_results=self.get_results_path(),
                           with_timestamp_in_file_name=with_timestamps_in_file_name)
                if verbose:
                    print(f"Plot In-connectivity graph")
                plot_graph(graph_in, with_fa2=False, randomized_positions=True,
                           filename=session_identifier + "_connectivity_graph_in", iterations=2000,
                           node_color=figure_facecolor, edge_color=figure_edgecolor, background_color=background_color,
                           with_labels=False, title=session_identifier + "  In-connectivity", ax_to_use=None,
                           save_formats=save_formats, save_figure=save_figure,
                           path_results=self.get_results_path(),
                           with_timestamp_in_file_name=with_timestamps_in_file_name)

            self.update_progressbar(start_time, 100 / n_sessions)

        if plot_them_all:
            if verbose:
                print(f"Plotting figure with all graphs")
            plot_connectivity_graphs(session_id_list, connectivity_type="in", graph_files_path=path_to_graphs,
                                     background_color=background_color,
                                     node_color=fig_facecolor_list, edge_color=figure_edgecolor,
                                     size_fig=(width_fig, height_fig),
                                     save_formats=save_formats, save_figure=save_figure,
                                     path_results=self.get_results_path(),
                                     with_timestamp_in_file_name=with_timestamps_in_file_name)

            plot_connectivity_graphs(session_id_list, connectivity_type="out", graph_files_path=path_to_graphs,
                                     background_color=background_color,
                                     node_color=fig_facecolor_list, edge_color=figure_edgecolor,
                                     size_fig=(width_fig, height_fig),
                                     save_formats=save_formats, save_figure=save_figure,
                                     path_results=self.get_results_path(),
                                     with_timestamp_in_file_name=with_timestamps_in_file_name)

from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.graphs.utils_graphs import build_connectivity_graphs
from time import time
from datetime import datetime
import os
import numpy as np
import networkx as nx
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class CicadaConnectivityGraphsDescription(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """

        CicadaAnalysis.__init__(self, name="Connectivity graphs description", family_id="Connectivity",
                                short_description="Give basic stats on graphs", config_handler=config_handler)

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
                                        default_value=500, family_widget="figure_config_graph")

        self.add_bool_option_for_gui(arg_name="save_graphs", true_by_default=True,
                                     short_description="Save graph",
                                     family_widget="figure_config_graph")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in tables",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figures",
                                     family_widget="figure_config_saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_density", choices=representations,
                                     default_value="bar",
                                     short_description="Plot to use for 'Graph-density' figure",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        x_ax = ["Age", "SubjectID", "Session"]
        self.add_choices_arg_for_gui(arg_name="x_axis_density", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_density", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_density", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_density_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_connectivity", choices=representations,
                                     default_value="box",
                                     short_description="Plot to use for 'Connectivity' figure",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Celltype"]
        self.add_choices_arg_for_gui(arg_name="x_axis_connectivity", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_connectivity", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_connectivity", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_connectivity_config_representation")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="label_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes label color",
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

        self.add_int_values_arg_for_gui(arg_name="axis_label_size", min_value=1, max_value=100,
                                        short_description="Font size",
                                        default_value=18, family_widget="figure_config_label")

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

        save_table = kwargs.get("save_table")

        x_axis_name_density = kwargs.get("x_axis_density")

        kind_density = kwargs.get("representation_density")

        hue_density = kwargs.get("hue_density")

        palette_density = kwargs.get("palettes_density")

        x_axis_name_connectivity = kwargs.get("x_axis_connectivity")

        kind_connectivity = kwargs.get("representation_connectivity")

        hue_connectivity = kwargs.get("hue_connectivity")

        palette_connectivity = kwargs.get("palettes_connectivity")

        fig_facecolor = kwargs.get("fig_facecolor")

        background_color = kwargs.get("background_color")

        labels_color = kwargs.get("label_color")

        axis_color = kwargs.get("axis_color")

        font_size = kwargs.get("axis_label_size", 20)

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        path_results = self.get_results_path()

        print("Connectivity graphs description: coming soon...")
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

        graph_density_table = pd.DataFrame()
        global_single_cell_info_table = pd.DataFrame()
        for session_index, session_data in enumerate(self._data_to_analyse):
            # Get Session Info
            session_identifier = session_data.identifier
            animal_id = session_data.subject_id
            animal_age = int(session_data.age)
            animal_weight = session_data.weight

            if verbose:
                print(f"------------------ ONGOING SESSION: {session_identifier} -------------------- ")

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
            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")
            samp_r = n_frames / duration_s

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

            if verbose:
                print(f"Get some statistics of the graph")

            # 1/ Get graph density and build table for density across ages (each row of the table is a session)
            graph_density = nx.density(graph_out)
            graph_density = graph_density * 100
            sum_up_data = {'Age': animal_age, 'Weight': animal_weight, 'SubjectID': animal_id,
                           'Session': session_identifier, 'GraphDensity': [graph_density]}
            data_frame = pd.DataFrame(sum_up_data)
            graph_density_table = graph_density_table.append(data_frame, ignore_index=True)

            # 2/ Describe graph at single cell level
            connectivity_degree_list = []
            ins_in_connected_cells_list = []
            pyr_in_connected_cells_list = []
            connected_ins_in_ins_list = []
            connected_pyr_in_pyr_list = []
            for cell in range(n_cells):
                # info 1: degree of connectivity of each cell
                neighbors_list = list(graph_out.neighbors(cell))
                n_neighbors = len(neighbors_list)
                percentage_connections = (n_neighbors / n_cells) * 100
                connectivity_degree_list.append(percentage_connections)

                # Use cell-type information
                n_ins_connected = len(np.intersect1d(neighbors_list, interneuron_indexes))
                n_pyr_connected = len(np.intersect1d(neighbors_list, pyramidal_indexes))

                # info 2: proportion of connected pyramidal cells and INs among the connected cells
                if n_neighbors > 0 and n_ins > 0:
                    ins_in_connected_cells = (n_ins_connected / n_neighbors) * 100
                else:
                    ins_in_connected_cells = 'NA'
                if n_neighbors > 0 and n_pyr > 0:
                    pyr_in_connected_cells = (n_pyr_connected / n_neighbors) * 100
                else:
                    pyr_in_connected_cells = 'NA'
                ins_in_connected_cells_list.append(ins_in_connected_cells)
                pyr_in_connected_cells_list.append(pyr_in_connected_cells)

                # info 3: proportion of connected pyramidal cells and INs among the 2 cell population
                if n_ins > 0:
                    connected_ins_in_ins = (n_ins_connected / n_ins) * 100
                else:
                    connected_ins_in_ins = 'NA'
                if n_pyr > 0:
                    connected_pyr_in_pyr = (n_pyr_connected / n_pyr) * 100
                else:
                    connected_pyr_in_pyr = 'NA'
                connected_ins_in_ins_list.append(connected_ins_in_ins)
                connected_pyr_in_pyr_list.append(connected_pyr_in_pyr)

            # Build the table (in the table each row is a cell)
            age_list = [animal_age for k in range(n_cells)]
            weight_list = [animal_weight for k in range(n_cells)]
            if animal_weight is None:
                weight_list = ["N.A." for k in range(n_cells)]
            session_identifier_list = [session_identifier for k in range(n_cells)]
            animal_id_list = [animal_id for k in range(n_cells)]
            single_cell_info_dict = {'Age': age_list, 'Weight': weight_list, 'SubjectID': animal_id_list,
                                     'Session': session_identifier_list, 'Celltype': cell_type_list,
                                     'DegreeofConnectivity': connectivity_degree_list,
                                     'InterneuronsInConnected': ins_in_connected_cells_list,
                                     'PyramideInConnected': pyr_in_connected_cells_list,
                                     'Connected-INs-in-INs': connected_ins_in_ins_list,
                                     'Connected-pyramide_in-pyramide': connected_pyr_in_pyr_list}

            single_cell_info_table = pd.DataFrame(single_cell_info_dict)
            global_single_cell_info_table = global_single_cell_info_table.append(single_cell_info_table,
                                                                                 ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        if save_table:
            if verbose:
                print(f"----------------------------------- SAVINGS --------------------------------------")
            path_results = self.get_results_path()
            path_table_xls = os.path.join(f'{path_results}', f'graphs_density_table.xlsx')
            path_table_csv = os.path.join(f'{path_results}', f'graphs_density_table.csv')
            path_cell_table_xls = os.path.join(f'{path_results}', f'cell_connectivity_table.xlsx')
            path_cell_table_csv = os.path.join(f'{path_results}', f'cell_connectivity_table.csv')
            if save_table:
                graph_density_table.to_excel(path_table_xls)
                graph_density_table.to_csv(path_table_csv)
                global_single_cell_info_table.to_excel(path_cell_table_xls)
                global_single_cell_info_table.to_csv(path_cell_table_csv)
                if verbose:
                    print(f"Data save as excel and csv files")

        # Do the plots
        if save_table:
            if verbose:
                print(f"------------------------------ DO SOME PLOTTING ---------------------------------")

        # Do the graph density plot according to GUI requirements
        if hue_density == "None":
            hue_density = None
            palette_density = None

        ylabel = "Graph density % of all possible connections (%)"

        filename = "graph_density_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)

        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_density, y="GraphDensity", hue=hue_density, data=graph_density_table,
                          hue_order=None, kind=kind_density, orient=None, color=fig_facecolor, palette=palette_density,
                          ax=ax1)
        ax1.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
        ax1.yaxis.label.set_color(labels_color)
        ax1.xaxis.label.set_color(labels_color)
        ax1.spines['left'].set_color(axis_color)
        ax1.spines['right'].set_color(background_color)
        ax1.spines['bottom'].set_color(background_color)
        ax1.spines['top'].set_color(background_color)
        ax1.yaxis.set_tick_params(labelsize=font_size)
        ax1.xaxis.set_tick_params(labelsize=font_size)
        ax1.tick_params(axis='y', colors=axis_color)
        ax1.tick_params(axis='x', colors=axis_color)

        fig.tight_layout()
        if save_figure and (path_results is not None):
            # transforming a string in a list
            if isinstance(save_formats, str):
                save_formats = [save_formats]
            time_str = ""
            if with_timestamp_in_file_name:
                time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")

            for save_format in save_formats:
                if not with_timestamp_in_file_name:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
                else:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
        plt.close()

        # Do the degree of connectivity plot according to GUI requirements
        if hue_connectivity == "None":
            hue_connectivity = None
            palette_connectivity = None

        ylabel = "Degree of cell-connectivity (%)"

        filename = "connectivity_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_connectivity, y="DegreeofConnectivity", hue=hue_connectivity,
                          data=global_single_cell_info_table, hue_order=None, kind=kind_connectivity,
                          orient=None, color=fig_facecolor, palette=palette_connectivity, ax=ax1)

        ax1.set_ylabel(ylabel, fontsize=font_size, labelpad=20, fontweight=fontweight, fontfamily=fontfamily)
        ax1.yaxis.label.set_color(labels_color)
        ax1.xaxis.label.set_color(labels_color)
        ax1.spines['left'].set_color(axis_color)
        ax1.spines['right'].set_color(background_color)
        ax1.spines['bottom'].set_color(background_color)
        ax1.spines['top'].set_color(background_color)
        ax1.yaxis.set_tick_params(labelsize=font_size)
        ax1.xaxis.set_tick_params(labelsize=font_size)
        ax1.tick_params(axis='y', colors=axis_color)
        ax1.tick_params(axis='x', colors=axis_color)

        fig.tight_layout()
        if save_figure and (path_results is not None):
            # transforming a string in a list
            if isinstance(save_formats, str):
                save_formats = [save_formats]
            time_str = ""
            if with_timestamp_in_file_name:
                time_str = datetime.now().strftime("%Y_%m_%d.%H-%M-%S")
            for save_format in save_formats:
                if not with_timestamp_in_file_name:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
                else:
                    fig.savefig(os.path.join(f'{path_results}', f'{filename}{time_str}.{save_format}'),
                                format=f"{save_format}",
                                facecolor=fig.get_facecolor())
        plt.close()

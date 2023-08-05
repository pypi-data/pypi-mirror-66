from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from datetime import datetime
from cicada.utils.misc import get_continous_time_periods
from cicada.utils.misc import give_unique_id_to_each_transient_of_raster_dur
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.signal as sci_si
from cicada.utils.sce_stats_utils import get_sce_threshold
from cicada.utils.stats import multiple_comparison_one_factor_effect
import pandas as pd
import os


class CicadaSceDescritpionAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="SCE description", family_id="Descriptive statistics",
                                short_description="Basic SCE statistics", config_handler=config_handler)

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

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=10000,
                                        short_description="Number of surrogates raster to compute SCE threshold",
                                        default_value=100, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="percentile", min_value=95, max_value=100,
                                        short_description="Percentile of surrogate distribution to compute SCE threshold",
                                        default_value=99, family_widget="figure_config_surrogate")

        methods = ["Peaks", "All frames"]
        self.add_choices_arg_for_gui(arg_name="method", choices=methods,
                                     default_value="peaks", short_description="Method used to detect SCEs",
                                     long_description="If 'Peaks': find SCEs using find-peaks with parameters below, "
                                                      "SCE will be define by a single frame. "
                                                      "If 'All frames': define SCEs as all continuous frame periods"
                                                      " with more active cells than the statistical threshold.",
                                     multiple_choices=False,
                                     family_widget="figure_config_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="min_sce_distance", min_value=1, max_value=10,
                                        short_description="Minimal number of frames between 2 SCEs",
                                        default_value=5, family_widget="figure_config_findpeaks")

        time_unity = ["seconds", "minutes"]
        self.add_choices_arg_for_gui(arg_name="time_unit", choices=time_unity,
                                     default_value="minutes", short_description="Time unit for SCE frequency",
                                     multiple_choices=False,
                                     family_widget="figure_config_time")

        self.add_bool_option_for_gui(arg_name="do_stats", true_by_default=True,
                                     short_description="Try statistical tests",
                                     family_widget="figure_config_stats")

        self.add_int_values_arg_for_gui(arg_name="pvalue", min_value=1, max_value=5,
                                        short_description="p-value (%) for statistical test",
                                        default_value=5, family_widget="figure_config_stats")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in tables",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figures",
                                     family_widget="figure_config_saving")

        cell_types = ["All_cells", "Pyramidal_cells", "Interneurons"]
        self.add_choices_arg_for_gui(arg_name="cell_to_use", choices=cell_types,
                                     default_value="All_cells",
                                     short_description="Cell-type to use for 'in-SCE spike ratio'",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_ratio", choices=representations,
                                     default_value="box",
                                     short_description="Plot to use for 'in-SCE spike ratio' figure",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Celltype"]
        self.add_choices_arg_for_gui(arg_name="x_axis_ratio", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_ratio", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_ratio", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_ratio_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_recruitment", choices=representations,
                                     default_value="box", short_description="Plot to use for 'SCE recruitment' figure",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        x_ax = ["Age", "SubjectID", "Session"]
        self.add_choices_arg_for_gui(arg_name="x_axis_recruitment", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_recruitment", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_recruitment", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_recruitment_config_representation")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation_amplitude", choices=representations,
                                     default_value="box",
                                     short_description="Plot to use for 'SCE transient amplitude' figure",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        x_ax = ["Age", "SubjectID", "Session"]
        self.add_choices_arg_for_gui(arg_name="x_axis_amplitude", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "None"]
        self.add_choices_arg_for_gui(arg_name="hue_amplitude", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes_amplitude", choices=palettes,
                                     default_value="muted", short_description="Color palette for subgroups",
                                     long_description="In that case figure facecolor and figure edgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_amplitude_config_representation")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description="Useless if a 'hue' is specified, in that case use 'palette'",
                                   family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(1, 1, 1, 1.),
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
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        roi_response_series_dict = kwargs["roi_response_series"]

        n_surrogates = kwargs.get("n_surrogates")

        percentile = kwargs.get("percentile")

        method = kwargs.get("method")

        min_sce_distance = kwargs.get("min_sce_distance")

        time_unit = kwargs.get("time_unit")

        do_stats = kwargs.get("do_stats")

        pvalue = kwargs.get("pvalue")
        pvalue = pvalue / 100

        verbose = kwargs.get("verbose", True)

        cell_to_use = kwargs.get("cell_to_use")

        x_axis_name_ratio = kwargs.get("x_axis_ratio")

        kind_ratio = kwargs.get("representation_ratio")

        hue_ratio = kwargs.get("hue_ratio")

        palette_ratio = kwargs.get("paletttes_ratio")

        x_axis_name_recruitment = kwargs.get("x_axis_recruitment")

        kind_recruitment = kwargs.get("representation_recruitment")

        hue_recruitment = kwargs.get("hue_recruitment")

        palette_recruitment = kwargs.get("paletttes_recruitment")

        x_axis_name_amplitude = kwargs.get("x_axis_amplitude")

        kind_amplitude = kwargs.get("representation_amplitude")

        hue_amplitude = kwargs.get("hue_amplitude")

        palette_amplitude = kwargs.get("paletttes_amplitude")

        background_color = kwargs.get("background_color")

        fig_facecolor = kwargs.get("fig_facecolor")

        labels_color = kwargs.get("axes_label_color")

        axis_color = kwargs.get("axis_color")

        font_size = kwargs.get("axis_label_size", 20)

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_figure = True

        save_table = kwargs.get("save_table")

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()
        print("SCE description: coming soon...")
        n_sessions = len(self._data_to_analyse)

        if verbose:
            print(f"{n_sessions} sessions to analyse")

        gobal_spike_ratio_data_table = pd.DataFrame()
        gobal_sce_recruitment_data_table = pd.DataFrame()
        global_sce_transient_amplitude_data_table = pd.DataFrame()
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
            spike_nums_dur_numbers = give_unique_id_to_each_transient_of_raster_dur(raster_dur)

            [n_cells, n_frames] = raster_dur.shape
            if verbose:
                print(f"N cells: {n_cells}, N frames: {n_frames}")

            trace_neuronal_data = session_data.get_roi_response_serie_data_by_keyword(keys=roi_response_serie_info[:-1],
                                                                                      keyword="trace")
            for key, data in trace_neuronal_data.items():
                traces = trace_neuronal_data.get(key)

            for trace_index, trace in enumerate(traces):
                traces[trace_index] = (trace - np.mean(trace)) / np.std(trace)

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

            # Check Data with respect to the specific analysis
            if n_ins == 0 and cell_to_use == "Interneurons":
                if verbose:
                    print(f"No Interneurons identified in this session: "
                          f"cannot use 'only interneurons'.")
                    print(f"Skipping {session_identifier} session for analysis")
            if n_pyr == 0 and cell_to_use == "Pyramidal_cells":
                if verbose:
                    print(f"No Pyramidal cells identified in this session: "
                          f"cannot use 'only pyramidal'.")
                    print(f"Skipping {session_identifier} session for analysis")

            # Get the SCE locations : 2 options to define SCE #
            sum_active_cells = np.sum(raster_dur, axis=0)
            sce_thresh = get_sce_threshold(raster_dur, n_surrogates=n_surrogates, percentile=percentile,
                                           verbose=verbose)[1]

            # With 'peaks' method: SCE are at a single frame which is the peak of synchrony
            if verbose:
                print(f"Detection of SCEs location using the {method} method")
            if method == "Peaks":
                sce_times = sci_si.find_peaks(sum_active_cells, height=sce_thresh, distance=min_sce_distance)[0]
                n_sce = len(sce_times)
                if verbose:
                    print(f"Minimal distance between 2 SCEs: {min_sce_distance} frames")
                    print(f"SCE detection found: {n_sce} SCEs")
                cells_in_sce = raster_dur[:, sce_times]
                cell_transient_in_sce = np.ones((n_cells, n_sce), dtype=int)
                cell_transient_in_sce = cell_transient_in_sce * (-1)
                for cell in range(n_cells):
                    for sce in range(n_sce):
                        if cells_in_sce[cell, sce] == 1:
                            cell_transient_in_sce[cell, sce] = spike_nums_dur_numbers[cell, sce_times[sce]]

            # With 'all frames' method: SCE are at all frames with more co-active cells is higher than the threshlold
            if method == "All frames":
                sce_times = np.array(np.where(sum_active_cells >= sce_thresh)[0])
                sce_times_bool = np.zeros(n_frames, dtype="bool")
                sce_times_bool[sce_times] = True
                sce_periods = get_continous_time_periods(sce_times_bool)
                n_sce = len(sce_periods)
                if verbose:
                    print(f"SCE detection found: {len(sce_periods)} SCEs")
                cells_in_sce = np.zeros((n_cells, n_sce), dtype=int)
                cell_transient_in_sce = np.ones((n_cells, n_sce), dtype=int)
                cell_transient_in_sce = cell_transient_in_sce * (-1)
                for cell in range(n_cells):
                    for sce in range(n_sce):
                        if sce_periods[sce][0] < sce_periods[sce][1]:
                            cells_in_sce[cell, sce] = np.max(raster_dur[cell, sce_periods[sce][0]: sce_periods[sce][1]])
                            cell_transient_in_sce[cell, sce] = \
                                np.max(spike_nums_dur_numbers[cell, sce_periods[sce][0]: sce_periods[sce][1]])
                        else:
                            cells_in_sce[cell, sce] = raster_dur[cell, sce_periods[sce][0]]
                            cell_transient_in_sce[cell, sce] = spike_nums_dur_numbers[cell, sce_periods[sce][0]]

            # Get 'cells_in_sce' matrices for pyramidal cells or interneurons only #
            pyramide_in_sce = cells_in_sce[pyramidal_indexes, :]
            interneuron_in_sce = cells_in_sce[interneuron_indexes, :]

            # Print SCE frequency #
            sce_frequeny_second = n_sce / duration_s
            sce_frequeny_minute = n_sce / duration_m

            if time_unit == "seconds":
                sce_frequeny = sce_frequeny_second
            else:
                sce_frequeny = sce_frequeny_minute

            if verbose:
                print(f"SCE frequency is: {sce_frequeny} SCEs / {time_unit}")

            # PART 1 :Get the 2 ratios spikes in SCE / total spikes and spike out SCE / total spikes #
            if verbose:
                print(f"Computing in-SCE and out-SCE spikes / total spike ratios for each cell")
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1
            n_spikes = np.sum(raster, axis=1)
            if verbose:
                print(f"N cells without spike: {len(np.where(n_spikes == 0)[0])}")

            n_spikes_sce = np.sum(cells_in_sce, axis=1)
            n_spikes_in_sce = np.minimum(n_spikes_sce, n_spikes)
            n_spikes_out_sce = n_spikes - n_spikes_in_sce
            spike_in_sce_ratio = n_spikes_in_sce / n_spikes
            spike_out_sce_ratio = n_spikes_out_sce / n_spikes

            # Build a pd.DataFrame to summarize the 2 ratios (each row is a cell)
            age_list = [animal_age for k in range(n_cells)]
            weight_list = [animal_weight for k in range(n_cells)]
            if animal_weight is None:
                weight_list = ["N.A." for k in range(n_cells)]
            session_identifier_list = [session_identifier for k in range(n_cells)]
            animal_id_list = [animal_id for k in range(n_cells)]
            sum_up_data_0 = {'Age': age_list, 'SubjectID': animal_id_list, 'Weight': weight_list,
                             'Session': session_identifier_list, 'Celltype': cell_type_list,
                             'In_SCE_spike_ratio': spike_in_sce_ratio, 'Out_SCE_spike_ratio': spike_out_sce_ratio}
            spike_ratio_data_table = pd.DataFrame(sum_up_data_0)
            if verbose:
                print(f"Data table is built")

            # PART 2: Get the % of cell (for each type) participating in each SCE #
            if verbose:
                print(f"Computing SCE recruitment for each SCE")
            n_cells_by_sce = np.sum(cells_in_sce, axis=0)
            all_cell_participation_sce = (n_cells_by_sce / n_cells) * 100

            n_pyramide_by_sce = np.sum(pyramide_in_sce, axis=0)
            pyr_participation_sce = (n_pyramide_by_sce / n_pyr) * 100

            n_interneuron_by_sce = np.sum(interneuron_in_sce, axis=0)
            interneuron_participation_sce = (n_interneuron_by_sce / n_ins) * 100

            # Build a pd.DataFrame to summarize the SCE recruitment (each row is a SCE)
            age_list_sce = [animal_age for k in range(n_sce)]
            weight_list_sce = [animal_weight for k in range(n_sce)]
            if animal_weight is None:
                weight_list_sce = ["N.A." for k in range(n_sce)]
            session_identifier_list_sce = [session_identifier for k in range(n_sce)]
            animal_id_list_sce = [animal_id for k in range(n_sce)]
            sum_up_data_1 = {'Age': age_list_sce, 'SubjectID': animal_id_list_sce, 'Weight': weight_list_sce,
                             'Session': session_identifier_list_sce,
                             'AllCells_Recruitment': all_cell_participation_sce,
                             'PyramidalCells_Recruitment': pyr_participation_sce,
                             'Interneurons_Recruitment': interneuron_participation_sce}
            sce_recruitment_data_table = pd.DataFrame(sum_up_data_1)
            if verbose:
                print(f"Data table is built")

            # PART 3: Get the mean amplitude of all transients involved for each SCE #
            if verbose:
                print(f"Computing mean transient amplitude of involved cells for each SCE")
            cell_activations_list = []
            for cell in range(n_cells):
                cell_activations = get_continous_time_periods(raster_dur[cell, :])
                cell_activations_list.append(cell_activations)
            amplitudes_list = []
            for sce in range(n_sce):
                amplitudes_by_sce = []
                for cell in range(n_cells):
                    cell_activations = cell_activations_list[cell]
                    if cell_transient_in_sce[cell, sce] != -1:
                        transient_id = cell_transient_in_sce[cell, sce]
                        onset = cell_activations[transient_id][0]
                        peak = cell_activations[transient_id][1]
                        amplitude = np.max(traces[cell, peak - 1: peak + 1]) - traces[cell, onset]
                        amplitudes_by_sce.append(amplitude)
                amplitudes_list.append(amplitudes_by_sce)
            mean_amplitude_by_sce = [np.mean(x) for x in amplitudes_list]

            # Build a pd.DataFrame to summarize the SCE recruitment (each row is a SCE)
            age_list_sce = [animal_age for k in range(n_sce)]
            weight_list_sce = [animal_weight for k in range(n_sce)]
            if animal_weight is None:
                weight_list_sce = ["N.A." for k in range(n_sce)]
            session_identifier_list_sce = [session_identifier for k in range(n_sce)]
            animal_id_list_sce = [animal_id for k in range(n_sce)]
            sum_up_data_2 = {'Age': age_list_sce, 'SubjectID': animal_id_list_sce, 'Weight': weight_list_sce,
                             'Session': session_identifier_list_sce, 'MeanTransientAmplitude': mean_amplitude_by_sce}
            sce_transient_amplitude_data_table = pd.DataFrame(sum_up_data_2)
            if verbose:
                print(f"Data table is built")

            # Generate / append global pd.DataFrame tables #
            gobal_spike_ratio_data_table = gobal_spike_ratio_data_table.append(spike_ratio_data_table,
                                                                               ignore_index=True)
            gobal_sce_recruitment_data_table = gobal_sce_recruitment_data_table.append(sce_recruitment_data_table,
                                                                                       ignore_index=True)
            global_sce_transient_amplitude_data_table = global_sce_transient_amplitude_data_table.append(
                sce_transient_amplitude_data_table, ignore_index=True)

            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        if verbose:
            print(f"----------------------------------- SAVINGS --------------------------------------")
        path_results = self.get_results_path()
        path_ratio_table_xls = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table.xlsx')
        path_ratio_table_csv = os.path.join(f'{path_results}', f'inSCE_spikes_ratio_table.csv')
        path_recruitment_table_xls = os.path.join(f'{path_results}', f'SCE_recruitment_table.xlsx')
        path_recruitment_table_csv = os.path.join(f'{path_results}', f'SCE_recruitment_table.csv')
        path_amplitude_table_xls = os.path.join(f'{path_results}', f'SCE_transients_amplitude_table.xlsx')
        path_amplitude_table_csv = os.path.join(f'{path_results}', f'SCE_transients_amplitude_table.csv')
        if save_table:
            gobal_spike_ratio_data_table.to_excel(path_ratio_table_xls)
            gobal_spike_ratio_data_table.to_csv(path_ratio_table_csv)
            gobal_sce_recruitment_data_table.to_excel(path_recruitment_table_xls)
            gobal_sce_recruitment_data_table.to_csv(path_recruitment_table_csv)
            global_sce_transient_amplitude_data_table.to_excel(path_amplitude_table_xls)
            global_sce_transient_amplitude_data_table.to_csv(path_amplitude_table_csv)
            if verbose:
                print(f"Data save as excel and csv files")

        if verbose:
            print(f"-------------------------- WORK ON IN-SCE SPIKE RATIO -----------------------------")

        if verbose:
            print(f"Filter data table accordingly to the GUI requirements")
        # Filter general table on query from the GUI
        if cell_to_use == "Pyramidal_cells":
            data_table = gobal_spike_ratio_data_table.query('Celltype == "Pyramidal"')
            n_pyr = len(data_table.index)

        if cell_to_use == "Interneurons":
            data_table = gobal_spike_ratio_data_table.query('Celltype == "Interneuron"')
            n_ins = len(data_table.index)

        if cell_to_use == "All_cells":
            data_table = gobal_spike_ratio_data_table
            n_cells = len(data_table.index)

            pyr_data_table = gobal_spike_ratio_data_table.query('Celltype == "Pyramidal"')
            n_pyr = len(pyr_data_table.index)

            ins_data_table = gobal_spike_ratio_data_table.query('Celltype == "Interneuron"')
            n_ins = len(ins_data_table.index)

        # Get Info
        ages = data_table.get("Age")
        ages_list = ages.values.tolist()
        ages_list = np.unique(ages_list)
        n_ages = len(ages_list)

        animals = data_table.get("SubjectID")
        animals_list = animals.values.tolist()
        animals_list = np.unique(animals_list)
        n_animals = len(animals_list)

        sessions = data_table.get("Session")
        sessions_list = sessions.values.tolist()
        sessions_list = np.unique(sessions_list)
        n_sessions = len(sessions_list)

        if do_stats:
            if n_ages > 1:
                if verbose:
                    print(f"Do some statistics")
                    print(f"Compare the ratio: spikes in-SCE / total spikes for {cell_to_use} across age")
                    distribution_by_age = [[] for k in range(n_ages)]
                    if cell_to_use == "All_cells":
                        if verbose:
                            print(f"N pups: {n_animals}, N sessions: {n_sessions}, N cells: {n_cells}")
                        for index in range(n_ages):
                            age = ages_list[index]
                            tmp_table = data_table[data_table.Age == age]
                            data = tmp_table.get("In_SCE_spike_ratio")
                            data_list = data.values.tolist()
                            distribution_by_age[index] = data_list
                    if cell_to_use == "Pyramidal_cells":
                        if verbose:
                            print(f"N pups: {n_animals}, N sessions: {n_sessions}, N pyramidal cells: {n_pyr}")
                        for index in range(n_ages):
                            age = ages_list[index]
                            tmp_table = data_table[data_table.Age == age]
                            data = tmp_table.get("In_SCE_spike_ratio")
                            data_list = data.values.tolist()
                            distribution_by_age[index] = data_list
                    if cell_to_use == "Interneurons":
                        if verbose:
                            print(f"N pups: {n_animals}, N sessions: {n_sessions}, N interneurons: {n_ins}")
                        for index in range(n_ages):
                            age = ages_list[index]
                            tmp_table = data_table[data_table.Age == age]
                            data = tmp_table.get("In_SCE_spike_ratio")
                            data_list = data.values.tolist()
                            distribution_by_age[index] = data_list

                multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                      sessions_ids=ages_list)

        if verbose:
            print(f"Do the plots")

        # Do the plot according to GUI requirements
        if hue_ratio == "None":
            hue_ratio = None
            palette_ratio = None

        ylabel = "Ratio: spikes in-SCE / total spikes " + "Population: " + cell_to_use

        filename = "In_SCE_spike_ratio_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_ratio, y="In_SCE_spike_ratio", hue=hue_ratio, data=data_table, hue_order=None,
                          kind=kind_ratio, orient=None, color=fig_facecolor, palette=palette_ratio, ax=ax1)

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

        if verbose:
            print(f"--------------------------- WORK ON SCE RECRUITMENT ------------------------------")

        if do_stats:
            if n_ages > 1:
                if verbose:
                    print(f"Do some statistics")
                    print(f"Compare SCE recruitment among 'All Cells' across age")
                distribution_by_age = [[] for k in range(n_ages)]
                recruitement_data = gobal_sce_recruitment_data_table
                for index in range(n_ages):
                    age = ages_list[index]
                    tmp_table = recruitement_data[recruitement_data.Age == age]
                    data = tmp_table.get("AllCells_Recruitment")
                    data_list = data.values.tolist()
                    distribution_by_age[index] = data_list

                multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                      sessions_ids=ages_list)

        if verbose:
            print(f"Do the plots")

        # Do the plot according to GUI requirements
        if hue_recruitment == "None":
            hue_recruitment = None
            palette_recruitment = None

        ylabel = "Proportion of cell recruited in SCE (% of 'All cells')"

        filename = "SCE_recruitment"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_recruitment, y="AllCells_Recruitment", hue=hue_recruitment,
                          data=gobal_sce_recruitment_data_table, hue_order=None, kind=kind_recruitment,
                          orient=None, color=fig_facecolor, palette=palette_recruitment, ax=ax1)

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

        if verbose:
            print(f"---------------------- WORK ON SCE TRANSIENTS' AMPLITUDES -------------------------")

        if verbose:
            print(f"Do the plots")

        # Do the plot according to GUI requirements
        if hue_amplitude == "None":
            hue_amplitude = None
            palette_amplitude = None

        ylabel = "Mean transient amplitude in SCE (ZScore F)"

        filename = "SCE_transient_amplitude_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name_amplitude, y="MeanTransientAmplitude", hue=hue_amplitude,
                          data=global_sce_transient_amplitude_data_table,
                          hue_order=None, kind=kind_amplitude, orient=None, color=fig_facecolor,
                          palette=palette_amplitude,
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


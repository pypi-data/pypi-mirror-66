from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
import numpy as np
from cicada.utils.misc import from_timestamps_to_frame_epochs
from cicada.utils.display.psth import get_psth_values, plot_one_psth, plot_several_psth
import math
from bisect import bisect_right
from cicada.utils.display.colors import BREWER_COLORS
import matplotlib.cm as cm


class CicadaPsthAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        A list of
        :param data_to_analyse: list of data_structure
        :param family_id: family_id indicated to which family of analysis this class belongs. If None, then
        the analysis is a family in its own.
        :param data_format: indicate the type of data structure. for NWB, NIX
        """
        CicadaAnalysis.__init__(self, name="PSTH", family_id="Epochs",
                                short_description="Build PeriStimuli Time Histogram", config_handler=config_handler)

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

        for data_to_analyse in self._data_to_analyse:
            roi_response_series = data_to_analyse.get_roi_response_series()
            if len(roi_response_series) == 0:
                self.invalid_data_help = f"No roi response series available in " \
                    f"{data_to_analyse.identifier}"
                return False

        # It is also necessary to have epoch to work with, but if None is available, then it won't just be possible
        # to run the analysis

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_intervals_names())
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Epochs",
                                            long_description="Select epochs for which you want to build PSTH",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="do_fusion_epochs", true_by_default=False,
                                     short_description="Fusion epochs ?",
                                     long_description="If checked, within a group epochs that overlap "
                                                      "will be fused so they represent "
                                                      "then one epoch.",
                                     family_widget="epochs")

        self.add_choices_arg_for_gui(arg_name="session_color_choice", choices=["default_color", "brewer", "spectral"],
                                     short_description="Colors for session plots",
                                     default_value="brewer",
                                     multiple_choices=False, long_description=None,
                                     family_widget="session_color_config")

        self.add_color_arg_for_gui(arg_name="session_default_color", default_value=(1, 1, 1, 1.),
                                   short_description="Default color for session",
                                   long_description=None, family_widget="session_color_config")

        self.add_int_values_arg_for_gui(arg_name="psth_range", min_value=50, max_value=2000,
                                        short_description="Range of the PSTH (ms)",
                                        default_value=500, family_widget="psth_config")

        self.add_choices_arg_for_gui(arg_name="ref_in_epoch", choices=["start", "end", "middle"],
                                     short_description="Reference point to center PSTH",
                                     long_description="Determine which part of the epoch to center the PSTH on",
                                     default_value="start",
                                     multiple_choices=False, family_widget="psth_config")

        self.add_choices_arg_for_gui(arg_name="plot_style_option", choices= ["lines", "bars"],
                                     short_description="Options to display the PSTH",
                                     default_value="lines",
                                     multiple_choices=False, long_description=None, family_widget="plot_config")

        self.add_bool_option_for_gui(arg_name="average_fig", true_by_default=False,
                                     short_description="Add a figure that average all sessions",
                                     long_description=None,
                                     family_widget="plot_config")

        self.add_image_format_package_for_gui()

        self.add_verbose_arg_for_gui()

        self.add_with_timestamp_in_filename_arg_for_gui()

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

        roi_response_series_dict = kwargs["roi_response_series"]

        epochs_names = kwargs.get("epochs_names")
        if (epochs_names is None) or len(epochs_names) == 0:
            print(f"No epochs selected, no analysis")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100)
            return

        # ------- figures config part -------
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_raster = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        ref_in_epoch = kwargs.get("ref_in_epoch")

        psth_range_in_ms = kwargs.get("psth_range")

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        session_color_choice = kwargs.get("session_color_choice")

        session_default_color = kwargs.get("session_default_color")

        #TODO: Add option to plot a "significant threshold" line using surrogates

        # ------- figures config part -------

        # we can either run the PSTH on all data from all session
        # or do a PSTH for each session individually and produce as many plots
        # or add option to group sessions for example by age

        # first we create a dict that will identify group of session by an id
        # a group could be just a session
        # dict key is a string, value is a list of CicadaAnalysisWrapper instances
        session_group_ids_dict = dict()

        # take as key a session identifier and return the group_id it is part of
        session_to_group_id_mapping = dict()

        # then we have a dict with key epoch_name, value is a dict with key session_group_id and value a list of 2
        # elements: the time (in sec) of each value time of the PSTH, and PSTH data: list of length the number of fct
        # used each list being a list of float of length the number of timestamps
        psth_data_by_epoch_dict = dict()

        # then we have a dict with key session_group_id, value is a dict with key epoch_name and value a list of 2
        # elements: the time (in sec) of each value time of the PSTH, and PSTH data: list of length the number of fct
        # used each list being a list of float of length the number of timestamps
        psth_data_by_session_group_dict = dict()

        epochs_color_dict = dict()
        for epoch_group_name, epoch_info in epochs_names.items():
            if len(epoch_info) != 2:
                continue
            epochs_color_dict[epoch_group_name] = epoch_info[1]

        n_sessions = len(self._data_to_analyse)

        low_percentile = 25
        high_percentile = 75

        fcts_to_apply = [np.nanmedian, lambda x: np.nanpercentile(x, low_percentile),
                         lambda x: np.nanpercentile(x, high_percentile)]

        # TODO: Add group by age option in the widgets, see to add more complex grouping like range of ages
        group_by_age = False
        # first building the groups
        if group_by_age:
            pass
        else:
            # each session is its own group
            for session_index, session_data in enumerate(self._data_to_analyse):
                session_identifier = session_data.identifier
                session_to_group_id_mapping[session_identifier] = session_identifier
                session_group_ids_dict[session_identifier] = [session_data]

        highest_sampling_rate = 0
        lowest_sampling_rate = 100000
        for session_index, session_data in enumerate(self._data_to_analyse):
            session_identifier = session_data.identifier

            sampling_rate_hz = session_data.get_ci_movie_sampling_rate()
            if sampling_rate_hz > highest_sampling_rate:
                highest_sampling_rate = sampling_rate_hz
            if sampling_rate_hz < lowest_sampling_rate:
                lowest_sampling_rate = sampling_rate_hz
            # print(f"{session_identifier}: sampling_rate {sampling_rate_hz}")

            one_frame_duration = 1000 / sampling_rate_hz
            psth_range_in_frames = math.ceil(psth_range_in_ms / one_frame_duration)

            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)

            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)

            for epoch_group_name, epoch_info in epochs_names.items():
                if len(epoch_info) != 2:
                    continue
                epochs_names_in_group = epoch_info[0]
                # epoch_color = epoch_info[1]

                epochs_frames_in_group = []

                for epoch_name in epochs_names_in_group:
                    # looking in behavior or intervals
                    epochs_timestamps = session_data.get_interval_times(interval_name=epoch_name)
                    if epochs_timestamps is None:
                        epochs_timestamps = session_data.get_behavioral_epochs_times(epoch_name=epoch_name)
                    if epochs_timestamps is None:
                        # means this session doesn't have this epoch name
                        continue
                    # now we want to get the intervals time_stamps and convert them in frames
                    intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=epochs_timestamps,
                                                                       frames_timestamps=neuronal_data_timestamps,
                                                                       as_list=True)
                    epochs_frames_in_group.extend(intervals_frames)
                # TODO: See for fusionning epochs from a same group so there are extended
                psth_frames_indices, psth_values = get_psth_values(data=neuronal_data,
                                                                   epochs=epochs_frames_in_group,
                                                                   ref_in_epoch="start",
                                                                   range_value=psth_range_in_frames,
                                                                   fcts_to_apply=fcts_to_apply)

                session_group_id = session_to_group_id_mapping[session_identifier]
                # then we have a dict with key epoch_name, value is a dict with key
                # session_group_id and value the PSTH data
                if epoch_group_name not in psth_data_by_epoch_dict:
                    psth_data_by_epoch_dict[epoch_group_name] = dict()
                # putting indices in msec
                psth_frames_indices = np.array(psth_frames_indices)
                psth_times = psth_frames_indices * 1000/sampling_rate_hz
                if session_group_id not in psth_data_by_epoch_dict[epoch_group_name]:
                    psth_data_by_epoch_dict[epoch_group_name][session_group_id] = []
                psth_data_by_epoch_dict[epoch_group_name][session_group_id].append([psth_times, psth_values])

                # then we have a dict with key session_group_id, value is a dict with key epoch_name
                # and value the PSTH data
                if session_group_id not in psth_data_by_session_group_dict:
                    psth_data_by_session_group_dict[session_group_id] = dict()
                if epoch_group_name not in psth_data_by_session_group_dict[session_group_id]:
                    psth_data_by_session_group_dict[session_group_id][epoch_group_name] = []
                psth_data_by_session_group_dict[session_group_id][epoch_group_name].append([psth_times, psth_values])

            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / (n_sessions+1))

        # first we determine the bins to use
        # using the lowest sampling_rate to get the biggest bins
        step_in_ms = 1000 / lowest_sampling_rate
        bins_edges = np.arange(-psth_range_in_ms, psth_range_in_ms + step_in_ms, step_in_ms)
        bins_edges[-1] = psth_range_in_ms
        # print(f"bins_edges {bins_edges}")
        # print(f"len(bins_edges) {len(bins_edges)}, len(psth_times) {len(psth_times)}")
        x_label = "Duration (ms)"
        y_label = "Activity (%)",
        # now we plot the PSTH
        # we want to make a figure for each session group with all epoch types in it
        for session_group_id, epoch_dict in psth_data_by_session_group_dict.items():
            data_psth = []
            colors_plot = []
            label_legends = []
            for epoch_group_name, epoch_data_list in epoch_dict.items():
                time_x_values, psth_values_for_plot = \
                    prepare_psth_values(epoch_data_list, bins_edges, low_percentile, high_percentile)
                data_psth.append([time_x_values, psth_values_for_plot])
                colors_plot.append(epochs_color_dict[epoch_group_name])
                label_legends.append(epoch_group_name)
            plot_several_psth(results_path=self.get_results_path(),
                              data_psth=data_psth,
                              colors_plot=colors_plot,
                              file_name=f"psth_{session_group_id}",
                              label_legends=label_legends,
                              x_label=x_label, y_label=y_label,
                              color_ticks="white",
                              axes_label_color="white",
                              color_v_line="white", line_width=2,
                              line_mode=True, background_color="black",
                              figsize=(30, 20),
                              save_formats="pdf",
                              summary_plot=True)

        # we want to make a figure for each epoch types with all the session group
        for epoch_group_name, session_dict in psth_data_by_epoch_dict.items():
            data_psth = []
            colors_plot = []
            label_legends = []
            session_index = 0
            n_sessions = len(session_dict)
            for session_group_id, session_data_list in session_dict.items():
                time_x_values, psth_values_for_plot = \
                    prepare_psth_values(session_data_list, bins_edges, low_percentile, high_percentile)
                data_psth.append([time_x_values, psth_values_for_plot])
                # "default_color", "brewer", "spectral"
                if session_color_choice == "brewer":
                    colors_plot.append(BREWER_COLORS[session_index % len(BREWER_COLORS)])
                elif session_color_choice == "spectral":
                    colors_plot.append(cm.nipy_spectral(float(session_index + 1) / (n_sessions + 1)))
                else:
                    colors_plot.append(session_default_color)
                label_legends.append(session_group_id)
                session_index += 1
            plot_several_psth(results_path=self.get_results_path(),
                              data_psth=data_psth,
                              colors_plot=colors_plot,
                              file_name=f"psth_{epoch_group_name}",
                              label_legends=label_legends,
                              x_label=x_label, y_label=y_label,
                              color_ticks="white",
                              axes_label_color="white",
                              color_v_line="white", line_width=2,
                              line_mode=True, background_color="black",
                              figsize=(30, 20),
                              save_formats="pdf",
                              summary_plot=True)

        # we want a figure for each epoch session group and each epoch
        for epoch_group_name, session_dict in psth_data_by_epoch_dict.items():
            session_index = 0
            n_sessions = len(session_dict)
            for session_group_id, session_data_list in session_dict.items():
                time_x_values, psth_values_for_plot = \
                    prepare_psth_values(session_data_list, bins_edges, low_percentile, high_percentile)
                if session_color_choice == "brewer":
                    color_plot = BREWER_COLORS[session_index % len(BREWER_COLORS)]
                elif session_color_choice == "spectral":
                    color_plot = cm.nipy_spectral(float(session_index + 1) / (n_sessions + 1))
                else:
                    color_plot = session_default_color
                label_legends.append(session_group_id)
                session_index += 1
                plot_one_psth(results_path=self.get_results_path(),
                              time_x_values=time_x_values, psth_values=psth_values_for_plot,
                              color_plot=color_plot,
                              x_label=x_label, y_label=y_label,
                              color_ticks="white",
                              axes_label_color="white",
                              color_v_line="white", label_legend=None, line_width=2,
                              line_mode=True, background_color="black", ax_to_use=None,
                              figsize=(15, 10),
                              file_name=f"psth_{epoch_group_name}_{session_group_id}",
                              save_formats="pdf",
                              put_mean_line_on_plt=False)

        self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / (n_sessions + 1))
        print(f"Raster analysis run in {time() - self.analysis_start_time} sec")


def prepare_psth_values(session_data_list, bins_edges, low_percentile, high_percentile):
    if len(session_data_list) == 1:
        session_data = session_data_list[0]
        psth_times, psth_values = session_data
        median_psth_values = fill_bins(bin_edges=bins_edges, data=psth_values[0],
                                       data_time_points=psth_times)
        low_threshold_psth_values = fill_bins(bin_edges=bins_edges, data=psth_values[1],
                                              data_time_points=psth_times)
        high_threshold_psth_values = fill_bins(bin_edges=bins_edges, data=psth_values[2],
                                               data_time_points=psth_times)
    else:
        psth_matrix = np.zeros((0, len(bins_edges) - 1))
        for session_data in session_data_list:
            psth_times, psth_values = session_data
            psth_values_norm = fill_bins(bin_edges=bins_edges, data=psth_values[0],
                                         data_time_points=psth_times)
            psth_values_norm = np.reshape(psth_values_norm, (1, len(psth_values_norm)))
            psth_matrix = np.concatenate((psth_matrix, psth_values_norm))
        median_psth_values = np.nanmedian(psth_matrix, axis=0)
        low_threshold_psth_values = np.nanpercentile(psth_matrix, low_percentile)
        high_threshold_psth_values = np.nanpercentile(psth_matrix, high_percentile)
    psth_values_for_plot = [median_psth_values * 100, low_threshold_psth_values * 100,
                            high_threshold_psth_values * 100]
    time_x_values = [(t + bins_edges[i + 1]) / 2 for i, t in enumerate(bins_edges[:-1])]

    return time_x_values, psth_values_for_plot


def fill_bins(bin_edges, data, data_time_points):
    """
    Create an array based on bin_edges. If two values are on the same edge, then we put the mean
    Args:
        bin_edges: 1d array representing the edges of the bins
        data: 1d array representing the value to fill in the bins
        data_time_points: time indices of the data values in order to fit them in the good bin

    Returns: a 1d array of length len(bin_edges) -1

    """
    result = np.zeros(len(bin_edges)-1)

    for value_index, data_value in enumerate(data):
        time_point = data_time_points[value_index]
        # now we want to know in which bin to insert it
        index = bisect_right(bin_edges, time_point) - 1
        if index >= len(result):
            index = len(result) - 1
        # TODO: plan the case when more than 2 values could be on the same bin
        if result[index] > 0:
            # should not happen often
            result[index] = np.mean((result[index], data_value))
        else:
            result[index] = data_value

    return result

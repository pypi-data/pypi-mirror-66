from cicada.analysis.cicada_analysis import CicadaAnalysis
from cicada.utils.connectivity.connectivity_utils import get_time_correlation_data, plot_time_correlation_graph
from cicada.utils.misc import get_continous_time_periods
from cicada.utils.sce_stats_utils import detect_sce_on_traces, get_sce_threshold
import numpy as np
from time import time
import scipy.signal as sci_si


class CicadaTimeCorrelationGraphAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Christmas tree", family_id="Connectivity",
                                short_description="Time correlation graph", config_handler=config_handler)

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

        sce_detection_methods = ["Peaks", "All frames", "Traces"]
        self.add_choices_arg_for_gui(arg_name="method", choices=sce_detection_methods,
                                     default_value="peaks", short_description="Method used to detect SCEs",
                                     long_description="If 'Peaks': find SCEs using find-peaks with parameters below, "
                                                      "SCE will be define by a single frame. "
                                                      "If 'All frames': define SCEs as all continuous frame periods"
                                                      " with more active cells than the statistical threshold.",
                                     multiple_choices=False,
                                     family_widget="figure_config_method_to_use")

        self.add_int_values_arg_for_gui(arg_name="n_surrogates", min_value=10, max_value=10000,
                                        short_description="Number of surrogates raster to compute SCE threshold",
                                        default_value=100, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="percentile", min_value=95, max_value=100,
                                        short_description="Percentile of surrogate distribution to compute SCE threshold",
                                        default_value=99, family_widget="figure_config_surrogate")

        self.add_int_values_arg_for_gui(arg_name="min_sce_distance", min_value=1, max_value=10,
                                        short_description="Minimal number of frames between 2 SCEs",
                                        default_value=5, family_widget="figure_config_findpeaks")

        self.add_int_values_arg_for_gui(arg_name="time_delay", min_value=100, max_value=1500,
                                        short_description="Time delay in ms to look for correlated cells (ms)",
                                        default_value=500, family_widget="figure_config_delay")

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

        sce_detection_method = kwargs.get("method")

        min_sce_distance = kwargs.get("min_sce_distance")

        time_around_event = kwargs.get("time_delay")

        path_results = self.get_results_path()

        verbose = True

        start_time = time()
        print("Christmas tree: coming soon...")
        n_sessions = len(self._data_to_analyse)

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

            trace_neuronal_data = session_data.get_roi_response_serie_data_by_keyword(keys=roi_response_serie_info[:-1],
                                                                                      keyword="trace")
            for key, data in trace_neuronal_data.items():
                traces = trace_neuronal_data.get(key)

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

            # Build raster from rasterdur
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1

            # Get the SCE locations based on rasterdur: 2 options to define SCE #
            if sce_detection_method == "Peaks" or sce_detection_method == "All frames":
                if verbose:
                    print(f"Detection of SCEs location based on the rasterdur")
                sum_active_cells = np.sum(raster_dur, axis=0)
                sce_thresh = get_sce_threshold(raster_dur, n_surrogates=n_surrogates, percentile=percentile,
                                               verbose=verbose)[1]

            # With 'peaks' method: SCE are at a single frame which is the peak of synchrony
            if sce_detection_method == "Peaks":
                if verbose:
                    print(f"Detection of SCEs location using the '{sce_detection_method}' method")
                    print(f"Minimal distance between 2 SCEs: {min_sce_distance} frames")
                sce_times = sci_si.find_peaks(sum_active_cells, height=sce_thresh, distance=min_sce_distance)[0]
                n_sce = len(sce_times)
                if verbose:
                    print(f"SCE detection found: {n_sce} SCEs")
                # Put sce_times as a list of tuple, not single frame list
                sce_times = [(frame, frame) for frame in sce_times]

            # With 'all frames' method: SCE are at all frames with more co-active cells is higher than the threshold
            if sce_detection_method == "All frames":
                if verbose:
                    print(f"Detection of SCEs location using the '{sce_detection_method}' method")
                sce_periods = np.array(np.where(sum_active_cells >= sce_thresh)[0])
                sce_periods_bool = np.zeros(n_frames, dtype="bool")
                sce_periods_bool[sce_periods] = True
                sce_times = get_continous_time_periods(sce_periods_bool)
                n_sce = len(sce_times)
                if verbose:
                    print(f"SCE detection found: {n_sce} SCEs")

            # With 'traces' method: SCE are defined as in Malvache paper (2016)
            if sce_detection_method == "Traces":
                if verbose:
                    print(f"Detection of SCEs location based on the calcium traces")
                [cells_in_sce, sce_times] = detect_sce_on_traces(raw_traces=traces,
                                                                 speed=None, use_speed=True,
                                                                 speed_threshold=None,
                                                                 sce_n_cells_threshold=5,
                                                                 sce_min_distance=min_sce_distance,
                                                                 use_median_norm=True,
                                                                 use_bleaching_correction=False,
                                                                 use_savitzky_golay_filt=True)
                # Put sce_times as a list of tuple, not single frame list
                sce_times = [(frame, frame) for frame in sce_times]
                sce_thresh = 5
                if cells_in_sce.shape[1] == 0:
                    if verbose:
                        print(f"No detected SCEs")
                    return

            # Get data for time correlation graph
            time_around_event = time_around_event / 1000
            frames_around_event = int(np.round(samp_r * time_around_event))
            if verbose:
                print(f"Getting data for time correlation graph")
            time_lags_list, correlation_list, time_lags_dict, correlation_dict, time_window, cells_list = \
                get_time_correlation_data(spike_nums=raster, events_times=sce_times,
                                          time_around_events=frames_around_event)

            if verbose:
                print(f"Plotting time correlation graph")

            plot_time_correlation_graph(time_lags_list=time_lags_list, correlation_list=correlation_list,
                                        time_lags_dict=time_lags_dict, correlation_dict=correlation_dict,
                                        n_cells=n_cells, time_window=time_window,
                                        data_id=session_identifier, path_results=path_results, plot_cell_numbers=False,
                                        title_option="",
                                        cells_groups=None, groups_colors=None, set_y_limit_to_max=True,
                                        set_x_limit_to_max=True, xlabel=None, size_cells=100, size_cells_in_groups=240,
                                        time_stamps_by_ms=0.01, ms_scale=200, save_formats="pdf",
                                        show_percentiles=None, ax_to_use=None, color_to_use=None,
                                        value_to_text_in_cell=None)

            self.update_progressbar(start_time, 100 / n_sessions)

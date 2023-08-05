from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.display.rasters import plot_raster
import numpy as np
# from cicada.utils.display.colors import rgb_to_name
from cicada.utils.misc import from_timestamps_to_frame_epochs


class CicadaDisplayRasterAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Raster", family_id="Display",
                                short_description="Display raster",
                                config_handler=config_handler)

        # key is the cell type name, value is the name of the arg to get the color from the widget
        self.cell_type_color_arg_name = dict()

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

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        # choices_dict = dict()
        # for index, data in enumerate(self._data_to_analyse):
        #     if index < 2:
        #         choices_dict[data.identifier] = ["test_1", "test_2"]
        #     else:
        #         choices_dict[data.identifier] = ["test_3", "test_4", "test_6"]
        #
        # test_arg = {"arg_name": "test_multiple_choices", "choices": choices_dict,
        #             "short_description": "Test choices for each session",
        #             "multiple_choices": True}
        #
        # self.add_argument_for_gui(**test_arg)

        all_intervals = []
        for data_to_analyse in self._data_to_analyse:
            all_intervals.extend(data_to_analyse.get_intervals_names())
            all_intervals.extend(data_to_analyse.get_behavioral_epochs_names())
        all_intervals = list(np.unique(all_intervals))
        # print(f"all_intervals {all_intervals}")

        self.add_choices_for_groups_for_gui(arg_name="interval_names", choices=all_intervals,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Epochs",
                                            long_description="Select epochs you want to color in the raster",
                                            family_widget="epochs")

        self.add_int_values_arg_for_gui(arg_name="intervals_alpha_color", min_value=1, max_value=100,
                                        short_description="Transparency of color bands",
                                        default_value=50, family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="span_area_only_on_raster", true_by_default=False,
                                     short_description="Span only on raster",
                                     long_description="If checked, means the span will also be displayed in "
                                                      "the sum of activity plot if existing",
                                     family_widget="epochs")

        all_cell_types = []
        for data_to_analyse in self._data_to_analyse:
            all_cell_types.extend(data_to_analyse.get_all_cell_types())

        all_cell_types = list(set(all_cell_types))

        if len(all_cell_types) > 0:
            self.add_bool_option_for_gui(arg_name="sort_raster_by_cell_type", true_by_default=False,
                                         short_description="Sort raster cells by cell type",
                                         family_widget="cell_type")
            for cell_type in all_cell_types:
                self.cell_type_color_arg_name[cell_type] = f"color_for_{cell_type}"
                self.add_color_arg_for_gui(arg_name=f"color_for_{cell_type}", default_value=(1, 1, 1, 1.),
                                           short_description=f"Color for {cell_type}",
                                           family_widget="cell_type")

        spike_shapes = ["|", "o", ".", "*"]
        self.add_choices_arg_for_gui(arg_name="spike_shape", choices=spike_shapes,
                                     default_value="|", short_description="Spikes shape",
                                     multiple_choices=False,
                                     family_widget="spikes")

        self.add_int_values_arg_for_gui(arg_name="spike_size", min_value=5, max_value=500,
                                        short_description="Spike size",
                                        default_value=5, long_description=None, family_widget="spikes")

        self.add_color_arg_for_gui(arg_name="spikes_color", default_value=(1, 1, 1, 1.),
                                   short_description="spikes color",
                                   long_description=None, family_widget="spikes")

        self.add_int_values_arg_for_gui(arg_name="traces_lw", min_value=1, max_value=500,
                                        short_description="Traces line width",
                                        default_value=30, family_widget="traces")

        self.add_bool_option_for_gui(arg_name="use_brewer_colors_for_traces", true_by_default=True,
                                     short_description="Use brewer colors for traces",
                                     long_description="If False, will use spectral color map",
                                     family_widget="traces")

        self.add_bool_option_for_gui(arg_name="display_dashed_line_with_traces", true_by_default=False,
                                     short_description="Dashlines with traces",
                                     long_description="Display a dashline representing the mean value of each cell "
                                                      "fluoresence' signal",
                                     family_widget="traces")

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="activity_sum_plot_color", default_value=(1, 1, 1, 1.),
                                   short_description="Activity sum plot color",
                                   long_description=None, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="y_ticks_labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Y axis ticks labels color",
                                   long_description=None, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="x_ticks_labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="X axis ticks labels color",
                                   long_description=None, family_widget="raster_config")

        self.add_field_text_option_for_gui(arg_name="raster_y_axis_label", default_value="",
                                           short_description="Raster y axis label",
                                           long_description=None, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="raster_y_axis_label_size", min_value=1, max_value=100,
                                        short_description="Raster y axis label size",
                                        default_value=10, family_widget="raster_config")

        self.add_color_arg_for_gui(arg_name="axes_label_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes label color",
                                   long_description=None, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="x_axis_ticks_label_size", min_value=1, max_value=50,
                                        short_description="X axis ticks label size",
                                        default_value=8, family_widget="raster_config")

        self.add_int_values_arg_for_gui(arg_name="y_axis_ticks_label_size", min_value=1, max_value=50,
                                        short_description="Y axis ticks label size",
                                        default_value=8, family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="hide_x_ticks_labels", true_by_default=False,
                                     short_description="Hide x ticks labels",
                                     family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="hide_raster_y_ticks_labels", true_by_default=True,
                                     short_description="Hide raster y ticks labels",
                                     family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="with_ticks", true_by_default=False,
                                     short_description="Ticks on plots",
                                     family_widget="raster_config")

        self.add_bool_option_for_gui(arg_name="with_activity_sum", true_by_default=True,
                                     short_description="With activity sum plot",
                                     long_description=None, family_widget="raster_config")

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
          segmentation

        :return:
        """
        CicadaAnalysis.run_analysis(self, **kwargs)

        roi_response_series_dict = kwargs["roi_response_series"]

        verbose = kwargs.get("verbose", True)

        hide_x_ticks_labels = kwargs.get("hide_x_ticks_labels")

        hide_raster_y_ticks_labels = kwargs.get("hide_raster_y_ticks_labels")

        with_ticks = kwargs.get("with_ticks")

        spike_shape = kwargs.get("spike_shape", "|")

        spike_size = kwargs.get("spike_size", "5")
        spike_size = spike_size * 0.01

        use_brewer_colors_for_traces = kwargs.get("use_brewer_colors_for_traces", True)

        background_color = kwargs.get("background_color")

        spikes_color = kwargs.get("spikes_color")

        activity_sum_plot_color = kwargs.get("activity_sum_plot_color")

        axes_label_color = kwargs.get("axes_label_color")

        with_activity_sum = kwargs.get("with_activity_sum")

        display_dashed_line_with_traces = kwargs.get("display_dashed_line_with_traces")

        # cell types
        sort_raster_by_cell_type = kwargs.get("sort_raster_by_cell_type", False)
        color_by_cell_type = dict()
        if sort_raster_by_cell_type:
            for cell_type, arg_name in self.cell_type_color_arg_name.items():
                color_by_cell_type[cell_type] = kwargs.get(arg_name)

        # ------------- EPOCHS ---------------
        interval_names = kwargs.get("interval_names")

        intervals_alpha_color = kwargs.get("intervals_alpha_color")
        intervals_alpha_color = intervals_alpha_color * 0.01

        span_area_only_on_raster = kwargs.get("span_area_only_on_raster")
        # ------------- EPOCHS ---------------

        traces_lw = kwargs.get("traces_lw")
        traces_lw = traces_lw * 0.01

        raster_y_axis_label = kwargs.get("raster_y_axis_label")
        if raster_y_axis_label.strip() == "":
            raster_y_axis_label = None
        raster_y_axis_label_size = kwargs.get("raster_y_axis_label_size")

        y_axis_ticks_label_size = kwargs.get("y_axis_ticks_label_size")
        x_axis_ticks_label_size = kwargs.get("x_axis_ticks_label_size")

        y_ticks_labels_color = kwargs.get("y_ticks_labels_color")
        x_ticks_labels_color = kwargs.get("x_ticks_labels_color")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_raster = True

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamps_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        n_sessions = len(self._data_to_analyse)

        for session_index, session_data in enumerate(self._data_to_analyse):
            session_identifier = session_data.identifier
            if verbose:
                print(f"-------------- {session_identifier} -------------- ")
            if isinstance(roi_response_series_dict, dict):
                roi_response_serie_info = roi_response_series_dict[session_identifier]
            else:
                roi_response_serie_info = roi_response_series_dict

            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)

            neuronal_data_timestamps = session_data.get_roi_response_serie_timestamps(keys=roi_response_serie_info)
            # ci_ts = session_data.get_ci_movie_time_stamps()

            # ------------- EPOCHS ---------------
            span_area_coords = None
            span_area_colors = None
            if (interval_names is not None) and (len(interval_names) > 0):
                span_area_coords = []
                span_area_colors = []

                for interval_group_name, interval_info in interval_names.items():
                    if len(interval_info) != 2:
                        continue
                    interval_names_in_group = interval_info[0]
                    interval_color = interval_info[1]
                    # print(f"Interval {interval_group_name}, color: "
                    #       f"{rgb_to_name(interval_color, with_float_values=True)}")
                    rdb_values = [int(np.round(c*255)) for c in interval_color]
                    rdb_values = rdb_values[:-1]
                    print(f"Interval {interval_group_name}, color: {rdb_values}")

                    intervals_frames_in_group = []
                    # TODO: See for fusioning epochs from a same group so there are extended
                    for interval_name in interval_names_in_group:
                        # looking in behavior or intervals
                        intervals_timestamps = session_data.get_interval_times(interval_name=interval_name)
                        if intervals_timestamps is None:
                            intervals_timestamps = session_data.get_behavioral_epochs_times(epoch_name=interval_name)
                        if intervals_timestamps is None:
                            # means this session doesn't have this epoch name
                            continue
                        # now we want to get the intervals time_stamps and convert them in frames
                        intervals_frames = from_timestamps_to_frame_epochs(time_stamps_array=intervals_timestamps,
                                                                           frames_timestamps=neuronal_data_timestamps,
                                                                           as_list=True)
                        intervals_frames_in_group.extend(intervals_frames)
                    span_area_coords.append(intervals_frames_in_group)
                    span_area_colors.append(interval_color)
            # ------------- END EPOCHS ---------------
            # print(f"timestamps[:5] {timestamps[:5]}")
            cells_to_highlight = None
            cells_to_highlight_colors = None
            if sort_raster_by_cell_type:
                new_neuronal_data = np.zeros(neuronal_data.shape)
                cell_indices_by_cell_type = session_data.get_cell_indices_by_cell_type(roi_serie_keys=
                                                                                       roi_response_serie_info)
                cells_to_highlight = []
                cells_to_highlight_colors = []
                # ordering the data by cell type
                last_index = 0
                for cell_type, cell_indices in cell_indices_by_cell_type.items():
                    new_neuronal_data[last_index:last_index+len(cell_indices)] = neuronal_data[cell_indices]
                    color = color_by_cell_type[cell_type]
                    # coloring the cells
                    cells_to_highlight_colors.extend([color]*len(cell_indices))
                    cells_to_highlight.extend(list(np.arange(last_index, last_index+len(cell_indices))))
                    last_index = last_index+len(cell_indices)
                neuronal_data = new_neuronal_data

            if "trace" in roi_response_serie_info[-1]:
                display_traces = True
                display_spike_nums = False
                traces = neuronal_data
                if verbose:
                    print(f"traces shape {traces.shape}")
                spike_nums = None
                # we normalize the traces with z-score
                for trace_index, trace in enumerate(traces):
                    traces[trace_index] = (trace - np.mean(trace)) / np.std(trace)
                # traces = traces[:20]
            else:
                display_traces = False
                display_spike_nums = True
                spike_nums = neuronal_data
                traces = None
                if verbose:
                    print(f"spike_nums shape {spike_nums.shape}")

            plot_raster(spike_nums=spike_nums, traces=traces, display_traces=display_traces,
                        display_dashed_line_with_traces=display_dashed_line_with_traces,
                        traces_lw=traces_lw,
                        file_name="raster_" + session_data.identifier,
                        display_spike_nums=display_spike_nums,
                        with_timestamp_in_file_name=with_timestamps_in_file_name,
                        path_results=self.get_results_path(),
                        save_raster=save_raster,
                        show_raster=False,
                        use_brewer_colors_for_traces=use_brewer_colors_for_traces,
                        dpi=dpi,
                        show_sum_spikes_as_percentage=True,
                        spike_shape=spike_shape,
                        spike_shape_size=spike_size,
                        without_ticks=not with_ticks,
                        without_activity_sum=not with_activity_sum,
                        cell_spikes_color=spikes_color,
                        figure_background_color=background_color,
                        raster_face_color=background_color,
                        activity_sum_plot_color=activity_sum_plot_color,
                        activity_sum_face_color=background_color,
                        axes_label_color=axes_label_color,
                        hide_x_ticks_labels=hide_x_ticks_labels,
                        hide_raster_y_ticks_labels=hide_raster_y_ticks_labels,
                        raster_y_axis_label=raster_y_axis_label,
                        raster_y_axis_label_size=raster_y_axis_label_size,
                        y_ticks_labels_size=y_axis_ticks_label_size,
                        x_ticks_labels_size=x_axis_ticks_label_size,
                        y_ticks_labels_color=y_ticks_labels_color,
                        x_ticks_labels_color=x_ticks_labels_color,
                        cells_to_highlight=cells_to_highlight,
                        cells_to_highlight_colors=cells_to_highlight_colors,
                        span_area_coords=span_area_coords,
                        span_area_colors=span_area_colors,
                        span_area_only_on_raster=span_area_only_on_raster,
                        alpha_span_area=intervals_alpha_color,
                        size_fig=(width_fig, height_fig),
                        save_formats=save_formats)

            if verbose:
                print(" ")
            self.update_progressbar(time_started=self.analysis_start_time, increment_value=100 / n_sessions)

        print(f"Raster analysis run in {time() - self.analysis_start_time} sec")

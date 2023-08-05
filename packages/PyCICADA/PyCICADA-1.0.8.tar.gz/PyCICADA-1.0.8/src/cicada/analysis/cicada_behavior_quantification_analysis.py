from cicada.analysis.cicada_analysis import CicadaAnalysis
from datetime import datetime
from time import time
import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class CicadaBehaviorQuantificationAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Behavior Description", family_id="Behavior",
                                short_description="Basic behavior quantification", config_handler=config_handler)

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

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))
        if len(all_epochs) == 0:
            self.invalid_data_help = "No behavioral epochs associated to this recording"
            return False

        return True

    def set_arguments_for_gui(self):
        """

        Returns:

        """

        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neural activity to use", long_description=None)

        all_epochs = []
        for data_to_analyse in self._data_to_analyse:
            all_epochs.extend(data_to_analyse.get_behavioral_epochs_names())
        all_epochs = list(np.unique(all_epochs))

        self.add_choices_for_groups_for_gui(arg_name="epochs_names", choices=all_epochs,
                                            with_color=True,
                                            mandatory=False,
                                            short_description="Behavior groups",
                                            long_description="Group the different behaviors",
                                            family_widget="epochs")

        self.add_bool_option_for_gui(arg_name="save_table", true_by_default=True,
                                     short_description="Save results in table",
                                     family_widget="figure_config_saving")

        self.add_bool_option_for_gui(arg_name="save_figure", true_by_default=True,
                                     short_description="Save figure",
                                     family_widget="figure_config_saving")

        representations = ["strip", "swarm", "violin", "box", "bar", "boxen"]
        self.add_choices_arg_for_gui(arg_name="representation", choices=representations,
                                     default_value="box", short_description="Kind of plot to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        x_ax = ["Age", "SubjectID", "Session", "Behavior", "Group"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Behavior", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Behavior", "Group", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="None",
                                     short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted", short_description="Color palette for cell types",
                                     long_description="In that case figure facecolor and figure edsgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        self.add_image_format_package_for_gui()

        self.add_color_arg_for_gui(arg_name="background_color", default_value=(0, 0, 0, 1.),
                                   short_description="background color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="fig_facecolor", default_value=(1, 1, 1, 1.),
                                   short_description="Figure face color",
                                   long_description="Useless if a 'hue' is specified, in such a case use 'palette'",
                                   family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="axis_color", default_value=(1, 1, 1, 1.),
                                   short_description="Axes color",
                                   long_description=None, family_widget="figure_config_color")

        self.add_color_arg_for_gui(arg_name="labels_color", default_value=(1, 1, 1, 1.),
                                   short_description="Label color",
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

        self.add_int_values_arg_for_gui(arg_name="font_size", min_value=1, max_value=100,
                                        short_description="Font size",
                                        default_value=10, family_widget="figure_config_label")
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

        behaviors_names = kwargs.get("epochs_names")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        verbose = kwargs.get("verbose", True)

        time_unit = kwargs.get("time_unit")

        background_color = kwargs.get("background_color")

        fig_facecolor = kwargs.get("fig_facecolor")

        axis_color = kwargs.get("axis_color")

        labels_color = kwargs.get("labels_color")

        font_size = kwargs.get("font_size")

        fontweight = kwargs.get("fontweight")

        fontfamily = kwargs.get("font_type")

        # image package format
        save_formats = kwargs["save_formats"]
        if save_formats is None:
            save_formats = "pdf"

        save_table = kwargs.get("save_table")

        save_figure = kwargs.get("save_figure")

        dpi = kwargs.get("dpi", 100)

        width_fig = kwargs.get("width_fig")

        height_fig = kwargs.get("height_fig")

        with_timestamp_in_file_name = kwargs.get("with_timestamp_in_file_name", True)

        start_time = time()

        print("Behavioral quantification: coming soon...")

        n_sessions = len(self._data_to_analyse)
        n_sessions_to_use = n_sessions
        if verbose:
            print(f"{n_sessions} sessions to analyse")

        session_id_dict = dict()
        animal_age_dict = dict()
        animal_weight_dict = dict()
        all_durations_by_group_by_session_dict = dict()
        total_events_by_group_by_session_dict = dict()
        for session_index, session_data in enumerate(self._data_to_analyse):
            session_identifier = session_data.identifier
            animal_age = session_data.age
            animal_id = session_data.subject_id
            animal_weight = session_data.weight
            if verbose:
                print(f"---------------  ONGOING SESSION: {session_identifier} ---------------")

            all_epochs = []
            all_epochs.extend(session_data.get_behavioral_epochs_names())
            all_epochs = list(np.unique(all_epochs))
            n_behaviors = len(all_epochs)
            if len(all_epochs) == 0:
                n_sessions_to_use = n_sessions_to_use - 1
                if verbose:
                    print(f"No behavioral epochs in this session, skip it for analysis")
                if n_sessions_to_use == 0:
                    if verbose:
                        print(f"No session can be analyzed for behavior")
                    return
                if n_sessions_to_use > 1:
                    continue

            animal_age_dict[session_identifier] = animal_age
            session_id_dict[session_identifier] = animal_id
            animal_weight_dict[session_identifier] = animal_weight

            if verbose:
                print(f"------------- Start with all behaviors identified for this session -------------")

            # TODO: find a way to know how long is the recording to compute frequency of behaviors
            if verbose:
                print(f"List of observed behaviors: {all_epochs}")

            n_occurence_by_behavior = []
            durations_by_behavior = [[] for behavior in range(n_behaviors)]
            for behavior in range(n_behaviors):
                behavior_name = all_epochs[behavior]
                if verbose:
                    print(f"Behavior studied: {behavior_name}")
                behavior_timestamps = session_data.get_behavioral_epochs_times(epoch_name=behavior_name)
                n_occurence_behavior = behavior_timestamps.shape[1]
                durations_behavior = []
                for occurence in range(n_occurence_behavior):
                    duration = behavior_timestamps[1, occurence] - behavior_timestamps[0, occurence]
                    durations_behavior.append(duration)
                tmp_mean = np.mean(durations_behavior)
                tmp_sum = np.sum(durations_behavior)
                durations_by_behavior[behavior] = durations_behavior
                if verbose:
                    print(f"N={n_occurence_behavior}, mean duration: {tmp_mean}s, total duration"
                          f": {tmp_sum}s")
                n_occurence_by_behavior.append(n_occurence_behavior)
            mean_duration_by_behavior = [np.mean(x) for x in durations_by_behavior]
            sum_duration_by_behavior = [np.sum(x) for x in durations_by_behavior]
            if verbose:
                print(f"---------------------------------- Summary ----------------------------------")
                print(f"Number of occurrences by behavior : {n_occurence_by_behavior}")
                print(f"Mean duration by behavior : {mean_duration_by_behavior}")
                print(f"Total time by behavior: {sum_duration_by_behavior}")

            if verbose:
                print(f"---------------------- Work on defined behavior groups ----------------------")

            all_durations_by_group_dict = dict()
            total_events_for_group_dict = dict()
            index = 0
            for behavior_group_name, behavior_info in behaviors_names.items():
                if len(behavior_info) != 2:
                    continue
                index = index + 1
                behaviors_names_by_group = behavior_info[0]
                if verbose:
                    print(f"Group {index}, name: {behavior_group_name}, includes: {behaviors_names_by_group}")

                n_behaviors_in_group = len(behaviors_names_by_group)
                durations_for_group = [[] for behavior in range(n_behaviors_in_group)]
                durations_for_group_dict = dict()
                occurences_for_group = []
                occurences_for_group_dict = dict()
                for behavior, behavior_name in enumerate(behaviors_names_by_group):
                    if behavior_name not in all_epochs:
                        if verbose:
                            print(f"No {behavior_name} to include in group {index} for this animal")
                        continue
                    tmp_index = all_epochs.index(behavior_name)
                    durations_for_group[behavior] = durations_by_behavior[tmp_index]
                    durations_for_group_dict[behavior_name] = durations_by_behavior[tmp_index]
                    occurences_for_group.append(n_occurence_by_behavior[tmp_index])
                    occurences_for_group_dict[behavior_name] = n_occurence_by_behavior[tmp_index]
                all_durations_for_group = np.concatenate(durations_for_group)
                mean_duration_for_group = np.mean(all_durations_for_group)
                total_events_for_group = np.sum(occurences_for_group)
                all_durations_by_group_dict[behavior_group_name] = durations_for_group_dict
                total_events_for_group_dict[behavior_group_name] = occurences_for_group_dict
                if verbose:
                    print(f"Total events in {behavior_group_name} group: {total_events_for_group}, "
                          f"mean duration: {mean_duration_for_group}s ")

            all_durations_by_group_by_session_dict[session_identifier] = all_durations_by_group_dict
            total_events_by_group_by_session_dict[session_identifier] = total_events_for_group_dict
            self.update_progressbar(start_time, 100 / n_sessions)

        column_names_durations = ["Duration", "Behavior", "Group", "Session", "Age", "Weight"]
        column_names_occurrences = ["Occurrence", "Behavior", "Group", "Session", "Age", "Weight"]
        durations_table = pd.DataFrame(columns=column_names_durations)
        occurrences_table = pd.DataFrame(columns=column_names_occurrences)
        for session_key, data in all_durations_by_group_by_session_dict.items():
            session_data = all_durations_by_group_by_session_dict.get(session_key)
            animal_age = animal_age_dict.get(session_key)
            animal_id = session_id_dict.get(session_key)
            animal_weight = animal_weight_dict.get(session_key, "N.A.")
            for group_key, data_second in session_data.items():
                session_data_group = session_data.get(group_key)
                for behavior_key, data_third in session_data_group.items():
                    session_data_goup_behavior = session_data_group.get(behavior_key)
                    n_events = len(session_data_goup_behavior)
                    occurrences_table = occurrences_table.append({'Occurrence': n_events, 'Behavior': behavior_key,
                                                                  'Group': group_key, 'Session': session_key,
                                                                  'SubjectID': animal_id, 'Age': animal_age,
                                                                  'Weight': animal_weight},
                                                                 ignore_index=True)
                    for event in range(n_events):
                        duration = session_data_goup_behavior[event]
                        durations_table = durations_table.append({'Duration': duration, 'Behavior': behavior_key,
                                                                 'Group': group_key, 'Session': session_key,
                                                                  'SubjectID': animal_id, 'Age': animal_age,
                                                                  'Weight': animal_weight},
                                                                 ignore_index=True)

        path_results = self.get_results_path()
        path_to_occurrence_table = os.path.join(f'{path_results}', f'occurrence_table.xlsx')
        path_to_duration_table = os.path.join(f'{path_results}', f'duration_table.xlsx')
        if save_table:
            if verbose:
                print(f"--------------------------- GENERAL SUMMARY TABLES ---------------------------")
            occurrences_table.to_excel(path_to_occurrence_table)
            if verbose:
                print(f"Occurences table is built and save")
            durations_table.to_excel(path_to_duration_table)
            if verbose:
                print(f"Durations table is built and save")

            if verbose:
                print(f"------------------------------ DO SOME PLOTTING ------------------------------")

        # Do the plot according to GUI requirements
        if hue == "None":
            hue = None
            palette = None

        # Figure1: occurrence
        filename = "occurrences_figure_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="Occurrence", hue=hue, data=occurrences_table, hue_order=None,
                          kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

        ax1.yaxis.label.set_color(labels_color)
        ax1.xaxis.label.set_color(labels_color)
        ax1.spines['left'].set_color(axis_color)
        ax1.spines['right'].set_color(background_color)
        ax1.spines['bottom'].set_color(background_color)
        ax1.spines['top'].set_color(background_color)
        ax1.yaxis.set_tick_params(labelsize=font_size)
        ax1.xaxis.set_tick_params(labelsize=font_size)
        ax1.tick_params(axis='y', colors=axis_color)
        ax1.tick_params(axis='x', colors=axis_color, rotation=45)

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

        # Figure2: duration
        filename = "durations_figure_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="Duration", hue=hue, data=durations_table, hue_order=None,
                          kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

        ax1.yaxis.label.set_color(labels_color)
        ax1.xaxis.label.set_color(labels_color)
        ax1.spines['left'].set_color(axis_color)
        ax1.spines['right'].set_color(background_color)
        ax1.spines['bottom'].set_color(background_color)
        ax1.spines['top'].set_color(background_color)
        ax1.yaxis.set_tick_params(labelsize=font_size)
        ax1.xaxis.set_tick_params(labelsize=font_size)
        ax1.tick_params(axis='y', colors=axis_color)
        ax1.tick_params(axis='x', colors=axis_color, rotation=45)

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

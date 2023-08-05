from cicada.analysis.cicada_analysis import CicadaAnalysis
from time import time
from cicada.utils.misc import get_continous_time_periods
import numpy as np
from datetime import datetime
from cicada.utils.stats import compare_two_distributions
from cicada.utils.stats import multiple_comparison_one_factor_effect
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns


class CicadaTransientFrequencyAnalysis(CicadaAnalysis):
    def __init__(self, config_handler=None):
        """
        """
        CicadaAnalysis.__init__(self, name="Transients' frequency", family_id="Descriptive statistics",
                                short_description="", config_handler=config_handler)

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
        Returns:

        """
        CicadaAnalysis.set_arguments_for_gui(self)

        self.add_roi_response_series_arg_for_gui(short_description="Neuronal activity to use", long_description=None)

        cell_types = ["All_cells", "Pyramidal_cells", "Interneurons"]
        self.add_choices_arg_for_gui(arg_name="cell_to_use", choices=cell_types,
                                     default_value="All_cells", short_description="Cell type to use",
                                     multiple_choices=False,
                                     family_widget="figure_config_data_to_use")

        time_unity = ["seconds", "minutes"]
        self.add_choices_arg_for_gui(arg_name="time_unit", choices=time_unity,
                                     default_value="minutes", short_description="Time unity for frequency",
                                     multiple_choices=False,
                                     family_widget="figure_config_data_to_use")

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

        x_ax = ["Age", "SubjectID", "Session", "Celltype"]
        self.add_choices_arg_for_gui(arg_name="x_axis", choices=x_ax,
                                     default_value="Age", short_description="Variable to use for x axis groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        possible_hues = ["Age", "SubjectID", "Session", "Celltype", "None"]
        self.add_choices_arg_for_gui(arg_name="hue", choices=possible_hues,
                                     default_value="Celltype", short_description="Variable to use for x axis sub-groups",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        palettes = ["muted", "deep", "pastel", "Blues"]
        self.add_choices_arg_for_gui(arg_name="palettes", choices=palettes,
                                     default_value="muted", short_description="Color palette for cell types",
                                     long_description="In that case figure facecolor and figure edsgecolor are useless",
                                     multiple_choices=False,
                                     family_widget="figure_config_representation")

        self.add_bool_option_for_gui(arg_name="do_stats", true_by_default=True,
                                     short_description="Try statistical tests",
                                     family_widget="figure_config_stats")

        self.add_int_values_arg_for_gui(arg_name="pvalue", min_value=1, max_value=5,
                                        short_description="p-value (%) for statistical test",
                                        default_value=5, family_widget="figure_config_stats")

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
        print("Transients' frequency: coming soon...")

        roi_response_series_dict = kwargs["roi_response_series"]

        cell_to_use = kwargs.get("cell_to_use")

        x_axis_name = kwargs.get("x_axis")

        hue = kwargs.get("hue")

        kind = kwargs.get("representation")

        palette = kwargs.get("palettes")

        do_stats = kwargs.get("do_stats")

        pvalue = kwargs.get("pvalue")
        pvalue = pvalue / 100

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

        n_sessions = len(self._data_to_analyse)
        if verbose:
            print(f"{n_sessions} sessions to analyse")

        gobal_frequence_data_table = pd.DataFrame()
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
            duration_s = neuronal_data_timestamps[len(neuronal_data_timestamps)-1] - neuronal_data_timestamps[0]
            duration_m = duration_s / 60
            if verbose:
                print(f"Acquisition last for : {duration_s} seconds // {duration_m} minutes ")

            # Get Neuronal Data
            neuronal_data = session_data.get_roi_response_serie_data(keys=roi_response_serie_info)
            raster_dur = neuronal_data
            [n_cells, n_frames] = raster_dur.shape
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

            # Building raster plot from rasterdur
            raster = np.zeros((n_cells, n_frames))
            for cell in range(n_cells):
                tmp_tple = get_continous_time_periods(raster_dur[cell, :])
                for tple in range(len(tmp_tple)):
                    onset = tmp_tple[tple][0]
                    raster[cell, onset] = 1

            # Building spike frequency vector
            n_onsets = np.sum(raster, axis=1)
            transient_frequeny_second = n_onsets / duration_s
            transient_frequeny_minute = n_onsets / duration_m
            if time_unit == "seconds":
                distribution_all_cells = transient_frequeny_second
            else:
                distribution_all_cells = transient_frequeny_minute

            # Generate pd.DataFrame table #
            age_list = [animal_age for k in range(n_cells)]
            weight_list = [animal_weight for k in range(n_cells)]
            if animal_weight is None:
                weight_list = ["N.A." for k in range(n_cells)]
            session_identifier_list = [session_identifier for k in range(n_cells)]
            animal_id_list = [animal_id for k in range(n_cells)]
            sum_up_data = {'Frequence': distribution_all_cells, 'Celltype': cell_type_list,
                           'Session': session_identifier_list, 'SubjectID': animal_id_list, 'Age': age_list,
                           'Weight': weight_list}
            frequence_data_table = pd.DataFrame(sum_up_data)

            # If possible compare Pyramidal cells and Interneurons for this session:
            if n_ins >= 1 and n_pyr >= 1:
                pyramidal_table = frequence_data_table.query('Celltype == "Pyramidal"')
                pyramidal_frequencies = pyramidal_table.get("Frequence")
                pyramidal_frequencies_list = pyramidal_frequencies.values.tolist()
                ins_table = frequence_data_table.query('Celltype == "Interneuron"')
                ins_table_frequencies = ins_table.get("Frequence")
                ins_table_frequencies_list = ins_table_frequencies.values.tolist()
                if do_stats:
                    if verbose:
                        print(f"--------------------- Basic stats: {session_identifier} ---------------------")
                        print(f"Compare transient frequency for interneurons VS pyramidal cells")
                    compare_two_distributions(pyramidal_frequencies_list, ins_table_frequencies_list, pvalues=pvalue,
                                              verbose=verbose)

            # Generate / append global pd.DataFrame table #
            gobal_frequence_data_table = gobal_frequence_data_table.append(frequence_data_table, ignore_index=True)
            self.update_progressbar(start_time, 100 / n_sessions)

        # Save results in table
        if verbose:
            print(f"----------------------------------- SAVINGS --------------------------------------")
        path_results = self.get_results_path()
        path_table_xls = os.path.join(f'{path_results}', f'transient_frequencies_table.xlsx')
        path_table_csv = os.path.join(f'{path_results}', f'transient_frequencies_table.csv')
        if save_table:
            gobal_frequence_data_table.to_excel(path_table_xls)
            gobal_frequence_data_table.to_csv(path_table_csv)
            if verbose:
                print(f"Data save as excel and csv files")

        # Filter general table on query from the GUI
        if cell_to_use == "Pyramidal_cells":
            data_table = gobal_frequence_data_table.query('Celltype == "Pyramidal"')
            n_pyr = len(data_table.index)

        if cell_to_use == "Interneurons":
            data_table = gobal_frequence_data_table.query('Celltype == "Interneuron"')
            n_ins = len(data_table.index)

        if cell_to_use == "All_cells":
            data_table = gobal_frequence_data_table
            n_cells = len(data_table.index)

            pyr_data_table = gobal_frequence_data_table.query('Celltype == "Pyramidal"')
            n_pyr = len(pyr_data_table.index)

            ins_data_table = gobal_frequence_data_table.query('Celltype == "Interneuron"')
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

        # Do Some Statistics
        if do_stats:
            if verbose:
                print(f"----------------------------------- DO STATS --------------------------------------")
            if cell_to_use == "All_cells":
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N cells: {n_cells}, "
                          f"N pyramidal cells: {n_pyr}, N Interneurons: {n_ins}")

                pyramidal_data = pyr_data_table.get("Frequence")
                pyramidal_list = pyramidal_data.values.tolist()
                ins_data = ins_data_table.get("Frequence")
                ins_list = ins_data.values.tolist()

                distribution_by_age = [[] for k in range(n_ages)]
                for index in range(n_ages):
                    age = ages_list[index]
                    tmp_table = data_table[data_table.Age == age]
                    data = tmp_table.get("Frequence")
                    data_list = data.values.tolist()
                    distribution_by_age[index] = data_list

                if verbose:
                    print(f"------------- Compare Interneurons VS Pyramidal cells: all data set --------------")
                compare_two_distributions(pyramidal_list, ins_list, pvalues=pvalue, verbose=verbose)
                if n_ages > 1:
                    if verbose:
                        print(f"------------------- Compare {cell_to_use} frequency across ages --------------------")
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

            if cell_to_use == "Pyramidal_cells":
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N pyramidal cells: {n_pyr}")

                distribution_by_age = [[] for k in range(n_ages)]
                for index in range(n_ages):
                    age = ages_list[index]
                    tmp_table = data_table[data_table.Age == age]
                    data = tmp_table.get("Frequence")
                    data_list = data.values.tolist()
                    distribution_by_age[index] = data_list
                if n_ages > 1:
                    if verbose:
                        print(f"------------------- Compare {cell_to_use} frequency across ages --------------------")
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

            if cell_to_use == "Interneurons":
                if verbose:
                    print(f"N pups: {n_animals}, N sessions: {n_sessions}, N interneurons: {n_ins}")

                distribution_by_age = [[] for k in range(n_ages)]
                for index in range(n_ages):
                    age = ages_list[index]
                    tmp_table = data_table[data_table.Age == age]
                    data = tmp_table.get("Frequence")
                    data_list = data.values.tolist()
                    distribution_by_age[index] = data_list
                if n_ages > 1:
                    if verbose:
                        print(f"------------------- Compare {cell_to_use} frequency across ages --------------------")
                    multiple_comparison_one_factor_effect(distribution_by_age, pvalues=pvalue, verbose=verbose,
                                                          sessions_ids=ages_list)

        # Do Some Plots
        if verbose:
            print(f"----------------------------------- DO PLOTS --------------------------------------")

        # Do the plot according to GUI requirements
        if hue == "None":
            hue = None
            palette = None

        ylabel = "Frequency  (Transients / " + time_unit + ")"

        filename = "transient_frequency_"

        fig, ax1 = plt.subplots(nrows=1, ncols=1,
                                gridspec_kw={'height_ratios': [1]},
                                figsize=(width_fig, height_fig), dpi=dpi)
        ax1.set_facecolor(background_color)
        fig.patch.set_facecolor(background_color)

        svm = sns.catplot(x=x_axis_name, y="Frequence", hue=hue, data=data_table, hue_order=None,
                          kind=kind, orient=None, color=fig_facecolor, palette=palette, ax=ax1)

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

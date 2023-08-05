from cicada.analysis.cicada_analysis_format_wrapper import CicadaAnalysisFormatWrapper
from pynwb.ophys import ImageSegmentation, TwoPhotonSeries, Fluorescence
from pynwb.image import ImageSeries
import os
from pynwb import NWBHDF5IO
import numpy as np


class CicadaAnalysisNwbWrapper(CicadaAnalysisFormatWrapper):
    """
    Allows to communicate with the nwb format
    """

    def __init__(self, data_ref, load_data=True):
        CicadaAnalysisFormatWrapper.__init__(self, data_ref=data_ref, data_format="nwb", load_data=load_data)
        self._nwb_data = None
        if self.load_data_at_init:
            self.load_data()

    def load_data(self):
        io = NWBHDF5IO(self._data_ref, 'r')
        self._nwb_data = io.read()
        # if we close it, then later on we have an exception such as: ValueError: Not a dataset (not a dataset)
        # io.close()

    @property
    def identifier(self):
        return self._nwb_data.identifier

    @property
    def age(self):
        return self._nwb_data.subject.age

    @property
    def genotype(self):
        return self._nwb_data.subject.genotype

    @property
    def species(self):
        return self._nwb_data.subject.species

    @property
    def subject_id(self):
        """
         Id of the subject
         :return: None if subject_id unknown
        """
        return self._nwb_data.subject.subject_id

    @property
    def weight(self):
        """
         Id of the subject
         :return: None if weight unknown
        """
        return self._nwb_data.subject.weight

    @property
    def sex(self):
        """
         Sex (gender) of the subject
         :return: None if sex unknown
        """
        return self._nwb_data.subject.sex

    def get_segmentations(self):
        """

        Returns: a dict that for each step till plane_segmentation represents the different option.
        First dict will have as keys the name of the modules, then for each modules the value will be a new dict
        with keys the ImageSegmentation names and then the value will be a list representing the segmentation plane

        """
        segmentation_dict = dict()
        for name_mod, mod in self._nwb_data.modules.items():
            segmentation_dict[name_mod] = dict()
            no_keys_added = True
            for key, value in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of ImageSegmentation
                if isinstance(value, ImageSegmentation):
                    no_keys_added = False
                    image_seg = value
                    # key is the name of segmentation, and value a list of plane_segmentation
                    segmentation_dict[name_mod][key] = []
                    # print(f"get_segmentations {name_mod} key {key}")
                    for plane_seg_name in image_seg.plane_segmentations.keys():
                        # print(f"get_segmentations plane_seg_name {plane_seg_name}")
                        segmentation_dict[name_mod][key].append(plane_seg_name)
            if no_keys_added:
                del segmentation_dict[name_mod]

        # it could be empty, but if it would matter, it should have been check by method check_data in CicadaAnalysis
        return segmentation_dict

    def get_roi_response_serie_data(self, keys):
        """

        Args:
            keys: lsit of string allowing to get the roi repsonse series wanted

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in self._nwb_data.modules:
            return None

        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        return np.array(self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series[keys[2]].data)

    def get_roi_response_serie_data_by_keyword(self, keys, keyword):
        """
        Return a dict with other last key data
        Args:
            keys: list of string allowing to get the  roi response series in data_interfaces
            keyword:
        Returns:
        """
        if len(keys) < 2:
            return dict()
        if keys[0] not in self._nwb_data.modules:
            return dict()
        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return dict()
        result_dict = dict()
        for key_data, rrs in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series.items():
            if keyword in key_data:
                result_dict[key_data] = np.array(rrs.data)
        return result_dict

    def get_all_cell_types(self):
        """
        Return a list of all cell types identified in this session. If the list is empty, it means the type of the cells
        is not identified
        Returns:

        """
        cell_types = []
        for name_mod, mod in self._nwb_data.modules.items():
            for key, fluorescence in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of pynwb.ophys.Fluorescence
                if isinstance(fluorescence, Fluorescence):
                    for name_rrs, rrs in fluorescence.roi_response_series.items():
                        cell_type_names = rrs.control_description
                        if cell_type_names is not None:
                            cell_types.extend(list(cell_type_names))
        # keeping only unique values
        return list(set(cell_types))

    def get_cell_indices_by_cell_type(self, roi_serie_keys):
        """
        Return a dict with key the cell_type name and value an array of int representing the cell indices of this type
        Args:
            roi_serie_keys:

        Returns:

        """
        rrs = self._get_roi_response_serie(keys=roi_serie_keys)
        if rrs is None:
            return {}

        # rrs.control is an array (uint8) as long as n_cells, with a code for each cell type
        # rrs.control_description is the list of cell type names, as long as n_cells
        if rrs.control_description is not None:
            cell_type_names = list(set(rrs.control_description))
        else:
            cell_type_names = []
        code_by_cell_type = dict()
        for cell_type_name in cell_type_names:
            index = list(rrs.control_description).index(cell_type_name)
            code_by_cell_type[cell_type_name] = rrs.control[index]

        cell_type_names.sort()

        cell_indices_by_cell_type = dict()
        for cell_type_name in cell_type_names:
            code = code_by_cell_type[cell_type_name]
            cell_indices_by_cell_type[cell_type_name] = np.where(np.array(rrs.control) == code)[0]

        return cell_indices_by_cell_type

    def _get_roi_response_serie(self, keys):
        """

        Args:
            keys: list of string allowing to get the roi repsonse series wanted

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in self._nwb_data.modules:
            return None

        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        return self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series[keys[2]]

    def get_roi_response_serie_timestamps(self, keys):
        """

        Args:
            keys: lsit of string allowing to get the roi repsonse series wanted

        Returns:

        """
        if len(keys) < 3:
            return None

        if keys[0] not in  self._nwb_data.modules:
            return None

        if keys[1] not in self._nwb_data.modules[keys[0]].data_interfaces:
            return None

        if keys[2] not in self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series:
            return None

        return self._nwb_data.modules[keys[0]].data_interfaces[keys[1]].roi_response_series[keys[2]].timestamps

    def get_roi_response_series(self, keywords_to_exclude=None):
        """
                param:
                keywords_to_exclude: if not None, list of str, if one of neuronal data has this keyword,
                then we don't add it to the choices

                Returns: a list or dict of objects representing all roi response series (rrs) names
                rrs could represents raw traces, or binary raster, and its link to a given segmentation.
                The results returned should allow to identify the segmentation associated.
                Object could be strings, or a list of strings, that identify a rrs and give information
                how to get there.

        """
        rrs_dict = dict()
        for name_mod, mod in self._nwb_data.modules.items():
            rrs_dict[name_mod] = dict()
            for key, fluorescence in mod.data_interfaces.items():
                # we want to check that the object in Module is an Instance of pynwb.ophys.Fluorescence
                if isinstance(fluorescence, Fluorescence):
                    rrs_dict[name_mod][key] = []
                    for name_rrs, rrs in fluorescence.roi_response_series.items():
                        if keywords_to_exclude is not None:
                            to_exclude = False
                            for keyword in keywords_to_exclude:
                                if keyword in name_rrs:
                                    to_exclude = True
                                    break
                            if to_exclude:
                                continue
                        rrs_dict[name_mod][key].append(name_rrs)
                    if len(rrs_dict[name_mod][key]) == 0:
                        del rrs_dict[name_mod][key]
            if len(rrs_dict[name_mod]) == 0:
                del rrs_dict[name_mod]

        # then we remove modules without Fluorescence instances
        # keys_to_remove = []
        # for key, value_dict in rrs_dict.items():
        #     if len(value_dict) == 0:
        #         keys_to_remove.append(key)
        # for key in keys_to_remove:
        #     del rrs_dict[key]
        return rrs_dict

    def get_pixel_mask(self, segmentation_info):
        """
        Return pixel_mask which is a list of list of pair of integers representing the pixels coordinate (x, y) for each
        cell. the list length is the same as the number of cells.
        Args:
            segmentation_info: a list of 3 elements: first one being the name of the module, then the name
            of image_segmentation and then the name of the segmentation plane.

        Returns:

        """
        if len(segmentation_info) < 3:
            return None

        name_module = segmentation_info[0]
        mod = self._nwb_data.modules[name_module]

        name_mode = segmentation_info[1]
        name_plane_seg = segmentation_info[2]
        plane_seg = mod[name_mode].get_plane_segmentation(name_plane_seg)

        if 'pixel_mask' not in plane_seg:
            return None

        return plane_seg['pixel_mask']

    def contains_ci_movie(self, consider_only_2_photons):
        """
        Indicate if the data object contains at least one calcium imaging movie represented by an instance of
        pynwb.image.ImageSeries
        Args:
            consider_only_2_photons: boolean, it True means we consider only 2 photons calcium imaging movies,
            if other exists but not 2 photons, then False will be return
        Returns: True if it's the case, False otherwise

        """
        # a TwoPhotonSeries is an instance of ImageSeries
        has_one = False
        for key, acquisition_data in self._nwb_data.acquisition.items():
            if consider_only_2_photons:
                if isinstance(acquisition_data, TwoPhotonSeries):
                    has_one = True
            else:
                if isinstance(acquisition_data, ImageSeries):
                    has_one = True
        if not has_one:
            return False

        return True

    def get_behavior_movies(self, key_to_identify="behavior"):
        """
                Return a dict with as key a string identifying the movie, and as value a dict of behavior movies
                a string as file_name if external, or a 3d array
                Args:
                    key_to_identify: string, key to identify that a movie is a behavior movie

                Returns:

        """
        behavior_movies_dict = dict()
        # print(f"self._nwb_data.acquisition.keys() {list(self._nwb_data.acquisition.keys())}")
        for key, acquisition_data in self._nwb_data.acquisition.items():
            if key_to_identify not in key:
                continue
            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                if image_series.format == "external":
                    movie_file_name = image_series.external_file[0]
                    movie_data = movie_file_name
                    behavior_movies_dict[key] = movie_data

        return behavior_movies_dict

    def get_ci_movies(self, only_2_photons):
        """
        Return a dict with as key a string identifying the movie, and as value a dict of CI movies
        a string as file_name if external, or a 3d array
        Args:
            only_2_photons: return only the 2 photon movies

        Returns:

        """
        ci_movies_dict = dict()

        for key, acquisition_data in self._nwb_data.acquisition.items():
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                if image_series.format == "external":
                    movie_file_name = image_series.external_file[0]
                    movie_data = movie_file_name
                else:
                    movie_data = image_series.data
                ci_movies_dict[key] = movie_data

        return ci_movies_dict

    def get_ci_movie_sampling_rate(self, only_2_photons=False, ci_movie_name=None):
        """

        Args:
            only_2_photons: if True only 2 photons one are considere
            ci_movie_name: (string) if not None, return the sampling rate for a given ci_movie, otherwise the first
            one found

        Returns: (float) sampling rate of the movie, return None if no movie is found

        """

        for key, acquisition_data in self._nwb_data.acquisition.items():
            if ci_movie_name is not None and (key != ci_movie_name):
                continue
            if only_2_photons:
                if isinstance(acquisition_data, ImageSeries) and \
                        (not isinstance(acquisition_data, TwoPhotonSeries)):
                    continue

            if isinstance(acquisition_data, ImageSeries):
                image_series = acquisition_data
                return image_series.rate

        return None

    def get_identifier(self, session_data):
        """
        Get the identifier of one of the data to analyse
        Args:
            session_data: Data we want to know the identifier

        Returns: A hashable object identfying the data

        """
        return session_data.identifier

    def get_intervals_names(self):
        """
        Return a list representing the intervals contains in this data
        Returns:

        """
        if self._nwb_data.intervals is None:
            return []

        intervals = []
        for name_interval in self._nwb_data.intervals.keys():
            intervals.append(name_interval)
        return intervals

    def get_interval_as_data_frame(self, interval_name):
        """
        Return an interval time as a pandas data frame.
        Args:
            interval_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a pandas data frame otherwise

        """
        if interval_name not in self._nwb_data.intervals:
            return None
        return self._nwb_data.intervals[interval_name].to_dataframe()

    def get_interval_times(self, interval_name):
        """
        Return an interval times (start and stop in seconds) as a numpy array of 2*n_times.
        Args:
            interval_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a 2d array

        """
        if interval_name not in self._nwb_data.intervals:
            return None

        df = self._nwb_data.intervals[interval_name].to_dataframe()

        # TODO: See to make it more modulable in case someone will use another name
        if ("start_time" not in df) or \
                ("stop_time" not in df):
            return None

        # time series
        start_time_ts = df["start_time"]
        stop_time_ts = df["stop_time"]

        # it shouldn't be the case
        if len(start_time_ts) != len(stop_time_ts):
            print(f"len(start_time_ts) {len(start_time_ts)} != {len(stop_time_ts)} len(stop_time_ts)")
            return None

        data = np.zeros((2, len(start_time_ts)))
        data[0] = np.array(start_time_ts)
        data[1] = np.array(stop_time_ts)

        return data

    def get_behavioral_epochs_names(self):
        """
        The name of the different behavioral
        Returns:

        """
        if 'behavior' not in self._nwb_data.processing:
            return []

        behavior_nwb_module = self._nwb_data.processing['behavior']
        try:
            behavioral_epochs = behavior_nwb_module.get(name='BehavioralEpochs')
        except KeyError:
            return []
        # a dictionary containing the IntervalSeries in this BehavioralEpochs container
        interval_series = behavioral_epochs.interval_series

        return list(interval_series.keys())

    def get_behavioral_epochs_times(self, epoch_name):
        """
        Return an interval times (start and stop in seconds) as a numpy array of 2*n_times.
        Args:
            epoch_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a 2d array

        """
        if 'behavior' not in self._nwb_data.processing:
            print("'behavior' not in self._nwb_data.processing")
            return None

        behavior_nwb_module = self._nwb_data.processing['behavior']
        try:
            behavioral_epochs = behavior_nwb_module.get(name='BehavioralEpochs')
        except KeyError:
            return None
        # a dictionary containing the IntervalSeries in this BehavioralEpochs container
        interval_series = behavioral_epochs.interval_series

        if epoch_name not in interval_series:
            return None

        interval_serie = interval_series[epoch_name]

        # data: >0 if interval started, <0 if interval ended.
        # timestamps: Timestamps for samples stored in data
        # so far we use only one type of integer, but otherwise as describe in the doc:
        """
        Stores intervals of data. The timestamps field stores the beginning and end of intervals. 
        The data field stores whether the interval just started (>0 value) or ended (<0 value). 
        Different interval types can be represented in the same series by using multiple key values 
        (eg, 1 for feature A, 2 for feature B, 3 for feature C, etc). The field data stores an 8-bit integer. 
        This is largely an alias of a standard TimeSeries but that is identifiable as representing 
        time intervals in a machine-readable way.
        """
        data = interval_serie.data
        time_stamps = interval_serie.timestamps

        data = np.zeros((2, int(len(time_stamps) / 2)))
        index_data = 0
        for i in np.arange(0, len(time_stamps), 2):
            data[0, index_data] = time_stamps[i]
            data[1, index_data] = time_stamps[i+1]
            index_data += 1

        return data

    def get_interval_original_frames(self, interval_name):
        """
        Return an interval times (start and stop in frames) as a numpy array of 2*n_times.
        Args:
            interval_name: Name of the interval to retrieve

        Returns: None if the interval doesn't exists or a 2d array

        """
        if interval_name not in self._nwb_data.intervals:
            return None

        df = self._nwb_data.intervals[interval_name].to_dataframe()

        # TODO: See to make it more modulable in case someone will use another name
        if ("start_original_frame" not in df) or \
                ("stop_original_frame" not in df):
            return None

        # time series
        start_frame = df["start_original_frame"]
        stop_frame = df["stop_original_frame"]

        # it shouldn't be the case
        if len(start_frame) != len(stop_frame):
            print(f"len(start_time_ts) {len(start_frame)} != {len(stop_frame)} len(stop_time_ts)")
            return None

        data = np.zeros((2, len(start_frame)))
        data[0] = np.array(start_frame)
        data[1] = np.array(stop_frame)

        return data

    def __str__(self):
        """
        Return a string representing the session. Here session.identifier
        :return:
        """
        return self._nwb_data.identifier

    def get_behaviors_movie_time_stamps(self):
        """
        return a dict with key the cam id and value np.array with the timestamps of each frame of the behavior movie
        return None if non available
        Returns:

        """
        time_stamps_dict = dict()

        for name, acquisition_data in self._nwb_data.acquisition.items():
            if name.startswith("cam_"):
                time_stamps_dict[name] = np.array(acquisition_data.timestamps)

        return time_stamps_dict

    def get_ci_movie_time_stamps(self):
        """
        return a np.array with the timestamps of each frame of the CI movie
        return None if non available
        Returns:

        """
        if "ci_frames" not in self._nwb_data.acquisition:
            return None
        ci_frames = self._nwb_data.acquisition["ci_frames"]
        return ci_frames.timestamps

    def get_timestamps_range(self):
        """
        Return a tuple of float representing the first and last time stamp with movie recording
        (behavior or ci movie)
        Returns:

        """
        min_time_stamp = None
        max_time_stamp = 0
        ci_movie_time_stamps = self.get_ci_movie_time_stamps()
        if ci_movie_time_stamps is not None:
            max_time_stamp = max(max_time_stamp, np.max(ci_movie_time_stamps))
            min_time_stamp = np.min(ci_movie_time_stamps)

        behavior_time_stamps_dict = self.get_behaviors_movie_time_stamps()
        for behavior_name, behavior_time_stamps in behavior_time_stamps_dict.items():
            max_time_stamp = max(max_time_stamp, np.max(behavior_time_stamps))
            if min_time_stamp is None:
                min_time_stamp = np.min(behavior_time_stamps)
            else:
                min_time_stamp = min(min_time_stamp, np.min(behavior_time_stamps))

        return min_time_stamp, max_time_stamp

from ..utils.constants import LOGConstants, UnitsConstants, MadymoConstants


class Madymo:
    def __init__(self, madymo_file, logger, dynasaur_definitions, name):
        '''
        Initialization/constructor

        :param: binout
        :param: logger
        :param: dynasaur definition
        :param: name

        :return:
        '''
        self._logger = logger
        self._dynasaur_definitions = dynasaur_definitions
        self._data = madymo_file["MODEL_0"]
        self._ids = []
        self._signals = []
        self._data_mapping = {}
        self._name = name

        self._time = []

    # Changed ".value" with [()] in order to get rid of warnings
    def set_madymo_data(self):
        '''

        :return:
        '''
        for key in self._data.keys():
            if key not in self._data_mapping.keys():
                self._data_mapping.update({key: {}})
            for signal in self._data[key].keys():
                if signal == MadymoConstants.COMP:
                    for index, value in enumerate(self._data[key][signal][()].T):
                        if MadymoConstants.CHANNEL_NAME not in self._data_mapping[key].keys():
                            self._data_mapping[key].update(
                                {MadymoConstants.CHANNEL_NAME: ["".join([chr(i) for i in list(value) if i != 0])]})
                        else:
                            self._data_mapping[key][MadymoConstants.CHANNEL_NAME].append(
                                "".join([chr(i) for i in list(value) if i != 0]))
                if signal == MadymoConstants.X_VALUES:
                    self._time.append(self._data[key][signal][()])
                    if UnitsConstants.TIME not in self._data_mapping[key].keys():
                        self._data_mapping[key].update({UnitsConstants.TIME: [self._data[key][signal][()]]})
                    else:
                        self._data_mapping[key][UnitsConstants.TIME].append(self._data[key][signal][()])
                if len(list(self._data[key][signal].attrs.items())):
                    self._signals.append(key + "/" + signal)
                    self._ids.append(
                        ''.join([chr(i) for i in list(self._data[key][signal].attrs.items())[0][1] if i != 0]))
                    if MadymoConstants.IDS not in self._data_mapping[key].keys() and MadymoConstants.SIGNALS not in \
                            self._data_mapping[key].keys():
                        self._data_mapping[key].update({MadymoConstants.IDS: [
                            ''.join([chr(i) for i in list(self._data[key][signal].attrs.items())[0][1] if i != 0])]})
                        self._data_mapping[key].update({MadymoConstants.SIGNALS: [key + "/" + signal]})
                    else:
                        self._data_mapping[key][MadymoConstants.IDS].append(
                            ''.join([chr(i) for i in list(self._data[key][signal].attrs.items())[0][1] if i != 0]))
                        self._data_mapping[key][MadymoConstants.SIGNALS].append(key + "/" + signal)

    def clean_channel_names(self):
        '''

        :return:
        '''
        for key in self._data_mapping.keys():
            for index, channel_name in enumerate(self._data_mapping[key][MadymoConstants.CHANNEL_NAME]):
                if channel_name.startswith("-"):
                    self._data_mapping[key][MadymoConstants.CHANNEL_NAME][index] = "-"
                else:
                    self._data_mapping[key][MadymoConstants.CHANNEL_NAME][index] = channel_name.split(" (")[0]

    def get_time(self):
        '''

        :return:
        '''
        return self._time[0]

    def get_channels_ids_object_name(self, object_name, plugin_name):
        '''

        :param object_name:
        :param plugin_name:
        :return:
        '''
        return self._dynasaur_definitions.get_ids_from_name(object_name, self._name, plugin_name)

    def get_measurement_channel(self, id, channel_name):
        '''

        :param id:
        :param channel_name:
        :return:
        '''
        if id not in self._ids:
            self._logger.emit(LOGConstants.ERROR[0], "ID " + str(id) + " not in ids list, check your def file!")
            return []

        signal_index = self._ids.index(id)

        signal = self._signals[signal_index]

        signal_first_part = signal.split("/")[0]

        if channel_name == UnitsConstants.TIME:
            return self._data_mapping[signal_first_part][UnitsConstants.TIME][0].reshape(-1, 1)

        if signal_first_part not in self._data_mapping.keys():
            self._logger.emit(LOGConstants.ERROR[0], "Signal not in h5 file")
            exit("Signal not in h5 file")

        if channel_name not in self._data_mapping[signal_first_part][MadymoConstants.CHANNEL_NAME]:
            self._logger.emit(LOGConstants.ERROR[0], "Channel not in channel list, check your def file!")
            exit("Channel name not in h5 file")

        index_channel_name = self._data_mapping[signal_first_part][MadymoConstants.CHANNEL_NAME].index(channel_name)

        d = self._data[signal][MadymoConstants.Y_VALUES][index_channel_name]

        return d.reshape(-1, 1)

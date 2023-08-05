import os
import csv
import copy
import numpy as np


from ..io.ISO_MME_Converter import ISOMMEConverter
from ..plugins.plugin import PluginInterface, Plugin
from ..utils.constants import PluginsParamDictDef, DataPluginConstants, DefinitionConstants, LoggerSCRIPT, LOGConstants


class DataPluginController(PluginInterface, Plugin):

    def __init__(self, path_to_def_file, path_def_file_id, data_source):
        '''
        Initialization i.e. call Plugin constructor

        :param: root
        :param: path_to_def_file
        :param: path_def_file_id
        :param: data_source(binout path)
        :param: logger
        :param: dynasaur definition

        :return:
        '''
        Plugin.__init__(self, path_to_def_file=path_to_def_file,  path_def_file_id=path_def_file_id,
                        data_source=data_source, name=DefinitionConstants.DATA_VIS)
        self.init_plugin_data(update=True)
        self._data_dict = {}

    def calculate_and_store_results(self, param_dict):
        '''
        TODO
        do not use extract_script_calc_array_and_title
        :param param_dict:
        :return:
        '''
        json_object = param_dict[PluginsParamDictDef.DYNASAUR_JSON]
        x_name = param_dict[PluginsParamDictDef.X_NAME]
        y_name = param_dict[PluginsParamDictDef.Y_NAME]

        sample_offsets = self._get_sample_offset(param_dict)

        reduced_sample_offsets_x = self._reduce_sample_offset(json_object[DataPluginConstants.X], sample_offsets)
        reduced_sample_offsets_y = self._reduce_sample_offset(json_object[DataPluginConstants.Y], sample_offsets)

        x_data = copy.copy(self._get_data_from_dynasaur_json(json_object=json_object[DataPluginConstants.X],
                                                             data_offsets=reduced_sample_offsets_x))
        if x_name.startswith(DataPluginConstants.TIME):
            x_data_time = self._data[reduced_sample_offsets_x[0][0]].get_interpolated_time()[
                          reduced_sample_offsets_x[0][1]:reduced_sample_offsets_x[0][2]]
            # start_time =self._data.get_time()[reduced_sample_offsets_x]
            x_data -= x_data_time[0] * self._units.second()

        y_data = copy.copy(self._get_data_from_dynasaur_json(json_object=json_object[DataPluginConstants.Y],
                                                             data_offsets=reduced_sample_offsets_y))
        if y_name.startswith(DataPluginConstants.TIME):
            # start_time = self._data.get_time()[[reduced_sample_offsets_x]]
            y_data_time = self._data[reduced_sample_offsets_x[0][0]].get_interpolated_time()[
                          reduced_sample_offsets_x[0][1]:reduced_sample_offsets_x[0][2]]
            y_data -= y_data_time[0] * self._units.second()

        self._store_data_to_dict(part_of=param_dict[DataPluginConstants.DIAGRAM_NAME].split("_")[0],
                                diagram_name="_".join(param_dict[DataPluginConstants.DIAGRAM_NAME].split("_")[1:]),
                                x_data_name=x_name, y_data_name=y_name,
                                x_data=x_data.flatten(), y_data=y_data.flatten())

    def _store_data_to_dict(self, part_of, diagram_name, x_data_name, y_data_name, x_data, y_data):
        '''
        :param separator:
        :param x_data_name:
        :param y_data_name:
        :param x_data:
        :param y_data:
        :return:
        '''
        if part_of not in self._data_dict.keys():
            self._data_dict.update({part_of: {}})

        if diagram_name not in self._data_dict[part_of].keys():
            self._data_dict[part_of].update({diagram_name: {"X": x_data, "x_name": x_data_name,
                                                            "Y": y_data, "y_name": y_data_name}})

    def write_ISO_MME(self, path_to_dir=None, test=False):
        converter = ISOMMEConverter()
        converter.write_ISOMME(path_to_dir=path_to_dir, data=self.get_data(),
                               dynasaur_definitions=self.dynasaur_definitions, logger=self._logger, test=test)

    def write_CSV(self, csv_file_dir, filename=None):
        '''None
        write csv file on the given path

        :param csv_file_dir:

        :return:
        '''
        if os.path.isdir(csv_file_dir) is None:
            self._logger.emit(LOGConstants.ERROR[0], self._name + ": csv_file_dir is not a directory")
            return

        if filename is None:
            filename = self._name + "_" + self._timestamp + ".csv"

        self._logger.emit(LOGConstants.SCRIPT[0], self._name + LoggerSCRIPT.print_statements[1] + csv_file_dir)
        path = os.path.join(csv_file_dir, filename)

        rows = []
        values = []
        d = self._get_padded_data_dict()
        for part_of in d.keys():
            for diagram_name in d[part_of].keys():
                rows.append(part_of + ":" + diagram_name + ":" + d[part_of][diagram_name]["x_name"])
                rows.append(part_of + ":" + diagram_name + ":" + d[part_of][diagram_name]["y_name"])

        for part_of in d.keys():
            for diagram_name in d[part_of].keys():
                values.append(d[part_of][diagram_name]["X"])
                values.append(d[part_of][diagram_name]["Y"])

        with open(path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', lineterminator='\n')
            writer.writerow(rows)
            t_m = list(zip(*values))
            for key in t_m:
                writer.writerow(key)

        self._logger.emit(LOGConstants.SCRIPT[0], self._name + LoggerSCRIPT.print_statements[6] + path)

    def get_data(self, part_of=None, diagram_name=None):
        '''
        Get data from data dict

        :param:

        :return data dict with all data:
        '''
        if part_of is None and diagram_name is None:
            return self._data_dict

        elif part_of is None and diagram_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], "data dictionary is empy")
                return
            return_dict = {}
            for counter, parts_of in enumerate(self._data_dict.keys()):
                if diagram_name not in self._data_dict[parts_of]:
                    if counter == len(self._data_dict.keys()):
                        self._logger.emit(LOGConstants.ERROR[0], diagram_name + "not in data dictionary")
                        return
                else:
                    return_dict.update(self._data_dict[parts_of][diagram_name])

            return return_dict

        elif part_of is not None and diagram_name is None:
            if len(self._data_dict):
                return self._data_dict[part_of]
            else:
                self._logger.emit(LOGConstants.ERROR[0], "data dictionary is empy")
                return

        elif part_of is not None and diagram_name is not None:
            if len(self._data_dict) == 0:
                self._logger.emit(LOGConstants.ERROR[0], "data dictionary is empy")
                return
            if part_of not in self._data_dict.keys():
                self._logger.emit(LOGConstants.ERROR[0], part_of + "not in data dictionary")
                return
            if diagram_name not in self._data_dict[part_of].keys():
                self._logger.emit(LOGConstants.ERROR[0], diagram_name + "not in data dictionary")
                return
            else:
                return self._data_dict[part_of][diagram_name]

    def _get_padded_data_dict(self):
        '''
        add padding to data visualization list
        :param:
        :return:
        '''
        d = copy.deepcopy(self._data_dict)
        length = self._get_maximum_length(d)
        for part_of in d.keys():
            for diagram_name in d[part_of].keys():
                if len(d[part_of][diagram_name]["X"]) < length:
                    index = len(d[part_of][diagram_name]["X"])
                    d[part_of][diagram_name]["X"] = np.concatenate((d[part_of][diagram_name]["X"], ['-'] * (length - index)))
                    d[part_of][diagram_name]["Y"] = np.concatenate((d[part_of][diagram_name]["Y"], ['-'] * (length - index)))
        return d

    def _get_maximum_length(self, data_dict):
        '''
        find max length of data visualization list
        :return max length:
        '''
        length = np.max([len(data_dict[p][d]["X"]) for p in data_dict.keys() for d in data_dict[p].keys()])
        return length

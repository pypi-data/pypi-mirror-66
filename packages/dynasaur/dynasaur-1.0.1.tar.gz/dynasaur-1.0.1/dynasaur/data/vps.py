import h5py
from ..data.dynasaur_definitions import DynasaurDefinitions
from ..utils.logger import ConsoleLogger


class VPSData:

    def __init__(self, vps_file_path, id_file_path):
        print(vps_file_path)
        print(id_file_path)
        self.file_data = {}             # should be wrapped to binout data.

        self._read_id_definitions(id_file_path)
        logger = ConsoleLogger()

        self.dynasaur_definitions = DynasaurDefinitions(logger)
        self.dynasaur_definitions.read_def(id_file_path)

        self._extract_data(vps_file_path, id_file_path)

    def _read_id_definitions(self, id_file_path):
        print(id_file_path)

    def _visitor_func(self, name, node):
        if isinstance(node, h5py.Dataset):
            if node.name.split("/")[-1] == 'res': # result of data
                if "TIME" in node.parent.name.split("/"):
                    print("TIME")
                    print(node.name)

            if node.name.split("/")[-1] == 'res': # result of data
                if "BEAM" in node.parent.name.split("/"):
                    print("BEAM")
                    print(node.name)
                    print(node.value.shape)

            if node.name.split("/")[-1] == 'res': # result of data
                if "NODE" in node.parent.name.split("/"):
                    print("NODE")
                    print(node.name)
                    print(node.value.shape)

        else:
            #TODO more about that later on!
            pass

    def _extract_data(self, vps_file_path, id_file_path):
        with h5py.File(vps_file_path, 'r') as f:
            f['CSMEXPL/multistate'].visititems(self._visitor_func)


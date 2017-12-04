from .wps_hello_docker import HelloDocker
from .wps_snap_general_processing import SnapGeneralProcessing
from .wps_snap_cp_tc_processing import SnapCpTcProcessing
from .wps_generate_dem_processing import GenerateDemProcessing
from .wps_get_cloud_params import GetCloudParams
from .wps_nr102 import Nr102
from .wps_compact_polarimetric_synthesis_with_terrain_correction import CPSWTC

processes = [
    HelloDocker(),
    #SnapCpTcProcessing(),
    #SnapGeneralProcessing(),
    #GenerateDemProcessing(),
    Nr102(),
    GetCloudParams(),
    CPSWTC(),
]
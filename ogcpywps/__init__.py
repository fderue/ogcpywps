from pyramid.config import Configurator
from pywps.app.Service import Service
from ogcpywps.processes import processes
import os


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    current_dir = os.path.dirname(os.path.realpath(__file__))
    parent_dir = os.path.dirname(os.path.realpath(current_dir))
    default_pywpsconfig_filepath = parent_dir+'/ogcpywps.cfg'
    application = Service(processes, [os.getenv('PYWPS_CFG', default_pywpsconfig_filepath)])

    return application

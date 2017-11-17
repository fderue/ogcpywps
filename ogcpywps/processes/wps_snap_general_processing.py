from pywps import Process, LiteralInput, LiteralOutput, OGCUNIT, UOM

import logging
LOGGER = logging.getLogger("PYWPS")


class SnapGeneralProcessing(Process):

    dockerim_name = 'docker-registry.crim.ca/ogc/debian8-snap5-ogc-processingt'
    registry_url = 'docker-registry.crim.ca'
    dockerim_version = 'v1'

    def __init__(self):
        inputs = [
            LiteralInput('input_snap_graph_path', 'Chemin du fichier xml du graphe', data_type='string'),
            LiteralInput('output_directory', 'Chemin de sortie du graphe edite', data_type='string'),
            LiteralInput('WMS_server', 'URI where to register a WMS-compatible output', data_type='string'),
            LiteralInput('Read.file', 'Chemin de l image d entree pour le noeud Read', data_type='string'),
            LiteralInput('Write.file', 'Chemin de sortie de l image filtree pour le noeud Write', data_type='string'),
            LiteralInput('Write.formatName', 'Format de sortie', data_type='string'),
            LiteralInput('Polarimetric-Speckle-Filter.filter', 'Nom du filtre dans snap', data_type='string', min_occurs=0),
            LiteralInput('Polarimetric-Speckle-Filter.numLooksStr', 'Le nombre de vues pour l estimation de l ecart-type du speckle', data_type='string', min_occurs=0),
            LiteralInput('Polarimetric-Speckle-Filter.windowSize', 'Grandeur du filtre', data_type='string', min_occurs=0),
            LiteralInput('queue_name', 'Name of celery queue to send the request', data_type='string'),
        ]
        outputs = [
            LiteralOutput('output', 'Path to output', data_type='string')
        ]

        super(SnapGeneralProcessing, self).__init__(
            self._handler,
            identifier='snap_general_processing',
            title='Snap General Processing',
            abstract='This wps process only shows the process params, '
                     'while the docker params are in the description process itself',
            version='1',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        LOGGER.info("run snap_general_processing")

        input_data_dict = {'process_id': 'snap_general_processing'}
        queue_name = request.inputs['queue_name'][0].data

        for lit_input in self.inputs:
            identifier = lit_input.identifier
            if identifier in request.inputs.keys():
                input_data_dict[identifier] = request.inputs[identifier][0].data

        from ogcservice.celery_request import format_body_request
        request_body = format_body_request(
            dockerim_name=self.dockerim_name,
            dockerim_version=self.dockerim_version,
            registry_url=self.registry_url,
            input_data=input_data_dict,
            param_as_envar=False,
            volume_mapping={})

        response = {'request_body': request_body,
                    'queue_name': queue_name}

        return response

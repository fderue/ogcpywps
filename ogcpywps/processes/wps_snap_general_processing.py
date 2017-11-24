from pywps import Process, LiteralInput, LiteralOutput, OGCUNIT, UOM
import json
import logging
from wps_get_cloud_params import GetCloudParams
LOGGER = logging.getLogger("PYWPS")


class SnapGeneralProcessing(Process):

    dockerim_name = 'docker-registry.crim.ca/ogc/debian8-snap5-ogc-processingt'
    registry_url = 'docker-registry.crim.ca'
    dockerim_version = 'v1'

    def __init__(self):
        inputs = [
            LiteralInput('IaaS_deploy_execute',
                         title='URI of the IaaS resource where the job will be deployed and executed ()',
                         abstract='If the WPS Server contains a Task Queue scheduler, the URI contains two part. The first part is the URI of the Message Broker in the form of amqp://broker_ip:broker_port//. The second part is the Task Queue name. For simplicity, both part are appended in a single string. This input parameter does not support credentials. Credentials for Message brokers are set as a system configuration. The credentials are injected in the environment variables of the VM instance that will host the WPS Server',
                         allowed_values=[json.dumps(broker_queue) for broker_queue in GetCloudParams.broker_queue_list],
                         default=json.dumps(GetCloudParams.broker_queue_list[0]),
                         data_type='string'),
            LiteralInput('IaaS_datastore',
                         title='URI of an IaaS data store where the outputs will stored',
                         abstract='This parameter sets the target for all outputs of the process (HTTPS fileserver, AWS S3, SWIFT, Globus, etc.). Outputs will be staged out in the datastore by the process. The current implementation only supports HTTP fileservers. This input parameter does not support credentials. Credentials for datastores are set as a system configuration. The credentials are injected in the environment variables of the VM instance that runs the Docker Image',
                         data_type='string'),
            LiteralInput('input_snap_graph_path', 'Chemin du fichier xml du graphe', data_type='string'),
            LiteralInput('output_directory', 'Chemin de sortie du graphe edite', data_type='string'),
            LiteralInput('WMS_server', 'URI where to register a WMS-compatible output', data_type='string'),
            LiteralInput('Read.file', 'Chemin de l image d entree pour le noeud Read', data_type='string'),
            LiteralInput('Write.file', 'Chemin de sortie de l image filtree pour le noeud Write', data_type='string'),
            LiteralInput('Write.formatName', 'Format de sortie', data_type='string'),
            LiteralInput('Polarimetric-Speckle-Filter.filter', 'Nom du filtre dans snap', data_type='string', min_occurs=0),
            LiteralInput('Polarimetric-Speckle-Filter.numLooksStr', 'Le nombre de vues pour l estimation de l ecart-type du speckle', data_type='string', min_occurs=0),
            LiteralInput('Polarimetric-Speckle-Filter.windowSize', 'Grandeur du filtre', data_type='string', min_occurs=0),
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

        input_data = {'process_id': 'snap_general_processing'}

        for lit_input in self.inputs:
            identifier = lit_input.identifier
            if identifier in request.inputs.keys() and (identifier != 'IaaS_deploy_execute'):
                input_data[identifier] = request.inputs[identifier][0].data

        from ogcservice.celery_request import format_body_request
        request_body = format_body_request(
            dockerim_name=self.dockerim_name,
            input_data=input_data,
            param_as_envar=True,
            volume_mapping={})

        # TODO check on cloud params
        cloud_params = {
            'IaaS_deploy_execute': json.loads(request.inputs['IaaS_deploy_execute'][0].data),
            'IaaS_datastore': request.inputs['IaaS_datastore'][0].data
        }
        response = {'request_body': request_body,
                    'cloud_params': cloud_params}

        return response

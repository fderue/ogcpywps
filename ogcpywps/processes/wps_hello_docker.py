from pywps import Process, LiteralInput, LiteralOutput
import json
from wps_get_cloud_params import GetCloudParams

import logging
LOGGER = logging.getLogger("PYWPS")


class HelloDocker(Process):
    def __init__(self):
        inputs = [
            LiteralInput('docker_image',
                         title='URI of the Docker Image to be deployed and executed',
                         abstract='The URI contains the full path to a Docker image as used by Docker Daemon, including the host, port, path, image name and version.',# This input parameter does not support credentials. Credentials for private Docker registries are set as a system configuration. The credentials are injected in the environment variables of the VM instance that runs the Docker Image',
                         data_type='string'),
            LiteralInput('IaaS_deploy_execute',
                         title='Json of the IaaS resource where the job will be deployed and executed ()',
                         abstract='Json formatted description of a broker url and the queue name where to send the task.',# This input parameter does not support credentials. Credentials for Message brokers are set as a system configuration. The credentials are injected in the environment variables of the VM instance that will host the WPS Server',
                         allowed_values=[json.dumps(broker_queue) for broker_queue in GetCloudParams.broker_queue_list],
                         default=json.dumps(GetCloudParams.broker_queue_list[0]),
                         data_type='string'),
            LiteralInput('IaaS_datastore',
                         title='URI of an IaaS data store where the outputs will stored',
                         abstract='This parameter sets the target for all outputs of the process (HTTPS fileserver, AWS S3, SWIFT, Globus, etc.).',# Outputs will be staged out in the datastore by the process. The current implementation only supports HTTP fileservers. This input parameter does not support credentials. Credentials for datastores are set as a system configuration. The credentials are injected in the environment variables of the VM instance that runs the Docker Image',
                         data_type='string'),
            LiteralInput('url_to_download', 'url of a file to download', data_type='string'),
            LiteralInput('new_file_name', 'new name to give to the downloaded file', data_type='string'),
        ]
        outputs = [
            LiteralOutput('output', 'Path to output', data_type='string')]

        super(HelloDocker, self).__init__(
            self._handler,
            identifier='hellodocker',
            abstract='Simple WPS to test stage in and out by downloading a file and save it to a file server with a new name',
            title='Hello Docker',
            version='0.1',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        LOGGER.info("run docker app")

        docker_image = request.inputs['docker_image'][0].data

        input_data={}
        for lit_input in self.inputs:
            identifier = lit_input.identifier
            # Avoid cloud params (that should not be in expose to the client ideally)
            if (identifier != 'IaaS_deploy_execute') and (identifier != 'IaaS_datastore'):
                input_data[identifier] = request.inputs[identifier][0].data

        from ogcservice.celery_request import format_body_request

        request_body = format_body_request(
            docker_image=docker_image,
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


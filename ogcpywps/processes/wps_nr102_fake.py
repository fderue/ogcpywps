from pywps import Process, LiteralInput, LiteralOutput
import json

import logging
LOGGER = logging.getLogger("PYWPS")


class Nr102Fake(Process):
    def __init__(self):
        inputs = [
            LiteralInput('docker_image',
                         title='URI of the Docker Image to be deployed and executed',
                         abstract='The URI contains the full path to a Docker image as used by Docker Daemon, including the host, port, path, image name and version. This input parameter does not support credentials. Credentials for private Docker registries are set as a system configuration. The credentials are injected in the environment variables of the VM instance that runs the Docker Image',
                         data_type='string'),
            LiteralInput('IaaS_deploy_execute',
                         title='URI of the IaaS resource where the job will be deployed and executed ()',
                         abstract='If the WPS Server contains a Task Queue scheduler, the URI contains two part. The first part is the URI of the Message Broker in the form of amqp://broker_ip:broker_port//. The second part is the Task Queue name. For simplicity, both part are appended in a single string. This input parameter does not support credentials. Credentials for Message brokers are set as a system configuration. The credentials are injected in the environment variables of the VM instance that will host the WPS Server',
                         default=json.dumps({"BROKER_HOST":"localhost", "BROKER_PORT":5672, "QUEUE_NAME":"celery_tiny"}),
                         data_type='string'),
            LiteralInput('IaaS_datastore',
                         title='URI of an IaaS data store where the outputs will stored',
                         abstract='This parameter sets the target for all outputs of the process (HTTPS fileserver, AWS S3, SWIFT, Globus, etc.). Outputs will be staged out in the datastore by the process. The current implementation only supports HTTP fileservers. This input parameter does not support credentials. Credentials for datastores are set as a system configuration. The credentials are injected in the environment variables of the VM instance that runs the Docker Image',
                         data_type='string'),
            LiteralInput('Radarsat2_data',
                         title='URI from where to download the Radarsat-2 data ZIP',
                         abstract='The Radarsat-2 file is unzipped in the local drive. The product.xml file is located then provided to RSTB/SNAP. The long string identifying the product is used to create temporary directories and to format the output file names',
                         data_type='string'),
            LiteralInput('WMS_server',
                         title='URI where to register a WMS-compatible output',
                         abstract='The process produces an RGB image of the data output. Its smaller footprint is better managed by WMS/WCS servers. The RGB output will be staged out in the specified WMS Server by the process. The output parameter named output_data_WMS_url will contain an URL pointing to this WMS server. The credentials are injected in the environment variables of the VM instance that runs the Docker Image.',
                         data_type='string'),
            LiteralInput('input_graph_url',
                         title='URL where to download the GPT graph used to process the Radarsat-2 data',
                         abstract='Allows a user to provide a different processing graph to the process. In case none is specified, a default graph stored in the application package is used. A graph provided here should present the same Inputs (reads) and Ouputs (writes) as the default graph',
                         data_type='string'),
            LiteralInput('input_graph_parameters',
                         title='KVP used to parametrize the graph itself',
                         abstract='Allows a user to provide customized parameters to the graph in the form of a JSON file. In case none are specified, default values will be used. Currently, the default graph supports Polarimetric-Speckle-Filter.filter, Polarimetric-Speckle-Filter.windowSize and Polarimetric-Speckle-Filter.numLooksStr',
                         data_type='string'),

        ]
        outputs = [
            LiteralOutput('output_data_url',
                          title='URL to data produced by the process',
                          abstract='The URL provided here is dependent on the IaaS_datastore selected. It allows an user to access and download from the Cloud the image data produced by the process. By default in the current implementation, the output data is accessible through HTTP fileservers.',
                          data_type='string'),
            LiteralOutput('output_data_WMS_url',
                          title='URL to WMS layer for the data produced',
                          abstract='The URL provided here is dependent on the WMS_server provided. If no WMS server was specified, this field is left blank. The URL allows an user to access the image data produced by the process in WMS client.',
                          data_type='string'),
        ]


        super(Nr102Fake, self).__init__(
            self._handler,
            identifier='nr102fake',
            abstract='This wps is an empty process to show the describe process documented on confluence',
            title='Cloud WPS Biomass with WCS/WMS support 2',
            version='0.1',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        LOGGER.info("run docker app")

        dockerim_name = request.inputs['docker_image'][0].data

        input_data={}
        for lit_input in self.inputs:
            identifier = lit_input.identifier
            # Avoid cloud params (that should not be in expose to the client ideally)
            if identifier != 'IaaS_deploy_execute':
                input_data[identifier] = request.inputs[identifier][0].data

        from ogcservice.celery_request import format_body_request

        request_body = format_body_request(
            dockerim_name=dockerim_name,
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


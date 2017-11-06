from pywps import Process, LiteralInput, LiteralOutput


import logging
LOGGER = logging.getLogger("PYWPS")


class HelloDocker(Process):
    def __init__(self):
        inputs = [
            LiteralInput('dockerim_name', 'Docker image name', data_type='string'),
            LiteralInput('registry_url', 'Docker image registry url', data_type='string'),
            LiteralInput('dockerim_version', 'Docker image version', data_type='string'),
            LiteralInput('queue_name', 'Name of celery queue to send the request', data_type='string'),
            LiteralInput('url_to_download', 'url of a file to download', data_type='string'),
            LiteralInput('new_file_name', 'new name to give to the downloaded file', data_type='string'),
        ]
        outputs = [
            LiteralOutput('output', 'Path to output', data_type='string')]

        super(HelloDocker, self).__init__(
            self._handler,
            identifier='hellodocker',
            abstract='This wps exposes every parameters to the client of a specific app, '
                     'including the docker params (ows:context)',
            title='Hello Docker',
            version='0.1',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        LOGGER.info("run docker app")

        dockerim_version = request.inputs['dockerim_version'][0].data
        dockerim_name = request.inputs['dockerim_name'][0].data
        queue_name = request.inputs['queue_name'][0].data

        input_data={}
        for lit_input in self.inputs:
            identifier = lit_input.identifier
            input_data[identifier] = request.inputs[identifier][0].data

        registry_url = request.inputs['registry_url'][0].data

        from ogcservice.celery_request import format_body_request

        request_body = format_body_request(
            dockerim_name=dockerim_name,
            dockerim_version=dockerim_version,
            registry_url=registry_url,
            input_data=input_data,
            param_as_envar=True,
            volume_mapping={})

        response = {'request_body': request_body,
                    'queue_name': queue_name}

        return response


from pywps import Process, LiteralInput, LiteralOutput, OGCUNIT, UOM

import logging
LOGGER = logging.getLogger("PYWPS")


class GenerateDemProcessing(Process):

    dockerim_name = 'docker-registry.crim.ca/ogc/debian8-snap5-ogc-processingt'
    registry_url = 'docker-registry.crim.ca'
    dockerim_version = 'v1'

    def __init__(self):
        inputs = [
            LiteralInput('rsat2_product_xml_path', 'rsat2_product_xml_path', data_type='string'),
            LiteralInput('output_directory', 'output_directory', data_type='string'),
            LiteralInput('output_dem_filename', 'output_dem_filename', data_type='string'),
            LiteralInput('download_directory', 'download_directory', data_type='string'),
            LiteralInput('queue_name', 'Name of celery queue to send the request', data_type='string'),
        ]
        outputs = [
            LiteralOutput('output', 'Path to output', data_type='string')]

        super(GenerateDemProcessing, self).__init__(
            self._handler,
            identifier='generate_dem_processing',
            title='Generate Dem Processing',
            abstract='This wps process only shows the process params, '
                     'while the docker params are in the description process itself',
            version='1',
            inputs=inputs,
            outputs=outputs,
            store_supported=True,
            status_supported=True
        )

    def _handler(self, request, response):
        LOGGER.info("run generate_dem_processing")

        input_data_dict = {'process_id': 'generate_dem_processing'}
        queue_name = request.inputs['queue_name'][0].data

        for lit_input in self.inputs:
            identifier = lit_input.identifier
            input_data_dict[identifier] = request.inputs[identifier][0].data

        from pywps.processing.celery_request import format_body_request
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


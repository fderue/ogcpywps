from pywps import Process, LiteralInput, LiteralOutput
from pywps.processing.celery_utils import config_module_dict
import json
import logging
LOGGER = logging.getLogger("PYWPS")


def format_broker_queue(broker_host, broker_port, queue_name):
    return {
        'BROKER_HOST': broker_host,
        'BROKER_PORT': broker_port,
        'QUEUE_NAME': queue_name
    }

class GetCloudParams(Process):

    BROKER_HOST = config_module_dict['BROKER_HOST']
    BROKER_PORT = config_module_dict['BROKER_PORT']
    celery_queue_names = [ws['celery_queue_name'] for ws in config_module_dict['WORKER_SERVICES'].values()]

    def __init__(self):
        inputs = [
        ]
        outputs = [
            LiteralOutput('IaaS_deploy_execute', 'List of (Broker, Celery Queue) available', data_type='string'),
        ]

        super(GetCloudParams, self).__init__(
            self._handler,
            identifier='get_cloud_params',
            abstract='Get cloud parameters',
            title='Get Cloud Parameters',
            version='0.1',
            inputs=inputs,
            outputs=outputs,
            store_supported=False,
            status_supported=False
        )

    def _handler(self, request, response):
        LOGGER.info("run get cloud params")

        broker_queue_list = [format_broker_queue(self.BROKER_HOST, self.BROKER_PORT, queue_name) for queue_name in self.celery_queue_names]
        response.outputs['IaaS_deploy_execute'].data = json.dumps(broker_queue_list)

        return response


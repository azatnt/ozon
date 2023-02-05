import requests, datetime
from config.settings import env
import logging, json

from shop.integrations import IntegrationInterface

logger = logging.getLogger(__name__)


class BaseIntegration(IntegrationInterface):
    _url = env('OZON_BASE_URL')
    _headers = {
        "Client-Id": env('CLIENT_ID'),
        "Api-Key": env('API_KEY')
    }
    _data = {
            "dir": "ASC",
            "filter": {
                "cutoff_from": "2022-08-31T14:15:22Z",
                "cutoff_to": "2030-08-31T14:15:22Z",
                "delivery_method_id": [],
                "provider_id": [],
                "status": "awaiting_deliver",
                "warehouse_id": []
            },
            "limit": 100,
            "offset": 0,
            "with": {
                "analytics_data": True,
                "barcodes": True,
                "financial_data": True,
                "translit": True
            }
        }

    def get_request(self, status):
        self._url = self._url + 'v3/posting/fbs/unfulfilled/list'
        if isinstance(self._data, str):
            self._data = json.loads(self._data)
        # self._data['filter']['cutoff_from'] = date_from
        # self._data['filter']['cutoff_to'] = date_to
        self._data['filter']['status'] = status
        self._data = json.dumps(self._data, indent=4)
        response = requests.post(url=self._url, headers=self._headers, data=self._data, verify=True)
        logger.info('-- response status from get products: {}'.format(response.status_code))
        output_data = response.text
        return output_data




import datetime
import json
import logging
import datetime

from django.core.management import BaseCommand

from shop.api import BaseIntegration
from shop.utils import perform_data_from_api

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        integration = BaseIntegration()
        try:
            # date_from = datetime.datetime.now()
            # date_to = date_from + datetime.timedelta(days=300)
            # date_from = date_from.strftime("%Y-%m-%dT%H:%M:%SZ")
            # date_to = date_to.strftime("%Y-%m-%dT%H:%M:%SZ")
            status = "awaiting_deliver"
            output = integration.get_request(status)
            perform_data_from_api(json.loads(output))
        except Exception as ex:
            logger.error(f'-- Ozon integration error: {ex}')

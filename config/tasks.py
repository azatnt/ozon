from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.management import call_command

logger = get_task_logger(__name__)


@shared_task
def reports_daily_awaiting():
    call_command("get_products_list_awaiting",)


@shared_task
def reports_daily_packaging():
    call_command("get_products_list_packaging",)
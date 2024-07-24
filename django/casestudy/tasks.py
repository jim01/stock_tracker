from celery import shared_task
from celery.utils.log import get_task_logger
from .settings import STOCKS_API
from .api import Stocks
from casestudy.models import Security
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json


"""
Tasks that run in background adding/updating Stocks and their prices
tasks are scheduled from Celery service
"""

logger = get_task_logger(__name__)

@shared_task
def save_tickers():
    logger.info("saving tickers")
    api = Stocks(STOCKS_API["host"], STOCKS_API["key"])
    tickers = api.get_tickers()
    Security.add_tickers(tickers)


@shared_task
def update_pricing():
    logger.info("saving prices")
    # create a dictionary of security to fetch and check price data against
    securities = dict((m.ticker, m) for m in Security.objects.all())
    api = Stocks(STOCKS_API["host"], STOCKS_API["key"])
    price_data = api.get_prices(list(securities.keys()))
    Security.update_prices(securities, price_data)

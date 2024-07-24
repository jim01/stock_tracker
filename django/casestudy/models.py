"""
Django models for the casestudy service.

We have added the initial Security model for you with common fields for a
stock market security. Add any additional fields you need to this model to
complete the case study.

Once you have added a new field to the Security model or created any new
models you can run 'make migrations' to create the new Django migration files
and apply them to the database.

https://docs.djangoproject.com/en/4.2/topics/db/models/
"""
from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from decimal import Decimal
import json


class Security(models.Model):
    """
    Represents a Stock or ETF trading in the US stock market, i.e. Apple,
    Google, SPDR S&P 500 ETF Trust, etc.
    """

    # The security’s name (e.g. Netflix Inc)
    name = models.TextField(null=False, blank=False)

    # The security’s ticker (e.g. NFLX)
    ticker = models.TextField(null=False, blank=False)

    # This field is used to store the last price of a security
    last_price = models.DecimalField(
        null=True, blank=True, decimal_places=2, max_digits=11,
    )

    users = models.ManyToManyField(User, related_name='securities', null=True, blank=True)

    # TODO: Add additional fields here.
    # ex: description, exchange name, etc.

    @staticmethod
    def add_tickers(tickers):
        """
        adds securities to the database
        :param tickers: {StockTicker:StockName,..}
        :return: void
        """
        securities = dict((m.ticker, m) for m in Security.objects.all())
        # if there were more these would be batched. Or have webhook for when they are added / updated
        for key in tickers:
            if key not in securities:
                print("Added new security: " + key)
                security = Security()
                security.ticker = key
                security.name = tickers[key]
                security.save()
            elif tickers[key] != securities[key].name:
                securities[key].name = tickers[key]
                securities[key].save()

    @staticmethod
    def update_prices(securities, price_data):
        """
        updates pricing and publishes update to channel
        :param securities: ditc of {stockerTicker: SecurityObject}
        :param price_data: dict of {stockTicker:newPrice} ex {XYZ:12.99,...}
        :return: void
        """
        # create a dictionary of security to fetch and check price data against
        channel_layer = get_channel_layer()
        for ticker in price_data:
            if ticker not in securities:
                print("security missing for: " + ticker)
                continue

            if price_data[ticker] is None:
                print("null price for: " + ticker)
                continue

            stock = securities[ticker]
            if stock.last_price is None or '{0:.2f}'.format(price_data[ticker]) != '{0:.2f}'.format(stock.last_price):
                #print('{0:.2f}'.format(stock.last_price) + " = " + '{0:.2f}'.format(price_data[ticker]))
                stock.last_price = price_data[ticker]
                stock.save()

                # push update to users
                async_to_sync(channel_layer.group_send)(
                    "ticker_%s" % stock.ticker,
                    {
                        "type": "send_ticker_update",
                        "message": json.dumps({stock.ticker: str(stock.last_price)})
                    }
                )

from djmoney.contrib.exchange.backends.base import BaseExchangeBackend


class TestExchangeBackend(BaseExchangeBackend):

    name = 'test'

    def get_rates(self, **kwargs):
        return {
            'USD': 1.0,
            'EUR': 1.5,
            'CAD': 2.0,
        }

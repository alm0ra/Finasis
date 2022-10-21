from exchange_connector.services.interfaces.base_exchange import BaseExchange
from signal_center.models import NewSignal
from decimal import Decimal


class TradeHandler:
    LIMIT_ORDER = 'limit'
    MARKET_ORDER = 'market'

    def __init__(self, exchange_connector: BaseExchange, signal: NewSignal):
        self.connector = exchange_connector
        self.signal = signal

    def submit_signal(self) -> None:
        pass

    def check_is_limit_or_market(self) -> str:
        if True:
            return self.MARKET_ORDER
        else:
            return self.LIMIT_ORDER

    def get_real_time_price(self) -> Decimal:
        pass

    def check_if_coin_exist_in_exchange(self) -> bool:
        if True:
            pass

        raise Exception("Coin Does Not Exist")

import abc

__all__ = ["BaseExchange"]


class BaseExchange(abc.ABC):
    @abc.abstractmethod
    def create_market_order(self, symbol, side, amount, params, leverage, margin_mode):
        pass

    @abc.abstractmethod
    def create_stop_market_order(self, symbol, side, stop_price, amount, leverage, params):
        pass

    @abc.abstractmethod
    def create_take_profit_market_order(self, symbol, side, stop_price, amount, leverage, params):
        pass

    @abc.abstractmethod
    def create_limit_order(self, symbol, side, amount, price, params, margin_mode='isolated'):
        pass

    @abc.abstractmethod
    def create_stop_order(self, symbol, side, amount, price, stop_price, params={}):
        pass

    @abc.abstractmethod
    def create_take_profit_order(self, symbol, side, amount, price, stop_price, params):
        pass

    @abc.abstractmethod
    def cancel_order(self, symbol, order_id, order_type=None):
        pass

    @abc.abstractmethod
    def cancel_all_open_orders(self, symbol):
        pass

    @abc.abstractmethod
    def set_leverage(self, symbol, leverage, margin_mode='isolated', params={}):
        pass

    @abc.abstractmethod
    def set_margin_type(self, symbol, leverage, margin_type, params={}):
        pass

    @abc.abstractmethod
    def get_account_info(self):
        pass

    @abc.abstractmethod
    def get_account_balance(self):
        pass

    @abc.abstractmethod
    def get_open_orders(self, symbol=None, params={}):
        pass

    @abc.abstractmethod
    def get_all_orders(self):
        pass

    @abc.abstractmethod
    def get_all_orders_per_symbol(self, symbol, params={}):
        pass

    @abc.abstractmethod
    def get_order_status(self, symbol, order_id, order_type=None, client_order_id=None, params={}):
        pass

    @abc.abstractmethod
    def get_positions_info(self, symbol):
        pass

    @abc.abstractmethod
    def get_all_positions(self, symbol):
        pass

    @abc.abstractmethod
    def get_user_trades(self, symbol=None, limit=None, since=None, params={}):
        pass

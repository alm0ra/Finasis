import ccxt
from exchange_connector.services.interfaces import BaseOkex, BaseExchange

__all__ = ["OKexFutureMarket"]


class OKexFutureMarket(BaseExchange, BaseOkex):
    """
        this class is used for okex future market

    """

    def create_market_order(self, symbol, side, amount, params, leverage, margin_mode):
        type_ = 'market'
        symbol = self.okex_symbol_changer(symbol)
        amount = self.okex_minimum_lot(symbol, amount)
        # update params
        params.update({
            'tdMode': margin_mode
        })
        self.exchange_api.options['createMarketBuyOrderRequiresPrice'] = False
        data = self.exchange_api.create_order(symbol=symbol, type=type_, side=side, amount=amount, params=params)
        return data

    def create_stop_market_order(self, symbol, side, stop_price, amount, leverage, params):
        amount = float(amount) if amount else None
        symbol = self.okex_symbol_changer(symbol)
        amount = self.okex_minimum_lot(symbol, amount)
        data = self.okex_place_algo_order(
            symbol=symbol,
            side=side,
            trade_mode='isolated',
            order_type='conditional',
            size=amount,
            sl_trigger_price=stop_price,
            sl_order_price='-1',
            params=params
        )
        data = self.okex_get_algo_order(algo_id=data['data'][0]['algoId'], order_type="conditional",
                                        method='single_order')

        del data['data'][0]['tpTriggerPx']
        del data['data'][0]['tpOrdPx']
        return data

    def create_take_profit_market_order(self, symbol, side, stop_price, amount, leverage, params):
        symbol = self.okex_symbol_changer(symbol)
        amount = self.okex_minimum_lot(symbol, amount)
        data = self.okex_place_algo_order(
            symbol=symbol,
            side=side,
            order_type="conditional",
            trade_mode='isolated',
            size=amount,
            tp_trigger_price=stop_price,
            tp_order_price='-1',
            params=params
        )
        data = self.okex_get_algo_order(algo_id=data['data'][0]['algoId'], order_type='conditional',
                                        method='single_order')
        del data['data'][0]['slTriggerPx']
        del data['data'][0]['slOrdPx']
        return data

    def create_limit_order(self, symbol, side, amount, price, params, margin_mode='isolated'):
        type_ = 'limit'
        symbol = self.okex_symbol_changer(symbol)
        amount = self.okex_minimum_lot(symbol, amount)
        # update params add trade mode
        params.update({'tdMode': margin_mode})
        self.exchange_api.options['createMarketBuyOrderRequiresPrice'] = False

        order_data = self.exchange_api.create_order(
            symbol=symbol,
            type=type_,
            side=side,
            amount=amount,
            price=price,
            params=params
        )
        return self.exchange_api.fetch_order(id=order_data['id'], symbol=symbol)

    def create_stop_order(self, symbol, side, amount, price, stop_price, params={}):
        symbol = self.okex_symbol_changer(symbol)
        amount = self.okex_minimum_lot(symbol, amount)
        data = self.okex_place_algo_order(
            symbol=symbol,
            side=side,
            trade_mode='isolated',
            order_type='conditional',
            size=amount,
            sl_trigger_price=stop_price,
            sl_order_price=price,
            params=params
        )

        data = self.okex_get_algo_order(algo_id=data['data'][0]['algoId'], order_type="conditional",
                                        method='single_order')
        del data['data'][0]['tpTriggerPx']
        del data['data'][0]['tpOrdPx']
        return data

    def create_take_profit_order(self, symbol, side, amount, price, stop_price, params):
        symbol = self.okex_symbol_changer(symbol)
        amount = self.okex_minimum_lot(symbol, amount)
        data = self.okex_place_algo_order(symbol=symbol, side=side, trade_mode='isolated',
                                          order_type='conditional', size=amount, tp_trigger_price=stop_price,
                                          tp_order_price=price, params=params)

        data = self.okex_get_algo_order(algo_id=data['data'][0]['algoId'], order_type="conditional",
                                        method='single_order')
        del data['data'][0]['slTriggerPx']
        del data['data'][0]['slOrdPx']
        return data

    def cancel_order(self, symbol, order_id, order_type=None):
        symbol = self.okex_symbol_changer(symbol)
        if order_type == 'stop_loss' or order_type == 'take_profit' or order_type == "conditional"\
                or order_type == "oco":
            self.okex_cancel_algo_order(symbol, algo_ids=[order_id])
            return True

        # cancel regular order
        self.exchange_api.cancel_order(int(order_id), symbol)
        return True

    def cancel_all_open_orders(self, symbol):
        symbol = self.okex_symbol_changer(symbol)
        self.okex_cancel_all_open_orders(symbol)
        return True

    def set_leverage(self, symbol, leverage, margin_mode='isolated', params={}):
        symbol = self.okex_symbol_changer(symbol)
        self.okex_set_leverage(
            symbol=symbol,
            leverage=leverage,
            margin_mode=margin_mode,
            params=params
        )
        return True

    def set_margin_type(self, symbol, leverage, margin_type, params={}):

        symbol = self.okex_symbol_changer(symbol)
        self.okex_set_leverage(
            symbol=symbol,
            leverage=leverage,
            margin_mode=margin_type,
            params=params
        )
        return True

    def get_account_info(self):
        return self.exchange_api.fetch_balance()

    def get_account_balance(self):
        return self.exchange_api.fetch_balance()

    def get_open_orders(self, symbol=None, params={}):

        algo_orders = []
        if symbol:
            symbol = self.okex_symbol_changer(symbol)

        algo_orders = self.okex_get_all_algo_orders(symbol=symbol)

        data = self.exchange_api.fetch_open_orders(symbol=symbol, params=params)
        if algo_orders:
            data.extend(algo_orders)
        return data

    def get_all_orders(self):
        return self.exchange_api.fetch_closed_orders(
            params={'instType': 'SWAP'}
        )

    def get_all_orders_per_symbol(self, symbol, params={}):
        symbol = self.okex_symbol_changer(symbol)
        # get all regular orders
        data = self.exchange_api.fetch_open_orders(symbol=symbol)
        data = [data[0]['info']]
        # get algo orders
        algo_orders = self.okex_get_all_algo_orders(symbol=symbol)
        if algo_orders:
            data.extend(algo_orders)
        return data

    def get_all_positions(self, symbol):
        symbol = self.okex_symbol_changer(symbol)
        return self.exchange_api.fetch_position(symbol)

    def get_order_status(self, symbol, order_id, order_type=None, client_order_id=None, params={}):

        symbol = self.okex_symbol_changer(symbol)

        # get algo orders in OKEx
        if order_type == 'stop_loss' or order_type == 'take_profit' or order_type=="conditional":
            order_type = 'conditional'

        if order_type == 'oco' or order_type == 'trigger' or order_type == 'iceberg' or order_type == 'twap' \
                or order_type == 'conditional':
            try:
                return self.okex_get_algo_order(algo_id=order_id, order_type=order_type)

            except ccxt.OrderNotFound:
                return self.okex_get_algo_order_history(order_type=order_type, algo_id=order_id)

    def get_positions_info(self, symbol):

        symbol = self.okex_symbol_changer(symbol)
        return self.exchange_api.fetch_position(symbol)

    def get_user_trades(self, symbol=None, limit=None, since=None, params={}):
        if symbol:
            symbol = self.okex_symbol_changer(symbol)
        return self.exchange_api.fetch_my_trades(
            symbol=symbol,
            limit=limit,
            since=since,
            params={"instType": "SWAP"}
        )


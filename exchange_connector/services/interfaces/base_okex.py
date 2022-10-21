import ccxt
from math import floor
from django.conf import settings

__all__ = ["BaseOkex"]


class BaseOkex:
    def __init__(self, secret_key: str, api_key: str, market_type: str, password=None) -> None:
        self.exchange_api = ccxt.okex5(
            {
                'apiKey': api_key,
                'secret': secret_key,
                'password': password,
                'options': {
                    'defaultType': market_type,
                },
                'enableRateLimit': True
             })

        if settings.PROXY_IP and settings.PROXY_PORT:
            self.exchange_api.proxies = {
                'http': f'socks5h://{settings.PROXY_IP}:{settings.PROXY_PORT}',
                'https': f'socks5h://{settings.PROXY_IP}:{settings.PROXY_PORT}',
            }

    @staticmethod
    def okex_symbol_changer(symbol):
        # change symbol from XLM/USDT ==> XLM-USDT-SWAP
        return symbol.replace('/', '-') + '-SWAP'

    def okex_minimum_lot(self, symbol, amount):
        """
        this function is written for calculate amount size in lot (OKEx SWAP contacts)
        """

        data = self.exchange_api.fetch_markets_by_type(
            type='SWAP', params={
                'instId': symbol
            })

        min_lot = float(data[0]['info']['ctVal'])
        return floor(amount / min_lot) if amount > min_lot else 1

    def okex_place_algo_order(self, symbol, side, order_type, size, trade_mode='isolated', ccy=None,
                              position_side=None, tp_trigger_price=None, tp_order_price=None, sl_trigger_price=None,
                              sl_order_price=None, tgt_ccy=None, params={}):
        """
        this function is written to place an algo order in OKEx
        use AlgoOrder for stop orders See: https://www.okex.com/docs-v5/en/#rest-api-trade-place-algo-order
        """

        args = {
            "instId": symbol,
            "tdMode": trade_mode,
            "side": side,
            "ordType": order_type,
            "sz": size
        }

        if ccy:
            args['ccy'] = ccy
        if position_side:
            args['posSide'] = position_side
        if tp_trigger_price:
            args['tpTriggerPx'] = tp_trigger_price
        if tp_order_price:
            args['tpOrdPx'] = tp_order_price
        if sl_trigger_price:
            args['slTriggerPx'] = sl_trigger_price
        if sl_order_price:
            args['slOrdPx'] = sl_order_price
        if tgt_ccy:
            args['tgtCcy'] = tgt_ccy
        args.update(params)

        return self.exchange_api.privatePostTradeOrderAlgo(args)

    def okex_get_algo_history(self, order_type, state=None, algo_id=None, instrument_type='SPOT', symbol=None,
                              after=None, before=None, limit=None, params={}):
        """
        this function is written for get algo order history in OKEx
        See : https://www.okex.com/docs-v5/en/?python#rest-api-trade-get-algo-order-history
        """
        args = {
            'instType': instrument_type,
            'ordType': order_type
        }

        if state:
            args['state'] = state
        if algo_id:
            args['algoId'] = algo_id
        if symbol:
            args['instId'] = symbol
        if after:
            args['after'] = after
        if before:
            args['before'] = before
        if limit:
            args['limit'] = limit

        args.update(params)

        return self.exchange_api.privateGetTradeOrdersAlgoHistory(params)

    def okex_get_algo_order_history(self, order_type, state=None, algo_id=None, instrument_type=None,
                                    instrument_id=None, after=None, before=None, limit=None, params={}):
        args = {}
        if order_type:
            args["ordType"] = order_type
        if state:
            args["state"] = state
        if algo_id:
            args["algoId"] = algo_id
        if instrument_id:
            args["instId"] = instrument_id
        if instrument_type:
            args["instType"] = instrument_type
        if after:
            args["after"] = after
        if before:
            args["before"] = before
        if limit:
            args["limit"] = limit

        args.update(params)

        return self.exchange_api.privateGetTradeOrdersAlgoHistory(args)

    def okex_get_algo_order(self, order_type, algo_id=None, instrument_type=None, instrument_id=None, after=None,
                            before=None, limit=None, method='general', params={}):
        """
        this function is written for getting algo order status
        """
        args = {}
        if order_type:
            args["ordType"] = order_type
        if algo_id:
            args["algoId"] = algo_id
        if instrument_id:
            args["instId"] = instrument_id
        if instrument_type:
            args["instType"] = instrument_type
        if after:
            args["after"] = after
        if before:
            args["before"] = before
        if limit:
            args["limit"] = limit

        args.update(params)

        return self.exchange_api.privateGetTradeOrdersAlgoPending(args)

    def okex_cancel_algo_order(self, symbol, algo_ids):
        """
        this function is written for cancel algo order or algo orders
        """

        # create input template for several order ids (a list of order ids
        args = [self.cancel_order_input_template(item, symbol, 'oco') for item in algo_ids]
        return self.exchange_api.privatePostTradeCancelAlgos(args)

    @staticmethod
    def cancel_order_input_template(order_id, symbol, type):
        """
        this function is used in cancel all order marker SPOT,
        and it prepares input parameters for a method in okex for 2 type of order regular or oco
        """
        if type != 'regular':
            return {
                "algoId": order_id,
                "instId": symbol
            }
        return {
            "instId": symbol,
            "ordId": order_id
        }

    def okex_cancel_multiple_orders(self, order_ids, symbol):
        """
        this function is written for cancel a group of orders ( regular orders in OKEx)
        See: https://www.okex.com/docs-v5/en/?python#rest-api-trade-cancel-multiple-orders
        """
        args = [self.cancel_order_input_template(item, symbol, 'regular') for item in order_ids]
        return self.exchange_api.privatePostTradeCancelBatchOrders(args)

    def okex_cancel_all_open_orders(self, symbol):
        """
        this function is written to cancel all open order in OKEx
        in OKEx orders are 2 type (regular orders and algo orders)
        OKEx use algo orders for stop loss / take profit / OCO order
        for more information checkout this link:
        See: https://www.okex.com/docs-v5/en/?python#rest-api-trade-place-algo-order
        """

        # make a list from order ids
        order_id_list = [item['info']['ordId'] for item in self.exchange_api.fetch_open_orders(symbol=symbol)]

        # make a dictionary from order ids
        if order_id_list:
            self.okex_cancel_multiple_orders(order_ids=order_id_list, symbol=symbol)
        # cancel algo order

        # get all conditional and oco open algo order
        conditional_algo_orders = self.okex_get_algo_order(order_type='conditional', instrument_id=symbol)
        oco_algo_orders = self.okex_get_algo_order(order_type='oco', instrument_id=symbol)
        trigger_algo_orders = self.okex_get_algo_order(order_type='trigger', instrument_id=symbol)

        # concat conditional and oco algo ids
        algo_order_id = [item['algoId'] for item in conditional_algo_orders['data']]
        algo_order_id.extend([item['algoId'] for item in oco_algo_orders['data']])
        algo_order_id.extend([item['algoId'] for item in trigger_algo_orders['data']])
        if algo_order_id:
            # cancel algo orders
            self.okex_cancel_algo_order(symbol, algo_order_id)

        return True

    def okex_set_leverage(self, margin_mode, leverage, symbol=None, currency=None, position_side=None, params={}):
        """
        this function is written for setting margin mode and leverage of a symbol
        """
        args = {
            'lever': leverage,
            'mgnMode': margin_mode,
        }

        if symbol:
            args['instId'] = symbol
        if currency:
            args['ccy'] = currency
        if position_side:
            args['posSide'] = position_side

        args.update(params)

        response = self.exchange_api.privatePostAccountSetLeverage(args)
        return response

    def okex_get_trade_history(self, instrument_type, symbol=None, order_type=None, state=None, category=None,
                               after=None, before=None, limit=None, params={}):
        """
        this function is written for Retrieve the completed order data for the last 7 days, and the incomplete orders
            that have been cancelled are only reserved for 2 hours.
        checkout this link:
        https://www.okex.com/docs-v5/en/?python#rest-api-trade-get-order-history-last-7-days
        """

        args = {
            'instType': instrument_type
        }

        if symbol:
            args['instId'] = symbol
        if order_type:
            args['ordType'] = order_type
        if state:
            args['state'] = state
        if category:
            args['category'] = category
        if after:
            args['after'] = after
        if before:
            args['before'] = before
        if limit:
            args['limit'] = limit

        args.update(params)

        return self.exchange_api.privateGetTradeOrdersHistory(args)

    def okex_get_all_algo_orders(self, instrument_type='SWAP', symbol=None):
        """
        this function is written for getting all algo orders
        it get all conditional , OCO and trigger algo orders and fetch responses
        """
        conditional_algo_orders = self.okex_get_algo_order(order_type='conditional', instrument_id=symbol,
                                                           instrument_type=instrument_type)

        oco_algo_orders = self.okex_get_algo_order(order_type='oco', instrument_id=symbol,
                                                   instrument_type=instrument_type)

        trigger_algo_orders = self.okex_get_algo_order(order_type='trigger', instrument_id=symbol,
                                                       instrument_type=instrument_type)

        algo_orders = conditional_algo_orders['data'] + oco_algo_orders['data'] + trigger_algo_orders['data']

        return algo_orders

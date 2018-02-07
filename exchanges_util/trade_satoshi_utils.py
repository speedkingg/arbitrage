# -*- coding: utf-8 -*-

# <installed>
#  requests

import requests

# API URL
trade_satoshi_qpi_market_summaries = "https://tradesatoshi.com/api/public/getmarketsummaries"
trade_satoshi_qpi_currencies = " https://tradesatoshi.com/api/public/getcurrencies"
trade_satoshi_qpi_order_book = "https://tradesatoshi.com/api/public/getorderbook"


class TradeSatoshiUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_market_price():
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        """
        trade_satoshi_market_summaries = requests.get(trade_satoshi_qpi_market_summaries).json()["result"]
        satoshi_json = dict()
        satoshi_json['exchange_name'] = 'trade_satoshi'  # 取引所名入力

        # 終値、取引量取得
        for record in trade_satoshi_market_summaries:
            satoshi_json[record['market']] = {
                'price': "%f" % record['last'],
                'volume': "%f" % record['volume']
            }

        # 通貨のfull name取得
        satoshi_json = TradeSatoshiUtils.get_currency_full_name(satoshi_json)

        return satoshi_json

    @staticmethod
    def get_currency_full_name(response_store_json):
        """
        受け取ったjson内のデータを参照し通貨のfull_nameを取得する
        :param: response_store_json
                 <json> {exchange_name, currency_pair:{last_price,volume} * n}
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        """
        trade_satoshi_get_currencies = requests.get(trade_satoshi_qpi_currencies).json()["result"]
        for key in response_store_json.keys():
            for item in trade_satoshi_get_currencies:
                if item['currency'] == key[0:len(item['currency'])]:
                    response_store_json[key]['coin_name'] = item['currencyLong']
                    continue
        return response_store_json

    @staticmethod
    def get_order_book(currency_pair, trade_type, depth):
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :param: currency_pair <str> 通貨ペア
        :param: type <str> 所得オーダー数(sell/buy)
        :param: depth <int> 所得オーダー数(n)
        :return: <list> {exchange_name, type:[{quantity, rate} * n}] }
        """
        api_options = "?" \
                      + "market=" + str(currency_pair) \
                      + "&type=" + str(trade_type) \
                      + "&depth=" + str(depth)

        order_book = requests.get(trade_satoshi_qpi_order_book + api_options).json()["result"]

        # getしたjsonを独自フォーマットに直す
        order_book_response = list()
        depth_count = 0
        for record in order_book[trade_type]:
            order_book_response_record = dict()
            order_book_response_record['price'] = "%f" % record['rate']
            order_book_response_record['quantity'] = "%f" % record['quantity']
            order_book_response.append(order_book_response_record)

            depth_count += 1
            if depth_count == depth:
                break

        return order_book_response

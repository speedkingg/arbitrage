# -*- coding: utf-8 -*-

# <installed>
#  requests

import requests
# binanceでは通貨名のfull nameが所得できないので、trade satoshiで照会する
from exchanges_util.trade_satoshi_utils import TradeSatoshiUtils

# 独自クラスインスタンス化
trade_satoshi = TradeSatoshiUtils()

# API URL
binance_qpi_ticker = "https://api.binance.com/api/v1/ticker/24hr"
binance_qpi_depth = "https://api.binance.com/api/v1/depth"


class BinanceUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_market_price():
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        """
        binance_tickers = requests.get(binance_qpi_ticker).json()
        binance_json = dict()
        binance_json['exchange_name'] = 'binance'  # 取引所名入力

        # 終値、取引量取得
        for ticker in binance_tickers:
            symbol = ticker['symbol']
            # symbolを整形(ex:ETHBTC → ETH_BTC)
            market_name = symbol[0:len(symbol)-3] + "_" + symbol[-3:len(symbol)]
            binance_json[market_name] = {
                'price': "%f" % float(ticker['prevClosePrice']),
                'volume': "%f" % float(ticker['volume'])
            }

        # TODO binance apiでは通貨名のfull nameが所得できないので、
        #      暫定的にtrade satoshiで照会する
        binance_json = trade_satoshi.get_currency_full_name(binance_json)

        return binance_json

    @staticmethod
    def get_order_book(currency_pair, trade_type, depth):
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :param: currency_pair <str> 通貨ペア
        :param: type <str> 所得オーダー数(sell/buy)
        :param: depth <int> 所得オーダー数(n)
        :return: <list> {exchange_name, type:[{quantity, rate} * n}] }
        """
        api_options = "?" + "symbol=" + str(currency_pair).replace("_", "")

        order_book = requests.get(binance_qpi_depth + api_options).json()

        if trade_type == "buy":
            trade_type = "bids"
        elif trade_type == "sell":
            trade_type = "asks"

        # getしたjsonを独自フォーマットに直す
        order_book_response = list()
        depth_count = 0
        for record in order_book[trade_type]:
            order_book_response_record = dict()
            order_book_response_record['price'] = "%f" % float(record[0])  # 0番目がprice
            order_book_response_record['quantity'] = "%f" % float(record[1])  # 1番目がamount
            order_book_response.append(order_book_response_record)

            depth_count += 1
            if depth_count == depth:
                break

        return order_book_response

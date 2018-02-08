# -*- coding: utf-8 -*-

# <installed>
#  requests

import requests

# API URL
bittrex_qpi_market_summaries = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
bittrex_qpi_markets = "https://bittrex.com/api/v1.1/public/getmarkets"
bittrex_qpi_order_book = "https://bittrex.com/api/v1.1/public/getorderbook"


class BittrexUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_market_price():
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        """
        bittrex_market_summaries = requests.get(bittrex_qpi_market_summaries).json()['result']
        bittrex_markets = requests.get(bittrex_qpi_markets).json()['result']

        bittrex_json = dict()
        bittrex_json['exchange_name'] = 'bittrex'  # 取引所名入力

        # 終値、取引量取得
        for market_summary in bittrex_market_summaries:
            market_name = market_summary['MarketName']

            # market_nameを整形(ex:BTC-ETH → ETH_BTC)
            separator_position_number = market_name.find("-")
            base_currency_name = market_name[:separator_position_number]
            market_currency_name = market_name[separator_position_number + 1:]
            market_name = market_currency_name + "_" + base_currency_name

            bittrex_json[market_name] = {
                'price': "%f" % float(market_summary['Last']),
                'volume': "%f" % float(market_summary['BaseVolume'])
            }

            # 通貨のfull name取得
            for market in bittrex_markets:
                if market_currency_name == market['MarketCurrency']:
                    bittrex_json[market_name]['coin_name'] = market['MarketCurrencyLong']
                    break

        return bittrex_json

    @staticmethod
    def get_order_book(currency_pair, trade_type, depth):
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :param: currency_pair <str> 通貨ペア
        :param: type <str> 所得オーダー数(sell/buy)
        :param: depth <int> 所得オーダー数(n)
        :return: <list> {exchange_name, type:[{quantity, rate} * n}] }
        """

        # market_nameを整形(ex:ETH_BTC → BTC-ETH)
        separator_position_number = currency_pair.find("_")
        base_currency_name = currency_pair[separator_position_number + 1:]
        market_currency_name = currency_pair[:separator_position_number]
        currency_pair = base_currency_name + "-" + market_currency_name

        api_options = "?" + "market=" + str(currency_pair) \
                      + "&" + "type=" + str(trade_type)

        order_book = requests.get(bittrex_qpi_order_book + api_options).json()['result']

        # getしたjsonを独自フォーマットに直す
        order_book_response = list()
        depth_count = 0
        for record in order_book:
            order_book_response_record = dict()
            order_book_response_record['price'] = "%f" % float(record['Rate'])
            order_book_response_record['quantity'] = "%f" % float(record['Quantity'])
            order_book_response.append(order_book_response_record)

            depth_count += 1
            if depth_count == depth:
                break

        return order_book_response

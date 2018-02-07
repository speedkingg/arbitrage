# -*- coding: utf-8 -*-

# <installed>
#  requests

import requests

# API URL
coin_exchange_api_market_summaries = "https://www.coinexchange.io/api/v1/getmarketsummaries"
coin_exchange_api_markets = "https://www.coinexchange.io/api/v1/getmarkets"
coin_exchange_api_order_book = "https://www.coinexchange.io/api/v1/getorderbook"


class CoinExchangeUtils:

    def __init__(self):
        pass

    @staticmethod
    def get_market_price():
        """
        価格取得(getしたjsonを独自フォーマットに直す)
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        """
        coin_exchange_market_summaries = requests.get(coin_exchange_api_market_summaries).json()["result"]
        market_summaries_json = {}

        for market_summary in coin_exchange_market_summaries:
            market_summaries_json[market_summary['MarketID']] = {
                'price': "%f" % float(market_summary['LastPrice']),
                'volume': "%f" % float(market_summary['Volume'])
            }
        # ペア情報を取得
        coin_exchange_markets = requests.get(coin_exchange_api_markets).json()["result"]
        markets_json = {}
        for market in coin_exchange_markets:
            markets_json[market['MarketID']] = {
                'pair': market['MarketAssetCode'] + "_" + market['BaseCurrencyCode'],
                'coin_full_name': market['MarketAssetName'],
                'market_id': market['MarketID']
            }
        # 情報を結合
        coin_exchange_json = dict()
        coin_exchange_json['exchange_name'] = 'coin_exchange'  # 取引所名入力
        for key in market_summaries_json.keys():
            coin_exchange_json[markets_json[key]['pair']] = market_summaries_json[key]
            coin_exchange_json[markets_json[key]['pair']]['market_id'] = markets_json[key]['market_id']
            coin_exchange_json[markets_json[key]['pair']]['coin_name'] = markets_json[key]['coin_full_name']

        return coin_exchange_json

    @staticmethod
    def get_order_book(market_id, trade_type, depth):
        """
        価格取得-----------------------
        :param: market_id <str> 通貨ID
        :param: type <str> 所得オーダー数(sell/buy)
        :param: depth <int> 所得オーダー数(n)
        :return: <list> {exchange_name, type:[{quantity, rate} * n}] }
        """
        api_options = "?" + "market_id=" + str(market_id)

        order_book = requests.get(coin_exchange_api_order_book + api_options).json()["result"]

        if trade_type == "sell":
            trade_type_key = "SellOrders"
        elif trade_type == "buy":
            trade_type_key = "BuyOrders"
        else:
            raise Exception('trade_type require <sell/buy>')

        # getしたjsonを独自フォーマットに直す
        order_book_response = list()
        depth_count = 0
        for record in order_book[trade_type_key]:
            order_book_response_record = dict()
            order_book_response_record['price'] = "%f" % float(record['Price'])
            order_book_response_record['quantity'] = "%f" % float(record['Quantity'])
            order_book_response.append(order_book_response_record)

            depth_count += 1
            if depth_count == depth:
                break

        return order_book_response

# -*- coding: utf-8 -*-

# <installed>
#  requests

import requests

# API URL
coin_exchange_api_market_summaries = "https://www.coinexchange.io/api/v1/getmarketsummaries"
coin_exchange_api_markets = "https://www.coinexchange.io/api/v1/getmarkets"

class COIN_EXCHANGE_UTILS():

    def __init(self):
        pass

    def get_market_price(self):
        '''
        価格取得-----------------------
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        '''
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
                'coin_full_name': market['MarketAssetName']
            }
        # 情報を結合
        coin_exchange_json = {}
        coin_exchange_json['exchange_name'] = 'coin_exchange' # 取引所名入力
        for key in market_summaries_json.keys():
            coin_exchange_json[markets_json[key]['pair']] = market_summaries_json[key]
            coin_exchange_json[markets_json[key]['pair']]['coin_name'] = markets_json[key]['coin_full_name']

        return coin_exchange_json
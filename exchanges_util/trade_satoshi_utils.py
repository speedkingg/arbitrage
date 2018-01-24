# -*- coding: utf-8 -*-

# <installed>
#  requests

import requests

# API URL
trade_satoshi_qpi_market_summaries = "https://tradesatoshi.com/api/public/getmarketsummaries"
trade_satoshi_qpi_get_currencies = " https://tradesatoshi.com/api/public/getcurrencies"

class TRADE_SATOHI_UTILS():

    def __init(self):
        pass

    def get_market_price(self):
        '''
        価格取得-----------------------
        :return: <json> {exchange_name, currency_pair:{last_price,volume,coin_name} * n}
        '''
        trade_satoshi_market_summaries = requests.get(trade_satoshi_qpi_market_summaries).json()["result"]
        satoshi_json = {}
        satoshi_json['exchange_name'] = 'trade_satoshi' # 取引所名入力

        # 終値、取引量取得
        for record in trade_satoshi_market_summaries:
            satoshi_json[record['market']] = {
                'price': "%f" % record['last'],
                'volume': "%f" % record['volume']
            }

        # 通貨full_name取得
        trade_satoshi_get_currencies = requests.get(trade_satoshi_qpi_get_currencies).json()["result"]
        for key in satoshi_json.keys():
            for item in trade_satoshi_get_currencies:
                if item['currency'] == key[0:len(item['currency'])]:
                    satoshi_json[key]['coin_name'] = item['currencyLong']
                    continue

        return satoshi_json
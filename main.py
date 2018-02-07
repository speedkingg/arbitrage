# -*- coding: utf-8 -*-

import json
from exchanges_util.coin_exchange_utils import CoinExchangeUtils
from exchanges_util.price_comparison import PriceComparison
from exchanges_util.trade_satoshi_utils import TradeSatoshiUtils
from exchanges_util.binance_utils import BinanceUtils

# 独自クラスインスタンス化
trade_satoshi = TradeSatoshiUtils()
coin_exchange = CoinExchangeUtils()
price_comparison = PriceComparison()
binance_utils = BinanceUtils()

# configファイル読み込み
arbitrage_parameter_file = 'config/arbitrage_parameter.json'
arbitrage_parameter = json.load(open(arbitrage_parameter_file, 'r'))
RATIO = arbitrage_parameter['output_limit_ratio']

if __name__ == '__main__':
    # 価格情報を格納するlist
    price_list = []

    # satoshi価格取得-----------------------
    satoshi_json = trade_satoshi.get_market_price()
    price_list.append(satoshi_json)

    # coin_exchange価格取得------------------
    coin_exchange_json = coin_exchange.get_market_price()
    price_list.append(coin_exchange_json)

    # binance価格取得------------------
    binance_json = binance_utils.get_market_price()
    price_list.append(binance_json)

    # 指定した倍率以上の通貨ペアと取引所を表示-----------------------------
    price_comparison.print_arbitrage_list(RATIO, price_list)

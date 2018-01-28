# -*- coding: utf-8 -*-

from exchanges_util.coin_exchange_utils import CoinExchangeUtils
from exchanges_util.price_comparison import PriceComparison
from exchanges_util.trade_satoshi_utils import TradeSatoshiUtils

# 独自クラスインスタンス化
trade_satoshi = TradeSatoshiUtils()
coin_exchange = CoinExchangeUtils()
price_comparison = PriceComparison()

if __name__ == '__main__':
    # 価格情報を格納するlist
    price_list = []

    # satoshi価格取得-----------------------
    satoshi_json = trade_satoshi.get_market_price()
    price_list.append(satoshi_json)

    # coin_exchange価格取得------------------
    coin_exchange_json = coin_exchange.get_market_price()
    price_list.append(coin_exchange_json)

    # 指定した倍率以上の通貨ペアと取引所を表示-----------------------------
    price_comparison.print_arbitrage_list(0.4, price_list)

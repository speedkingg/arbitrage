# -*- coding: utf-8 -*-

from exchanges_util.trade_satoshi_utils import TRADE_SATOHI_UTILS
from exchanges_util.coin_exchange_utils import COIN_EXCHANGE_UTILS
from exchanges_util.price_comparison import PRICE_COMPARISON

# 独自クラスインスタンス化
trade_satoshi = TRADE_SATOHI_UTILS()
coin_exchange = COIN_EXCHANGE_UTILS()
price_comparison = PRICE_COMPARISON()

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
    price_comparison.print_arbitrage_list(0.4,price_list)




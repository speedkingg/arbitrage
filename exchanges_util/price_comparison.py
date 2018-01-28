# -*- coding: utf-8 -*-

from exchanges_util.coin_exchange_utils import CoinExchangeUtils
from exchanges_util.trade_satoshi_utils import TradeSatoshiUtils

# 独自クラスインスタンス化
trade_satoshi = TradeSatoshiUtils()
coin_exchange = CoinExchangeUtils()


class PriceComparison:

    def __init__(self):
        pass

    def print_arbitrage_list(self, ratio, price_list):
        """
        指定した倍率より価格が離れているの通貨ペアを表示する
        :param:  ratio <float> 指定する倍率
        :param:  price_list <list> 各取引所の価格情報リスト
        :return: None
        """

        list_length = len(price_list)

        # 引数チェック
        if list_length < 2:
            return '[error] listの個数が不足しています(require:2以上)'

        # price_listを総当りで比較する
        for i in range(0, list_length - 1):
            for j in range(i + 1, list_length):
                self._print_arbitrage(ratio, price_list[i], price_list[j])
                j += 1
            i += 1

    def _print_arbitrage(self, ratio, first_list, second_list):
        """
        受けとった2つのリストを比較して、
        指定した倍率より価格が離れているの通貨ペアを表示する
        :param:  ratio <float> 指定する倍率
        :param:  first_list <json> 1つ目の取引所の価格情報
        :param:  second_list <json> 2つ目の取引所の価格情報
        :return: None
        """

        for key in first_list.keys():

            # 取引所名の項目をスキップ
            if key == 'exchange_name':
                continue

            # 通貨ペアが両方に存在しなければスキップ
            if key not in second_list:
                continue

            # volumeが0の場合スキップする
            if float(first_list[key]['volume']) == 0 or \
                    float(second_list[key]['volume']) == 0:
                continue

            # priceが0の場合スキップする
            if float(first_list[key]['price']) == 0 or \
                    float(second_list[key]['price']) == 0:
                continue

            # 低レートを除外する
            rate = float(first_list[key]['price']) / float(second_list[key]['price'])
            if 1 + ratio > rate > 1 - ratio:
                continue

            # 通貨名が一致しない場合、除外する??
            # print(satoshi_json[key]['coin_name'].lower())
            # print(coin_exchange_json[key]['coin_name'].lower())
            if first_list[key]['coin_name'].lower().replace(' ', '') \
                    != second_list[key]['coin_name'].lower().replace(' ', ''):
                continue

            # 取引所ごとに板を取得
            depth = 3  # 板のオーダー取得数
            if rate > 1:
                first_trade_type = "buy"
                second_trade_type = "sell"
            elif rate < 1:
                first_trade_type = "sell"
                second_trade_type = "buy"

            # <例外処理>
            # coin_exchangeはcurrency_pairでなくmarket_idがキーのため、
            # currency_pairにmarket_idを入れる
            if first_list['exchange_name'] == "coin_exchange":
                market_id = first_list[key]['market_id']
                first_order_book = self._get_order_book(market_id, first_trade_type, depth, first_list['exchange_name'])
                second_order_book = self._get_order_book(key, second_trade_type, depth, second_list['exchange_name'])

            elif second_list['exchange_name'] == "coin_exchange":
                market_id = second_list[key]['market_id']
                first_order_book = self._get_order_book(key, first_trade_type, depth, first_list['exchange_name'])
                second_order_book = self._get_order_book(market_id, second_trade_type, depth,
                                                         second_list['exchange_name'])

            else:
                first_order_book = self._get_order_book(key, first_trade_type, depth, first_list['exchange_name'])
                second_order_book = self._get_order_book(key, second_trade_type, depth, second_list['exchange_name'])

            # 結果を整理して出力
            print("【" + key + "】"
                  + first_list['exchange_name']
                  + " - "
                  + second_list['exchange_name']
                  )

            print("rate" + " : " + str(rate))

            print("price" + " : "
                  + str(first_list[key]['price'])
                  + " - "
                  + str(second_list[key]['price'])
                  )

            print("volume" + " : "
                  + str(first_list[key]['volume'])
                  + " - "
                  + str(second_list[key]['volume'])
                  )

            print("order_book [ price( quantity ) ]" + " : ")
            for i in range(0, depth):
                print("・"
                      + str(first_order_book[i]['price'])
                      + "( " + str(first_order_book[i]['quantity']) + " )"
                      + " - "
                      + str(second_order_book[i]['price'])
                      + "( " + str(second_order_book[i]['quantity']) + " )"
                      )

            print("")

    # 取引所を判定してオーダー一覧を返す
    @staticmethod
    def _get_order_book(currency_pair, trade_type, depth, exchange_name):
        if exchange_name == "trade_satoshi":
            return trade_satoshi.get_order_book(currency_pair, trade_type, depth)
        elif exchange_name == "coin_exchange":
            return coin_exchange.get_order_book(currency_pair, trade_type, depth)

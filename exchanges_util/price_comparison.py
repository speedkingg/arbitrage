# -*- coding: utf-8 -*-


class PRICE_COMPARISON():

    def __init(self):
        pass

    def print_arbitrage_list(self, ratio, price_list):
        '''
        指定した倍率より価格が離れているの通貨ペアを表示する
        :param:  ratio <float> 指定する倍率
        :param:  price_list <list> 各取引所の価格情報リスト
        :return: None
        '''

        list_length = len(price_list)

        # 引数チェック
        if list_length < 2:
            return '[error] listの個数が不足しています(require:2以上)'

        # price_listを総当りで比較する
        for i in range(0,list_length-1):
            for j in range(i+1,list_length):
                self._print_arbitrage(ratio, price_list[i],price_list[j])
                j += 1
            i += 1

    def _print_arbitrage(self, ratio, first_list, second_list):
        '''
        受けとった2つのリストを比較して、
        指定した倍率より価格が離れているの通貨ペアを表示する
        :param:  ratio <float> 指定する倍率
        :param:  first_list <json> 1つ目の取引所の価格情報
        :param:  second_list <json> 2つ目の取引所の価格情報
        :return: None
        '''

        for key in first_list.keys():

            # 取引所名の項目をスキップ
            if key == 'exchange_name':
                continue

            # 通貨ペアが両方に存在しなければスキップ
            if not key in second_list:
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
            if rate < 1 + ratio and rate > 1 - ratio:
                continue

            # 通貨名が一致しない場合、除外する??
            # print(satoshi_json[key]['coin_name'].lower())
            # print(coin_exchange_json[key]['coin_name'].lower())
            if first_list[key]['coin_name'].lower().replace(' ', '') \
                    != second_list[key]['coin_name'].lower().replace(' ', ''):
                continue

            # 結果を整理して出力
            print("【" + key + "】" + first_list['exchange_name'] + " - " + second_list['exchange_name'] )
            print("price" + " : "
                  + str(first_list[key]['price']) + " - "
                  + str(second_list[key]['price'])
                  )

            print("volume" + " : "
                  + str(first_list[key]['volume'])
                  + " - "
                  + str(second_list[key]['volume'])
                  )

            print("rate" + " : " + str(rate))

            print("")
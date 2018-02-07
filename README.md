# arbitrage

## 概要
各取引所の価格を比較し、一定のレート以上のペアを表示する

## 対応取引所
- trade satoshi
- coin exchange
- Binance

### 出力フォーマット
>【通貨ペア】取引所A - 取引所B  
>rate : 倍率  
>price : 価格A - 価格B  
>volume : 取引量A - 取引量B  
>order_book [ price( quantity ) ] :  
>・板価格A( 板取引量A ) - 板価格B( 板取引量B )  
>・板価格A( 板取引量A ) - 板価格B( 板取引量B )  
>・板価格A( 板取引量A ) - 板価格B( 板取引量B )  

### 設定ファイル
config/arbitrage_parameter.json
```
{
  "output_limit_ratio" : 0.4, #最低倍率：指定した値(ex: 0.4の場合4割以上価格が離れたペアのみを表示する)
  "show_order_book_number": 4, #板のオーダー取得数
  "minimum_volume": 0.001 #取得する最低取引量
}
```

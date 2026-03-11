def calculate_arbitrage_profit(
    buy_price,
    sell_price,
    withdraw_fee_coin,
    trade_amount_usdt,
    trade_fee=0.001
):
    # покупка монеты
    coin_amount = trade_amount_usdt / buy_price
    coin_amount = coin_amount * (1 - trade_fee)
    coin_amount = coin_amount - withdraw_fee_coin

    if coin_amount <= 0:
        return -999

    # продажа монеты
    usdt_after_sell = coin_amount * sell_price
    usdt_after_sell = usdt_after_sell * (1 - trade_fee)

    profit = usdt_after_sell - trade_amount_usdt
    return round(profit,2)
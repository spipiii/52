def find_arbitrage(tickers, min_spread):

    opportunities = []

    exchanges = list(tickers.keys())

    for i in range(len(exchanges)):
        for j in range(len(exchanges)):

            if i == j:
                continue

            ex1 = exchanges[i]
            ex2 = exchanges[j]

            for symbol, ticker1 in tickers[ex1].items():

                if "/USDT" not in symbol:
                    continue

                if symbol not in tickers[ex2]:
                    continue

                ticker2 = tickers[ex2][symbol]

                ask = ticker1["ask"]
                bid = ticker2["bid"]

                if not ask or not bid:
                    continue

                spread = (bid - ask) / ask * 100

                if spread >= min_spread:

                    opportunities.append({
                        "symbol": symbol,
                        "buy_exchange": ex1,
                        "sell_exchange": ex2,
                        "buy_price": ask,
                        "sell_price": bid,
                        "spread": round(spread, 2)
                    })

    opportunities.sort(key=lambda x: x["spread"], reverse=True)

    return opportunities[:10]

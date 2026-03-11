import asyncio
from exchanges import load_exchange
from arbitrage import calculate_arbitrage_profit
from utils import get_transfer_info

TRADE_FEE = 0.001

async def scan(settings):
    exchanges = {}
    for name in settings["exchanges"]:
        exchanges[name] = await load_exchange(name)

    tickers = {}
    for name, ex in exchanges.items():
        try:
            tickers[name] = await ex.fetch_tickers()
        except:
            tickers[name] = {}

    results = []

    for ex1 in exchanges:
        for ex2 in exchanges:
            if ex1 == ex2:
                continue

            for symbol in tickers[ex1]:
                if symbol not in tickers[ex2]:
                    continue

                ask = tickers[ex1][symbol].get("ask")
                bid = tickers[ex2][symbol].get("bid")
                if not ask or not bid: continue

                spread = (bid - ask) / ask * 100
                if spread < settings["min_spread"]: continue

                coin = symbol.split("/")[0]

                nets1 = await get_transfer_info(exchanges[ex1], coin)
                nets2 = await get_transfer_info(exchanges[ex2], coin)
                if not nets1 or not nets2: continue

                networks = set(n["network"] for n in nets1) & set(n["network"] for n in nets2)
                if not networks: continue
                network = list(networks)[0]

                fee = next(n["fee"] for n in nets1 if n["network"] == network)

                profit = calculate_arbitrage_profit(
                    ask,
                    bid,
                    fee,
                    settings["trade_amount_usdt"]
                )
                if profit <= 0: continue

                results.append({
                    "symbol": symbol,
                    "buy": ex1,
                    "sell": ex2,
                    "spread": round(spread,2),
                    "profit": round(profit,2),
                    "network": network
                })

    results = sorted(results, key=lambda x: x["profit"], reverse=True)
    return results[:5]
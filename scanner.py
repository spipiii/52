from exchanges import create_exchanges
from arbitrage import find_arbitrage
from utils import load_settings


async def scan():

    settings = load_settings()

    exchanges = await create_exchanges(settings["exchanges"])

    tickers = {}

    for name, exchange in exchanges.items():

        try:
            data = await exchange.fetch_tickers()
            tickers[name] = data
        except:
            tickers[name] = {}

    opportunities = find_arbitrage(
        tickers,
        settings["min_spread"]
    )

    for exchange in exchanges.values():
        try:
            await exchange.close()
        except:
            pass

    return opportunities

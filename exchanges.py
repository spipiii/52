import ccxt.async_support as ccxt

SUPPORTED_EXCHANGES = {
    "binance": ccxt.binance,
    "bybit": ccxt.bybit,
    "okx": ccxt.okx,
    "kucoin": ccxt.kucoin,
    "mexc": ccxt.mexc,
    "gate": ccxt.gate,
    "bitget": ccxt.bitget,
    "bingx": ccxt.bingx
}


async def create_exchanges(exchange_names):

    exchanges = {}

    for name in exchange_names:
        if name in SUPPORTED_EXCHANGES:
            exchanges[name] = SUPPORTED_EXCHANGES[name]()

    return exchanges

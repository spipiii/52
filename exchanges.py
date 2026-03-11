import ccxt.async_support as ccxt

EXCHANGE_CLASSES = {
    "binance": ccxt.binance,
    "bybit": ccxt.bybit,
    "okx": ccxt.okx,
    "kucoin": ccxt.kucoin,
    "mexc": ccxt.mexc,
    "gate": ccxt.gate
}

async def load_exchange(name):
    exchange = EXCHANGE_CLASSES[name]({
        "enableRateLimit": True,
        "timeout": 30000
    })
    await exchange.load_markets()
    return exchange
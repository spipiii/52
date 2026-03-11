network_cache = {}


async def get_networks(exchange):

    if exchange.id in network_cache:
        return network_cache[exchange.id]

    try:
        currencies = await exchange.fetch_currencies()
        network_cache[exchange.id] = currencies
        return currencies
    except:
        return {}

async def get_transfer_info(exchange, coin):
    try:
        currencies = await exchange.fetch_currencies()
    except:
        return None

    if coin not in currencies:
        return None

    data = currencies[coin]
    networks = []

    if "networks" in data:
        for n in data["networks"]:
            net = data["networks"][n]
            if net.get("withdraw") and net.get("deposit"):
                networks.append({
                    "network": n,
                    "fee": net.get("fee",0)
                })
    return networks
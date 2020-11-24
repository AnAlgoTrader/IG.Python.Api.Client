class OpenMarketPositionRequest:
    epic = None
    direction = None
    size = None
    expiry = 'DFB'
    orderType = 'MARKET'
    guaranteedStop = False,
    trailingStop = False,
    forceOpen = True,
    currencyCode = 'GBP'

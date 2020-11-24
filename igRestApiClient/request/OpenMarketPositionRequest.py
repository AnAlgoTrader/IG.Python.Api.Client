from igRestApiClient.model.enum.Currency import Currency
from igRestApiClient.model.enum.Expiry import Expiry
from igRestApiClient.model.enum.OrderType import OrderType


class OpenMarketPositionRequest:
    epic = None
    direction = None
    size = None
    expiry = Expiry.DFB
    orderType = OrderType.Market
    guaranteedStop = False,
    trailingStop = False,
    forceOpen = True,
    currencyCode = Currency.GBP

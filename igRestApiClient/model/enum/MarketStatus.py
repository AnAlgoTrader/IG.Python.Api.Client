from enum import Enum


class MarketStatus(str, Enum):
    EDITS_ONLY = 'EDITS_ONLY',
    TRADEABLE = 'TRADEABLE'

from enum import Enum


class MarketStatus(Enum, str):
    EDITS_ONLY = 'EDITS_ONLY',
    TRADEABLE = 'TRADEABLE'

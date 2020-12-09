from enum import Enum


class TransactionType(str, Enum):
    DEAL = 'DEAL'
    WITH = 'WITH'
    DEPO = 'DEPO'

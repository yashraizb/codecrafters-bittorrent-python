from enum import Enum
from app.strategy.decode.IntegerStrategy import IntegerStrategy
from app.strategy.decode.StringStrategy import StringStrategy


class DecodeType(Enum):
    PARSE_INTEGER = ("i", IntegerStrategy)
    PARSE_STRING = (True, StringStrategy) # True indicates any string starting with a digit
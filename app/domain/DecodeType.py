from enum import Enum
from app.strategy.decode.IntegerStrategy import IntegerStrategy
from app.strategy.decode.StringStrategy import StringStrategy
from app.strategy.decode.ListStrategy import ListStrategy
from app.strategy.decode.DictStrategy import DictStrategy


class DecodeType(Enum):
    PARSE_INTEGER = ("i", IntegerStrategy)
    PARSE_STRING = (True, StringStrategy) # True indicates any string starting with a digit
    PARSE_LIST = ("l", ListStrategy)
    PARSE_DICT = ("d", DictStrategy)
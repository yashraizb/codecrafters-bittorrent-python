from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
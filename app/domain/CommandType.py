from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand
from app.strategy.command.PeersCommand import PeersCommand


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
    PEERS = ("peers", PeersCommand)
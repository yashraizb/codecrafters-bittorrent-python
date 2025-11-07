from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand
from app.strategy.command.PeersCommand import PeersCommand
from app.strategy.command.HandshakeCommand import HandshakeCommand


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
    PEERS = ("peers", PeersCommand)
    HANDSHAKE = ("handshake", HandshakeCommand)
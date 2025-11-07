from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand
from app.strategy.command.PeersCommand import PeersCommand
from app.strategy.command.HandshakeCommand import HandshakeCommand
from app.strategy.command.DownloadPiece import DownloadPiece


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
    PEERS = ("peers", PeersCommand)
    HANDSHAKE = ("handshake", HandshakeCommand)
    DOWNLOAD = ("download_piece", DownloadPiece)
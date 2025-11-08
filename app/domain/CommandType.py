from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand
from app.strategy.command.PeersCommand import PeersCommand
from app.strategy.command.HandshakeCommand import HandshakeCommand
from app.strategy.command.DownloadPieceCmd import DownloadPieceCmd
from app.strategy.command.FileDownloadCmd import FileDownloadCmd


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
    PEERS = ("peers", PeersCommand)
    HANDSHAKE = ("handshake", HandshakeCommand)
    PIECE_DOWNLOAD = ("download_piece", DownloadPieceCmd)
    FILE_DOWNLOAD = ("download", FileDownloadCmd)
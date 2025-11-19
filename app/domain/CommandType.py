from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand
from app.strategy.command.PeersCommand import PeersCommand
from app.strategy.command.HandshakeCommand import HandshakeCommand
from app.strategy.command.DownloadPieceCmd import DownloadPieceCmd
from app.strategy.command.FileDownloadCmd import FileDownloadCmd
from app.strategy.command.MagnetParse import MagnetParse
from app.strategy.command.MagnetHandshake import MagnetHandshake


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
    PEERS = ("peers", PeersCommand)
    HANDSHAKE = ("handshake", HandshakeCommand)
    PIECE_DOWNLOAD = ("download_piece", DownloadPieceCmd)
    FILE_DOWNLOAD = ("download", FileDownloadCmd)
    MAGNET_PARSE = ("magnet_parse", MagnetParse)
    MAGNET_HANDSHAKE = ("magnet_handshake", MagnetHandshake)
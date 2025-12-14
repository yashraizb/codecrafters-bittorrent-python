from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand
from app.strategy.command.InfoCommand import InfoCommand
from app.strategy.command.PeersCommand import PeersCommand
from app.strategy.command.HandshakeCommand import HandshakeCommand
from app.strategy.command.DownloadPieceCmd import DownloadPieceCmd
from app.strategy.command.FileDownloadCmd import FileDownloadCmd
from app.strategy.command.MagnetParse import MagnetParse
from app.strategy.command.MagnetHandshake import MagnetHandshake
from app.strategy.command.MagnetInfo import MagnetInfo
from app.strategy.command.MgntDownloadPiece import MgntDownloadPiece
from app.strategy.command.MgntDownloadFile import MgntDownloadFile


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
    INFO = ("info", InfoCommand)
    PEERS = ("peers", PeersCommand)
    HANDSHAKE = ("handshake", HandshakeCommand)
    PIECE_DOWNLOAD = ("download_piece", DownloadPieceCmd)
    FILE_DOWNLOAD = ("download", FileDownloadCmd)
    MAGNET_PARSE = ("magnet_parse", MagnetParse)
    MAGNET_HANDSHAKE = ("magnet_handshake", MagnetHandshake)
    MAGNET_INFO = ("magnet_info", MagnetInfo)
    MAGNT_PIECE_DOWNLOAD = ("magnet_download_piece", MgntDownloadPiece)
    MAGNT_FILE_DOWNLOAD = ("magnet_download", MgntDownloadFile)
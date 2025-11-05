import bencodepy
from app.strategy.command.CommandStrategy import CommandStrategy
from app.strategy.command.DecodeCommand import DecodeCommand
from app.domain.TorrentInfo import TorrentInfo


class InfoCommand(CommandStrategy):

    def __init__(self):
        self.decodeCommand = DecodeCommand()

    def execute(self, data: list):
        decoded_data = bencodepy.Bencode().read(data[0])
        torrentInfo = TorrentInfo(decoded_data)
        torrentInfo.printInfo()
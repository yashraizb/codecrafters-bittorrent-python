import bencodepy
from app.strategy.command.CommandStrategy import CommandStrategy
from app.domain.TorrentInfo import TorrentInfo


class InfoCommand(CommandStrategy):

    def execute(self, data: list):
        decoded_data = bencodepy.Bencode().read(data[0])
        torrentInfo = TorrentInfo(decoded_data)
        torrentInfo.printInfo()
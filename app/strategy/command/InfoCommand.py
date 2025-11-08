from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.domain.TorrentInfo import TorrentInfo
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent


class InfoCommand(CommandStrategy):

    def execute(self, data: list):
        torrentInfo: TorrentInfo = TorrentConnBuilder().\
            operation(ReadTorrent(data)).\
            build()
        torrentInfo.printInfo()
        
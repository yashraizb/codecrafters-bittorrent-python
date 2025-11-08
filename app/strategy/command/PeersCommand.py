from app.domain.TorrentInfo import TorrentInfo
from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent
from app.strategy.torrentBuilder.FetchPeers import FetchPeers


class PeersCommand(CommandStrategy):

    def execute(self, data: list):
        torrentInfo: TorrentInfo = TorrentConnBuilder().\
            operation(ReadTorrent(data)).\
            operation(FetchPeers()).\
            build()
        torrentInfo.printPeers()
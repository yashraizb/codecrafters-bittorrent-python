from app.strategy.command.CommandStrategy import CommandStrategy
from app.domain.TorrentInfo import TorrentInfo
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent
from app.strategy.torrentBuilder.Handshake import Handshake


class HandshakeCommand(CommandStrategy):
    def execute(self, data: list):

        torrentInfo: TorrentInfo = TorrentConnBuilder().\
            operation(ReadTorrent(data)).\
            operation(Handshake(data, 0)).\
            build()
        
        torrentInfo.printHandshakePeerId()

        torrentInfo.verifiedConnections[0][2].close()  # Close the connection after handshake
        
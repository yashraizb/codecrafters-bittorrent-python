from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent
from app.strategy.torrentBuilder.Handshake import Handshake
from app.strategy.torrentBuilder.FetchPeers import FetchPeers
from app.strategy.torrentBuilder.Piece import Piece


class DownloadPieceCmd(CommandStrategy):

    def execute(self, data: list):
        # Fetch peers from the torrent file
        fetchPeers: TorrentConnBuilder = (
            TorrentConnBuilder()
            .operation(ReadTorrent(data[2:3]))
            .operation(FetchPeers())
        )
        
        # Perform handshake with the first peer
        handShake: TorrentConnBuilder = fetchPeers.operation(
            Handshake([0, f"{fetchPeers.peers[0][0]}:{fetchPeers.peers[0][1]}"], 0)
        )
        pieceIndex = int(data[3])

        # Download the piece
        pieceDownload = handShake.operation(
            Piece(pieceIndex, 0)
        ).build()

        # Close the connection after downloading the piece
        pieceDownload.verifiedConnections[0][2].close()
        
        # Write the piece to the file
        with open(data[1], "wb") as file:
                file.write(pieceDownload.parts[pieceIndex])

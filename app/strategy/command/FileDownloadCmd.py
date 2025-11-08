from queue import Queue
from threading import Thread
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent
from app.strategy.torrentBuilder.FetchPeers import FetchPeers
from app.strategy.torrentBuilder.Handshake import Handshake
from app.strategy.torrentBuilder.Piece import Piece
from app.strategy.command.CommandStrategy import CommandStrategy
from app.domain.TorrentInfo import TorrentInfo


class FileDownloadCmd(CommandStrategy):

    def __init__(self):
        self.freeConnections = Queue()

    def pieceDownloader(
        self,
        builder: TorrentConnBuilder,
        pieceIndex: int,
        connectionIndex: int
    ):
        # Download the piece
        builder.operation(Piece(pieceIndex, connectionIndex, self.freeConnections))

    def execute(self, data: list):
        # Fetch peers from the torrent file
        fetchPeers: TorrentConnBuilder = (
            TorrentConnBuilder()
            .operation(ReadTorrent(data[2:3]))
            .operation(FetchPeers())
        )

        for peer in range(len(fetchPeers.peers)):
            # Perform handshake with the peers
            fetchPeers: TorrentConnBuilder = fetchPeers.operation(
                Handshake(
                    [0, f"{fetchPeers.peers[peer][0]}:{fetchPeers.peers[peer][1]}"]
                )
            )
            self.freeConnections.put(peer)

        for pieceIndex in range(fetchPeers.numberOfPieces):

            while self.freeConnections.empty():
                pass  # Wait for a free connection

            connIndex = self.freeConnections.get()
            self.freeConnections.task_done()
            thread = Thread(
                target=self.pieceDownloader,
                args=(fetchPeers, pieceIndex, connIndex),
            )
            thread.start()
        
        while self.freeConnections.qsize() < 3:
            pass  # Wait for all connections to be free

        # Write the pieces to the file

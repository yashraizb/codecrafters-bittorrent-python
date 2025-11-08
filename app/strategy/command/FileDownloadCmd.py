from queue import Queue
from threading import Thread
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent
from app.strategy.torrentBuilder.FetchPeers import FetchPeers
from app.strategy.torrentBuilder.Handshake import Handshake
from app.strategy.torrentBuilder.Piece import Piece
from app.strategy.command.CommandStrategy import CommandStrategy


class FileDownloadCmd(CommandStrategy):

    def __init__(self):
        self.freeConnections = Queue()

    def pieceDownloader(
        self, builder: TorrentConnBuilder, pieceIndex: int, connectionIndex: int
    ):
        handshake: TorrentConnBuilder = builder.operation(
            Handshake(
                [
                    None,
                    f"{builder.peers[connectionIndex][0]}:{builder.peers[connectionIndex][1]}",
                ],
                connectionIndex,
            )
        )
        # Download the piece
        handshake.operation(Piece(pieceIndex, connectionIndex))
        builder.verifiedConnections[connectionIndex][2].close()
        self.freeConnections.put(connectionIndex)

    def execute(self, data: list):
        # Fetch peers from the torrent file
        fetchPeers: TorrentConnBuilder = (
            TorrentConnBuilder()
            .operation(ReadTorrent(data[2:3]))
            .operation(FetchPeers())
        )

        for peer in range(len(fetchPeers.peers)):
            self.freeConnections.put(peer)

        print("Number of pieces to download:", fetchPeers.numberOfPieces)

        for pieceIndex in range(fetchPeers.numberOfPieces):

            connIndex = self.freeConnections.get()
            self.freeConnections.task_done()
            thread = Thread(
                target=self.pieceDownloader,
                args=(fetchPeers, pieceIndex, connIndex),
            )
            thread.start()
        
        while self.freeConnections.qsize() < 3:
            pass  # Wait for all connections to be free

        final = fetchPeers.build()

        # Write the pieces to the file
        with open(data[1], "wb") as file:
            for piece in final.parts:
                file.write(piece)

        print(f"Downloaded file to {data[1]}")

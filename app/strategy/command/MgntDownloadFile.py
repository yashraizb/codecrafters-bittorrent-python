from queue import Queue
from threading import Thread

from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.MagnetBuilder import MagnetBuilder
from app.domain.Magnet import Magnet

from app.strategy.magnetBuilder.ExtractInfo import ExtractInfo
from app.strategy.magnetBuilder.GetPeers import GetPeers
from app.strategy.magnetBuilder.MgntHandshake import MgntHandshake
from app.strategy.magnetBuilder.RequestMetadata import RequestMetadata
from app.strategy.torrentBuilder.Handshake import Handshake
from app.strategy.torrentBuilder.Piece import Piece


class MgntDownloadFile(CommandStrategy):

    def __init__(self):
        self.freeConnections = Queue()

    def pieceDownloader(self, builder: MagnetBuilder, pieceIndex: int, connIndex: int):
        """
        Thread target:
        - Handshake with peer
        - Request metadata
        - Download piece
        - Close connection
        - Mark this connection as free again
        """

        handshakeBuilder = (
            builder
            .operation(
                Handshake(
                    [connIndex, f"{builder.peers[connIndex][0]}:{builder.peers[connIndex][1]}"],
                    connIndex
                )
            )
        )

        # STEP 3: Download piece
        pieceBuilder = handshakeBuilder.operation(Piece(pieceIndex, connIndex))

        # Final constructed output
        built = pieceBuilder

        # Close the connection
        built.verifiedConnections[connIndex][2].close()

        # Return this connection index back to free pool
        self.freeConnections.put(connIndex)

    def execute(self, data: list):
        """
        Main execution flow:
        - Extract magnet info
        - Get peers
        - Initialize connection slots
        - Spawn threads for each piece
        - Wait for all pieces
        - Write final file
        """

        magnetInfo: MagnetBuilder = (
            MagnetBuilder()
            .operation(ExtractInfo(data[2:3]))
            .operation(GetPeers(data))
            .operation(MgntHandshake(0))
            .operation(RequestMetadata(0))
        )

        magnetInfo.verifiedConnections[0][2].close()  # Close the connection after metadata request

        num_peers = len(magnetInfo.peers)
        num_pieces = magnetInfo.numberOfPieces

        # Fill free queue with peer indexes
        for peerIndex in range(num_peers):
            self.freeConnections.put(peerIndex)

        print(f"Magnet: {num_pieces} pieces, {num_peers} peers")

        for pieceIndex in range(num_pieces):

            # Get a free connection slot
            connIndex = self.freeConnections.get()
            self.freeConnections.task_done()

            # Start thread for this piece
            t = Thread(
                target=self.pieceDownloader,
                args=(magnetInfo, pieceIndex, connIndex)
            )
            t.start()

        while self.freeConnections.qsize() < num_peers:
            pass  # Wait for all connections to be free

        final: Magnet = magnetInfo.build()

        # Write final file
        with open(data[1], "wb") as file:
            for piece in final.parts:
                file.write(piece)

        print(f"Downloaded magnet file → {data[1]}")

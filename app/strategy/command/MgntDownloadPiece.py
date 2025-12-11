from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.MagnetBuilder import MagnetBuilder
from app.domain.Magnet import Magnet
from app.strategy.magnetBuilder.ExtractInfo import ExtractInfo
from app.strategy.magnetBuilder.GetPeers import GetPeers
from app.strategy.magnetBuilder.MgntHandshake import MgntHandshake
from app.strategy.magnetBuilder.RequestMetadata import RequestMetadata
from app.strategy.torrentBuilder.Piece import Piece
from app.strategy.torrentBuilder.Handshake import Handshake


class MgntDownloadPiece(CommandStrategy):
    def execute(self, data: list):
        pieceIndex = int(data[3])
        magnetInfo: MagnetBuilder = (
            MagnetBuilder()
            .operation(ExtractInfo(data[2:3]))
            .operation(GetPeers(data))
            .operation(MgntHandshake(0))
            .operation(RequestMetadata(0))
        )

        magnetInfo.verifiedConnections[0][2].close()  # Close the connection after metadata request

        print("Requested data received. Proceeding to download piece index", pieceIndex)

        handShake = (magnetInfo
        .operation(
            Handshake([0, f"{magnetInfo.peers[0][0]}:{magnetInfo.peers[0][1]}"], 0)
        )
        .operation(Piece(pieceIndex, 0))
        .build())

        handShake.verifiedConnections[0][2].close()  # Close the connection after downloading the piece
        # print(handShake.parts)

        with open(data[1], "wb") as file:
            file.write(handShake.parts[pieceIndex])
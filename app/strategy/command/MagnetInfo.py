from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.MagnetBuilder import MagnetBuilder
from app.domain.Magnet import Magnet
from app.strategy.magnetBuilder.ExtractInfo import ExtractInfo
from app.strategy.magnetBuilder.GetPeers import GetPeers
from app.strategy.magnetBuilder.MgntHandshake import MgntHandshake
from app.strategy.magnetBuilder.RequestMetadata import RequestMetadata


class MagnetInfo(CommandStrategy):
    def execute(self, data: list):
        magnetInfo: Magnet = (
            MagnetBuilder()
            .operation(ExtractInfo(data))
            .operation(GetPeers(data))
            .operation(MgntHandshake())
            .operation(RequestMetadata())
            .build()
        )

        magnetInfo.sock.close()
        print("Tracker URL:", magnetInfo.trackerURL)
        print("Length:", magnetInfo.length)
        print("Info Hash:", magnetInfo.infoHash)
        print("Piece Length:", magnetInfo.pieceLength)  # Example calculation
        print("Pieces:")
        for piece in magnetInfo.pieces:
            print(piece)

from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.MagnetBuilder import MagnetBuilder
from app.domain.Magnet import Magnet
from app.strategy.magnetBuilder.ExtractInfo import ExtractInfo
from app.strategy.magnetBuilder.GetPeers import GetPeers
from app.strategy.magnetBuilder.MgntHandshake import MgntHandshake


class MagnetHandshake(CommandStrategy):
    def execute(self, data: list):
        magnetInfo: Magnet = MagnetBuilder().operation(
            ExtractInfo(data)
        ).operation(
            GetPeers(data)
        ).\
        operation(MgntHandshake(0)).build()

        magnetInfo.sock.close()  # Close the socket after handshake

        print("Peer ID:", magnetInfo.handshakePeerId)
        print("Peer Metadata Extension ID:", magnetInfo.metadataExtensionId)
        
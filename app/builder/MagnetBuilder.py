from app.domain.Magnet import Magnet
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy


class MagnetBuilder:
    def __init__(self):
        self.infoHash = None
        self.name = None
        self.trackerURL = None
        self.peerId = "-PC0001-123456789012"
        self.queryString = None
        self.peers = []
        self.handshakePeerId = None
        self.metadataExtensionId = None
        self.sock = None

    def operation(self, operationStrategy: OperationStrategy):
        operationStrategy.execute(self)
        return self

    def build(self):
        return Magnet(
            self.infoHash,
            self.name,
            self.trackerURL,
            self.peerId,
            self.queryString,
            self.peers,
            self.handshakePeerId,
            self.metadataExtensionId,
            self.sock
        )

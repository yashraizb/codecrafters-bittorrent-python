import hashlib
import bencodepy
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy


class ReadTorrent(OperationStrategy):

    def __init__(self, data: list):
        self.data = data

    def execute(self, builder):
        builder.info = bencodepy.Bencode().read(self.data[0])
        builder.trackerURL = builder.info.get(b"announce").decode()
        builder.length = builder.info.get(b"info").get(b"length")
        builder.infoHash = hashlib.sha1(
            bencodepy.encode(builder.info.get(b"info"))
        ).hexdigest()
        builder.pieceLength = builder.info.get(b"info").get(b"piece length")
        builder.pieces = builder.info.get(b"info").get(b"pieces").hex()
        builder.infoHash20Bytes = hashlib.sha1(
            bencodepy.encode(builder.info.get(b"info"))
        ).digest()
        builder.numberOfPieces = len(builder.info.get(b"info").get(b"pieces")) // 20
        builder.parts = [i for i in range(builder.numberOfPieces)]
        # builder.peerId = "APC0001B123456789012"  # Example peer ID
        return builder

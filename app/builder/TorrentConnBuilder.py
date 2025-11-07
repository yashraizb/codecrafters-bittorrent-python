import bencodepy
import hashlib
import requests
from urllib.parse import urlencode
from app.domain.TorrentInfo import TorrentInfo
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy


class TorrentConnBuilder:
    
    def __init__(self):
        self.info = None
        self.trackerURL = None
        self.length = None
        self.infoHash = None
        self.pieceLength = None
        self.pieces = None
        self.peerId = "APC0001B123456789012"  # Example peer ID
        self.peers = []
        self.queryString = None
        self.handshakePeerId = None
    
    def operation(self, operationStrategy: OperationStrategy):
        operationStrategy.execute(self)
        return self

    def build(self):
        return TorrentInfo(
            self.info, 
            self.trackerURL, 
            self.length, 
            self.infoHash, 
            self.pieceLength, 
            self.pieces, 
            self.peerId, 
            self.queryString, 
            self.peers, 
            self.handshakePeerId
        )
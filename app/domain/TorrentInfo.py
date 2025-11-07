import hashlib
import bencodepy
from urllib.parse import urlencode


class TorrentInfo:
    def __init__(self, info, trackerURL, length, infoHash, pieceLength, pieces, peerId, queryString, peers, handshakePeerId):
        self.info:dict = info
        self.trackerURL = trackerURL
        self.length = length
        self.infoHash = infoHash
        self.pieceLength = pieceLength
        self.pieces = pieces
        self.peerId = peerId
        self.queryString = queryString
        self.peers = peers
        self.handshakePeerId = handshakePeerId
    
    def getTrackerURL(self):
        return self.trackerURL
    
    def printPeers(self):
        for ip, port in self.peers:
            print(f"{ip}:{port}")
    
    def printInfo(self):
        print("Tracker URL:", self.trackerURL)
        print("Length:", self.length)
        print("Info Hash:", self.infoHash)
        print("Piece Length:", self.pieceLength)
        print("Pieces: ")
        for i in range(0, len(self.pieces), 40):
            piece_hash = self.pieces[i: i + 40]
            print(f"{piece_hash}")
    
    def printHandshakePeerId(self):
        print("Handshake Peer ID:", self.handshakePeerId)
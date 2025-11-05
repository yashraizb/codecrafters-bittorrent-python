import hashlib
import bencodepy
import math


class TorrentInfo:
    def __init__(self, info):
        self.trackerURL = info.get(b'announce').decode()
        self.length = info.get(b'info').get(b'length')
        self.infoHash = hashlib.sha1(bencodepy.encode(info.get(b'info'))).hexdigest()
        self.pieceLength = info.get(b'info').get(b'piece length')
        self.pieces = info.get(b'info').get(b'pieces').hex()
    
    def printInfo(self):
        print("Tracker URL:", self.trackerURL)
        print("Length:", self.length)
        print("Info Hash:", self.infoHash)
        print("Piece Length:", self.pieceLength)
        print("Pieces: ")
        for i in range(0, len(self.pieces), 40):
            piece_hash = self.pieces[i: i + 40]
            print(f"{piece_hash}")
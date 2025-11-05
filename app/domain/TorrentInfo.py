import hashlib
import bencodepy
from urllib.parse import urlencode


class TorrentInfo:
    def __init__(self, info):
        self.info:dict = info
        self.trackerURL = info.get(b'announce').decode()
        self.length = info.get(b'info').get(b'length')
        self.infoHash = hashlib.sha1(bencodepy.encode(info.get(b'info'))).hexdigest()
        self.pieceLength = info.get(b'info').get(b'piece length')
        self.pieces = info.get(b'info').get(b'pieces').hex()
    
    def getTrackerURL(self):
        return self.trackerURL
    
    def getQueryString(self):
        query = {
            "info_hash": hashlib.sha1(bencodepy.encode(self.info.get(b'info'))).digest(),
            "peer_id": "APC0001B123456789012",
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": self.length,
            "compact": 1
        }
        self.queryString = urlencode(query)
        return self.queryString
    
    def printInfo(self):
        print("Tracker URL:", self.trackerURL)
        print("Length:", self.length)
        print("Info Hash:", self.infoHash)
        print("Piece Length:", self.pieceLength)
        print("Pieces: ")
        for i in range(0, len(self.pieces), 40):
            piece_hash = self.pieces[i: i + 40]
            print(f"{piece_hash}")
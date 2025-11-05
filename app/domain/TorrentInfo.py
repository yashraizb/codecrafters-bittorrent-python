import hashlib
import bencodepy


class TorrentInfo:
    def __init__(self, info):
        self.trackerURL = info.get(b'announce').decode()
        self.length = info.get(b'info').get(b'length')
        self.infoHash = hashlib.sha1(bencodepy.encode(info.get(b'info'))).hexdigest()
    
    def printInfo(self):
        print("Tracker URL:", self.trackerURL)
        print("Length:", self.length)
        print("Info Hash:", self.infoHash)
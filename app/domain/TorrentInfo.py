class TorrentInfo:
    def __init__(self, info):
        self.trackerURL = info.get(b'announce').decode()
        self.length = info.get(b'info').get(b'length')
    
    def printInfo(self):
        print("Tracker URL:", self.trackerURL)
        print("Length:", self.length)
class Magnet:

    def __init__(
        self,
        infoHash: str,
        name: str,
        trackerURL: str,
        peerId: str,
        queryString: dict,
        peers: list,
        handshakePeerId: str
    ):
        self.infoHash = infoHash
        self.name = name
        self.trackerURL = trackerURL
        self.peerId = peerId
        self.queryString = queryString
        self.peers = peers
        self.handshakePeerId = handshakePeerId

    def printParsedData(self):
        print("Tracker URL:", self.trackerURL)
        print("Info Hash:", self.infoHash)

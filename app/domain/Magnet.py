class Magnet:

    def __init__(
        self,
        infoHash: str,
        name: str,
        trackerURL: str,
        peerId: str,
        queryString: dict,
        peers: list,
        handshakePeerId: str,
        metadataExtensionId: str
    ):
        self.infoHash = infoHash
        self.name = name
        self.trackerURL = trackerURL
        self.peerId = peerId
        self.queryString = queryString
        self.peers = peers
        self.handshakePeerId = handshakePeerId
        self.metadataExtensionId = metadataExtensionId

    def printParsedData(self):
        print("Tracker URL:", self.trackerURL)
        print("Info Hash:", self.infoHash)

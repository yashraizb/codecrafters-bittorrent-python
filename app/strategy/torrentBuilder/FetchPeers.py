import hashlib
import bencodepy
import requests
from urllib.parse import urlencode
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy
from app.builder.TorrentConnBuilder import TorrentConnBuilder


class FetchPeers(OperationStrategy):

    def getQueryString(self, builder: TorrentConnBuilder):
        query = {
            "info_hash": hashlib.sha1(bencodepy.encode(builder.info.get(b'info'))).digest(),
            "peer_id": builder.peerId,
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": builder.length,
            "compact": 1
        }
        builder.queryString = urlencode(query)
        return builder.queryString

    def execute(self, builder: TorrentConnBuilder):
        response = requests.get(builder.trackerURL, params=self.getQueryString(builder))
        content = bencodepy.decode(response.content)
        peers = content[b'peers']
        
        for i in range(0, len(peers), 6):
            ip = ".".join(str(b) for b in peers[i:i+4])
            port = int.from_bytes(peers[i+4:i+6], byteorder='big')
            builder.peers.append((ip, port))
            # print(f"{ip}:{port}")
        
        return self
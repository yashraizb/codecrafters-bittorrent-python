import bencodepy
import requests
from app.domain.TorrentInfo import TorrentInfo
from app.strategy.command.CommandStrategy import CommandStrategy


class PeersCommand(CommandStrategy):

    def execute(self, data: list):
        decoded_data = bencodepy.Bencode().read(data[0])
        torrentInfo = TorrentInfo(decoded_data)

        response = requests.get(torrentInfo.getTrackerURL(), params=torrentInfo.getQueryString())
        content = bencodepy.decode(response.content)
        peers = content[b'peers']
        
        for i in range(0, len(peers), 6):
            ip = ".".join(str(b) for b in peers[i:i+4])
            port = int.from_bytes(peers[i+4:i+6], byteorder='big')
            print(f"{ip}:{port}")
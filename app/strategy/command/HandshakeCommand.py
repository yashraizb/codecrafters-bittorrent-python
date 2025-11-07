import socket
import hashlib
import bencodepy
from app.strategy.command.CommandStrategy import CommandStrategy
from app.domain.TorrentInfo import TorrentInfo


class HandshakeCommand(CommandStrategy):
    def execute(self, data: list):
        decoded_data = bencodepy.Bencode().read(data[0])
        torrentInfo = TorrentInfo(decoded_data)
        ip, port = data[1].split(':')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))
        pstr = b"BitTorrent protocol"
        reserved = b"\x00" * 8
        info_hash = hashlib.sha1(bencodepy.encode(decoded_data.get(b'info'))).digest()
        peer_id = torrentInfo.peerId.encode()
        handshake_msg = bytes([len(pstr)]) + pstr + reserved + info_hash + peer_id
        
        sock.send(handshake_msg)
        response = sock.recv(68)
        sock.close()

        print("Peer ID:", response[48:].hex())
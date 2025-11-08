import hashlib
import bencodepy
import socket
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.domain.HandshakeMessage import HandshakeMessage


class Handshake(OperationStrategy):

    def __init__(self, data: list):
        self.data = data

    def execute(self, builder: TorrentConnBuilder):
        ip, port = self.data[1].split(':')

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))
        info_hash = hashlib.sha1(bencodepy.encode(builder.info.get(b'info'))).digest()
        peer_id = builder.peerId.encode()

        handshakeMessage = HandshakeMessage(info_hash, peer_id).to_bytes()
        
        sock.send(handshakeMessage)
        response = sock.recv(68)
        builder.verifiedConnections.append((ip, int(port), sock))
        builder.handshakePeerId = response[48:].hex()

        return builder
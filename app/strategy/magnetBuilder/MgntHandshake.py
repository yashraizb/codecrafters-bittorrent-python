import socket
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy
from app.builder.MagnetBuilder import MagnetBuilder
from app.domain.HandshakeMessage import HandshakeMessage


class MgntHandshake(OperationStrategy):

    def execute(self, builder: MagnetBuilder):
        ip, port = builder.peers[0]

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))
        infoHash = bytes.fromhex(builder.infoHash)
        peerId = builder.peerId.encode()

        handshakeMessage = HandshakeMessage(infoHash, peerId)
        handshakeMessage.reserved = (
            handshakeMessage.reserved[:-3] + b"\x10" + handshakeMessage.reserved[-2:]
        )  # Setting the DHT flag
        handshakeMessageBytes = handshakeMessage.to_bytes()

        sock.send(handshakeMessageBytes)
        response = sock.recv(68)
        builder.handshakePeerId = response[48:].hex()

        # print(response)

        return builder
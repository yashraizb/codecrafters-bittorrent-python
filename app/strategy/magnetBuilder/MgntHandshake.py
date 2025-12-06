import socket
import bencodepy
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

        # If the peer supports extension protocol, send extended handshake request
        if response[20:28] == b'\x00\x00\x00\x00\x00\x10\x00\x00':
            msg_len = sock.recv(4)
            sock.recv(int.from_bytes(msg_len, byteorder="big"))

            extension_len = sock.recv(4)
            sock.recv(int.from_bytes(extension_len, byteorder="big"))

            ben_dict = {
                "m": {
                    "ut_metadata": 18
                }
            }
            
            ben_dict_bytes = bencodepy.encode(ben_dict)
            msg_id = (20).to_bytes(1, byteorder="big")
            extension_id = (0).to_bytes(1, byteorder="big")
            msg_len = (1 + 1 + len(ben_dict_bytes)).to_bytes(4, byteorder="big")
            message = msg_len + msg_id + extension_id + ben_dict_bytes
            sock.send(message)


        builder.handshakePeerId = response[48:].hex()

        # print(response)

        return builder
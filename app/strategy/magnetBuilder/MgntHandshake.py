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
        builder.handshakePeerId = response[48:].hex()

        # If the peer supports extension protocol, send extended handshake request
        if response[20:28] == b'\x00\x00\x00\x00\x00\x10\x00\x00':
            extensions = bencodepy.encode({"m": {"ut_metadata": 1}})
            message_id = (20).to_bytes(1, byteorder="big")
            extension_message_id = (0).to_bytes(1, "big")
            sent_length = (1 + 1 + len(extensions)).to_bytes(4, byteorder="big")
            sock.send(sent_length + message_id + extension_message_id + extensions)

            test = sock.recv(4)
            received_length = sock.recv(4)
            received = sock.recv(int.from_bytes(received_length, "big"))
            received = received[received.index(b'\x14'):]

            if received[0] != 20:
                raise ValueError(f"Expecting message ID of 20. Got {received[0]}")
            if received[1] != 0:
                raise ValueError(f"Expected extension message ID of 0. Got {received[1]}")

            supported_extensions = bencodepy.decode(received[2:])
            metadata_extension_id = supported_extensions[b"m"][b"ut_metadata"]

            builder.metadataExtensionId = metadata_extension_id

        return builder
import bencodepy
import socket
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy
from app.builder.MagnetBuilder import MagnetBuilder


class RequestMetadata(OperationStrategy):

    def execute(self, builder: MagnetBuilder):
        ip, port = builder.peers[0]  # Using the first peer for simplicity
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, int(port)))

        metadataDict = bencodepy.encode({
            "msg_type": 0,
            "piece": 0
        })

        message_id = (20).to_bytes(1, byteorder="big")
        extension_message_id = (builder.metadataExtensionId).to_bytes(1, "big")
        sent_length = (1 + 1 + len(metadataDict)).to_bytes(4, byteorder="big")
        builder.sock.send(sent_length + message_id + extension_message_id + metadataDict)

        return builder
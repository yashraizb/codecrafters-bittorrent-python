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

        # Receive metadata size
        length = builder.sock.recv(4)
        while not length or not int.from_bytes(length):
            length = builder.sock.recv(4)

        message = builder.sock.recv(int.from_bytes(length))
        while len(message) < int.from_bytes(length):
            message += builder.sock.recv(int.from_bytes(length) - len(message))
        
        message = bencodepy.decode(b'l' + message[2:] + b'e')

        # print(message)

        builder.length = message[1][b'length']
        builder.pieceLength = message[1][b'piece length']
        pieces = message[1][b'pieces']

        for i in range(0, len(pieces), 20):
            builder.pieces.append(pieces[i:i+20].hex())

        return builder
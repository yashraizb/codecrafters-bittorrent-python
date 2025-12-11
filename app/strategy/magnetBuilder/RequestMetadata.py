import bencodepy
import socket
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy
from app.builder.MagnetBuilder import MagnetBuilder


class RequestMetadata(OperationStrategy):
    def __init__(self, connectionIndex: int):
        self.connectionIndex = connectionIndex

    def execute(self, builder: MagnetBuilder):
        sock = builder.verifiedConnections[self.connectionIndex][2]

        metadataDict = bencodepy.encode({
            "msg_type": 0,
            "piece": 0
        })

        message_id = (20).to_bytes(1, byteorder="big")
        extension_message_id = (builder.metadataExtensionId).to_bytes(1, "big")
        sent_length = (1 + 1 + len(metadataDict)).to_bytes(4, byteorder="big")
        sock.send(sent_length + message_id + extension_message_id + metadataDict)

        # Receive metadata size
        length = sock.recv(4)
        while not length or not int.from_bytes(length):
            length = sock.recv(4)

        message = sock.recv(int.from_bytes(length))
        while len(message) < int.from_bytes(length):
            message += sock.recv(int.from_bytes(length) - len(message))
        
        message = bencodepy.decode(b'l' + message[2:] + b'e')

        builder.info = {b"info": message[1]}

        builder.length = message[1][b'length']
        builder.pieceLength = message[1][b'piece length']
        builder.pieces = message[1][b'pieces'].hex()
        
        builder.numberOfPieces = len(builder.pieces)
        builder.parts = [i for i in range(builder.numberOfPieces)]

        return builder
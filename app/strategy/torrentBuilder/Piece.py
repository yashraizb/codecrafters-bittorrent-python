import hashlib
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy
from app.builder.TorrentConnBuilder import TorrentConnBuilder


class Piece(OperationStrategy):

    def __init__(self, pieceIndex: int, connectionIndex: int):
        self.pieceIndex = pieceIndex
        self.connectionIndex = connectionIndex

    def recv(self, sock):
        length = sock.recv(4)
        while not length or not int.from_bytes(length):
            length = sock.recv(4)

        message = sock.recv(int.from_bytes(length))
        while len(message) < int.from_bytes(length):
            message += sock.recv(int.from_bytes(length) - len(message))

        return message

    def execute(self, builder: TorrentConnBuilder):
        numberOfPieces = builder.numberOfPieces
        pieceLength = builder.pieceLength

        if self.pieceIndex + 1 == numberOfPieces:
            pieceLength = builder.length % builder.pieceLength
            if pieceLength == 0:
                pieceLength = builder.pieceLength

        numberOfBlocks = pieceLength // 2**14

        if (pieceLength % (2**14)) != 0:
            numberOfBlocks += 1

        # # Connect to peer
        sock = builder.verifiedConnections[self.connectionIndex][2]

        self.recv(sock)  # Bitfield
        sock.send(b"\x00\x00\x00\x01\x02")
        self.recv(sock)  # Unchoke

        piece = b""

        for i in range(numberOfBlocks):
            begin = i * (2**14)
            blockLength = min(2**14, pieceLength - begin)

            # Send request
            request = (
                b"\x00\x00\x00\x0d\x06"
                + self.pieceIndex.to_bytes(4, byteorder="big")
                + begin.to_bytes(4, byteorder="big")
                + blockLength.to_bytes(4, byteorder="big")
            )
            sock.send(request)

            # Receive piece
            response = self.recv(sock)
            piece += response[9:]  # Skip the message ID and piece index/begin

        pieceHash = hashlib.sha1(piece).hexdigest()

        if pieceHash == builder.pieces[self.pieceIndex * 40 : (self.pieceIndex + 1) * 40]:
            builder.parts[self.pieceIndex] = piece
            print(f"Piece {self.pieceIndex} verified successfully.")
        else:
            print(f"Piece {self.pieceIndex} failed verification.")



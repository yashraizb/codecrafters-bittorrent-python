from app.strategy.command.CommandStrategy import CommandStrategy
from app.domain.TorrentInfo import TorrentInfo
from app.builder.TorrentConnBuilder import TorrentConnBuilder
from app.strategy.torrentBuilder.ReadTorrent import ReadTorrent
from app.strategy.torrentBuilder.Handshake import Handshake
from app.strategy.torrentBuilder.FetchPeers import FetchPeers
from app.domain.HandshakeMessage import HandshakeMessage
import socket
import hashlib
import bencodepy


class DownloadPiece(CommandStrategy):

    def execute(self, data: list):
        torrentInfo: TorrentInfo = TorrentConnBuilder().\
            operation(ReadTorrent(data[2:3])).\
            operation(FetchPeers()).build()
        # torrentInfo: TorrentInfo = torrentInfo.operation(Handshake([0, f"{torrentInfo.peers[0][0]}:{torrentInfo.peers[0][1]}"])).build()

        # torrentInfo.printHandshakePeerId()
        pieceIndex = int(data[3])

        numberOfPieces = len(torrentInfo.info.get(b'info').get(b'pieces')) // 20
        pieceLength = torrentInfo.pieceLength
        
        if pieceIndex + 1 == numberOfPieces:
            pieceLength = torrentInfo.length % torrentInfo.pieceLength
            if pieceLength == 0:
                pieceLength = torrentInfo.pieceLength
        
        numberOfBlocks = pieceLength // 2 ** 14

        if (pieceLength % (2 ** 14)) != 0:
            numberOfBlocks += 1

        infoHash = hashlib.sha1(bencodepy.encode(torrentInfo.info.get(b'info'))).digest()
        peerId = torrentInfo.peerId.encode()

        # Connect to peer
        peer_ip = torrentInfo.peers[0][0]
        peer_port = torrentInfo.peers[0][1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((peer_ip, peer_port))

        print(f"Connected to peer {peer_ip}:{peer_port}")

        # Send handshake
        handshakeMessage = HandshakeMessage(infoHash, peerId).to_bytes()
        sock.send(handshakeMessage)
        print("Sent handshake")

        d = b''

        print(sock.recv(68))  # Handshake response

        def recv(sock):
            length = sock.recv(4)
            while not length or not int.from_bytes(length):
                length = sock.recv(4)
            
            print("Received length:", length, int.from_bytes(length))
            message = sock.recv(int.from_bytes(length))
            while len(message) < int.from_bytes(length):
                message += sock.recv(int.from_bytes(length) - len(message))
        
            print("Received message:", len(length + message))
            return message
        
        recv(sock)  # Bitfield

        sock.send(b"\x00\x00\x00\x01\x02")

        recv(sock)  # Unchoke

        piece = b''

        for i in range(numberOfBlocks):
            begin = i * (2 ** 14)
            blockLength = min(2 ** 14, pieceLength - begin)

            # Send request
            request = b"\x00\x00\x00\x0d\x06" + pieceIndex.to_bytes(4, byteorder='big') + begin.to_bytes(4, byteorder='big') + blockLength.to_bytes(4, byteorder='big')
            sock.send(request)
            print(f"Sent request for piece {pieceIndex}, begin {begin}, length {blockLength}")

            # Receive piece
            data = recv(sock)
        
            # print(f"Received piece {data}")
            piece += data[9:]  # Skip the message ID and piece index/begin
        
        pieceHash = hashlib.sha1(piece).hexdigest()
        if pieceHash == torrentInfo.pieces[pieceIndex * 40: (pieceIndex + 1) * 40]:
            print(f"Piece {pieceIndex} downloaded and verified successfully.")
        else:
            print(f"Piece {pieceIndex} failed verification.")
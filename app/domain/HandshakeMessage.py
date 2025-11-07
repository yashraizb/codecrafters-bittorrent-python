class HandshakeMessage:
    def __init__(self, info_hash, peer_id):
        self.pstr = b"BitTorrent protocol"
        self.reserved = b"\x00" * 8
        self.info_hash = info_hash
        self.peer_id = peer_id
    
    def to_bytes(self):
        pstr_len = len(self.pstr)
        return bytes([pstr_len]) + self.pstr + self.reserved + self.info_hash + self.peer_id
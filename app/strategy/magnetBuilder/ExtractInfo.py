from urllib.parse import unquote
from app.builder.MagnetBuilder import MagnetBuilder
from app.strategy.torrentBuilder.OperationStrategy import OperationStrategy


class ExtractInfo(OperationStrategy):

    def __init__(self, data: list):
        self.data = data

    def execute(self, builder: MagnetBuilder):
        details = {}
        temp = ""
        key = ""

        for char in self.data[0]:
            temp += char
            if char == '?':
                temp = ""
            elif char == '=':
                key = temp[:-1]
                temp = ""
            elif char == '&':
                details[key] = temp[:-1]
                temp = ""
                key = ""
        
        details[key] = temp  # Add the last key-value pair

        builder.infoHash = details["xt"].rsplit(":")[-1]
        builder.name = details["dn"]
        builder.trackerURL = unquote(details["tr"])
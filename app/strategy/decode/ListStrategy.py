import bencodepy
from app.strategy.decode.ParserStrategy import ParserStrategy


class ListStrategy(ParserStrategy):
    def parse(self, data):
        data: list = bencodepy.decode(data[0])
        return data
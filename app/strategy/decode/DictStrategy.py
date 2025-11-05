import bencodepy
from app.strategy.decode.ParserStrategy import ParserStrategy


class DictStrategy(ParserStrategy):
    def parse(self, data):
        data: dict = bencodepy.decode(data[0])
        return data
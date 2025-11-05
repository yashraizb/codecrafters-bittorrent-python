from app.strategy.decode.ParserStrategy import ParserStrategy


class IntegerStrategy(ParserStrategy):
    def parse(self, data):
        # print(data)
        data: str = data[0]
        # print(data)
        return int(data[data.index('i') + 1 : data.index('e')])
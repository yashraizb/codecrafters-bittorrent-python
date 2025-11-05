from app.strategy.command.CommandStrategy import CommandStrategy
from app.factory.DecodeFactory import DecodeFactory
from app.strategy.decode.ParserStrategy import ParserStrategy


class DecodeCommand(CommandStrategy):
    def __init__(self):
        self.decode_factory = DecodeFactory()

    def execute(self, data: list):
        parser: ParserStrategy = self.decode_factory.get_parser(data[0])
        data = parser.parse(data)
        return data
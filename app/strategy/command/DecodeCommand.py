import json
from app.strategy.command.CommandStrategy import CommandStrategy
from app.factory.DecodeFactory import DecodeFactory
from app.strategy.decode.ParserStrategy import ParserStrategy


class DecodeCommand(CommandStrategy):
    def __init__(self):
        self.decode_factory = DecodeFactory()

    def execute(self, data: list):
        try:
            parser: ParserStrategy = self.decode_factory.get_parser(data[0])
            data = parser.parse(data)
            print(json.dumps(data, default=lambda x: x.decode() if isinstance(x, bytes) else x))
        except Exception as e:
            print(f"Error during decoding: {e}")
            print(data)
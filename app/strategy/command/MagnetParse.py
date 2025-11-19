from urllib.parse import unquote
from app.strategy.command.CommandStrategy import CommandStrategy
from app.builder.MagnetBuilder import MagnetBuilder
from app.strategy.magnetBuilder.ExtractInfo import ExtractInfo
from app.domain.Magnet import Magnet


class MagnetParse(CommandStrategy):
    def execute(self, data: list):
        magnetInfo: Magnet = MagnetBuilder().operation(
            ExtractInfo(data)
        ).build()

        magnetInfo.printParsedData()
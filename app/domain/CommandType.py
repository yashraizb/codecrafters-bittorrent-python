from enum import Enum
from app.strategy.command.DecodeCommand import DecodeCommand


class CommandType(Enum):
    DECODE = ("decode", DecodeCommand)
from urllib.parse import unquote
from app.strategy.command.CommandStrategy import CommandStrategy


class MagnetParse(CommandStrategy):
    def execute(self, data: list):
        details = {}
        temp = ""
        key = ""

        for char in data[0]:
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
        
        print("Tracker URL:", unquote(details["tr"]))
        print("Info Hash:", details["xt"].rsplit(":")[-1])
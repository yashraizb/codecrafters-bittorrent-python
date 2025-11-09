from app.strategy.command.CommandStrategy import CommandStrategy


class MagnetParse(CommandStrategy):
    def execute(self, data: list):
        details = {}
        temp = ""
        key = ""

        print(data[0])

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
        
        details[key] = temp[:-1]  # Add the last key-value pair
        
        print(details)

    def _extract_bencoded_value(self, magnet_link):
        # This is a placeholder for the actual extraction logic
        # In a real implementation, you would parse the magnet link
        return b"5:hello"
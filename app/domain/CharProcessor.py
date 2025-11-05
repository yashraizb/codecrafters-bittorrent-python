class CharProcessor:

    def isString(self, char: str):
        return char.isdigit()
    
    def process(self, data: str | bytes) -> str:
        if isinstance(data, bytes):
            data = data[:1].decode('utf-8')
        elif self.isString(data[0]):
            return True
        return data[0]
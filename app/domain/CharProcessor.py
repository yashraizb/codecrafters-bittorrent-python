class CharProcessor:

    def isString(self, char: str):
        return char.isdigit()
    
    def process(self, data: str) -> str:
        if self.isString(data[0]):
            return True
        return data[0]
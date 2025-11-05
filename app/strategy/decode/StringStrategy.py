class StringStrategy:
    def parse(self, data):
        data: str = data[0]
        return data[data.index(':') + 1 : ]
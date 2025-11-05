import bencodepy
from app.strategy.decode.ParserStrategy import ParserStrategy


class DictStrategy(ParserStrategy):

    def recursiveParser(self, d):
        temp = {}
        # print(d)
        for key in d:
            if isinstance(d[key], dict):
                temp[key.decode()] = self.recursiveParser(d[key])
            elif isinstance(d[key], list):
                l = []
                for item in d[key]:
                    if isinstance(item, dict):
                        l.append(self.recursiveParser(item))
                    elif isinstance(item, list):
                        l.append(self.recursiveParser(item))
                    elif isinstance(item, bytes):
                        l.append(item.decode())
                    else:
                        l.append(item)
                temp[key.decode()] = l
            else:
                temp[key.decode()] = d[key].decode() if isinstance(d[key], bytes) else d[key]
        
        return temp

    def parse(self, data):
        data: dict = self.recursiveParser(bencodepy.decode(data[0]))
        # print(data)
        return data
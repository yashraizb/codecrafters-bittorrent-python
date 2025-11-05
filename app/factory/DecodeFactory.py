from app.domain.DecodeType import DecodeType
from app.domain.CharProcessor import CharProcessor


class DecodeFactory:
    def __init__(self):
        self.processor = CharProcessor()
        self._mapping = {
        }

        for decode in DecodeType:
            self._mapping[decode.value[0]] = decode.value[1]
    
    def get_parser(self, parser_name):

        parser_name = self.processor.process(parser_name)
        
        if parser_name in self._mapping:
            return self._mapping[parser_name]()
    
        # Additional parsers can be added here
        raise ValueError(f"Unknown parser: {parser_name}")
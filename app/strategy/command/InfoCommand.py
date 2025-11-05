from strategy.command.CommandStrategy import CommandStrategy


class InfoCommand(CommandStrategy):

    def getFileContents(self, file_path: str) -> bytes:
        with open(file_path, 'rb') as f:
            return f.read()

    def execute(self, data: list):
        info_dict = self.getFileContents(data[0])
        print(info_dict)
        # return info_dict
from app.domain.CommandType import CommandType


class CommandFactory:

    def __init__(self):
        self._mapping = {
        }

        for command in CommandType:
            self._mapping[command.value[0]] = command.value[1]
    
    def get_command(self, command_name):
        if command_name in self._mapping:
            return self._mapping[command_name]()
    
        # Additional commands can be added here
        raise ValueError(f"Unknown command: {command_name}")
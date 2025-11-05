import json
import sys
from app.factory.CommandFactory import CommandFactory
from app.strategy.command.CommandStrategy import CommandStrategy

# import bencodepy - available if you need it!
# import requests - available if you need it!

# Examples:
#
# - decode_bencode(b"5:hello") -> b"hello"
# - decode_bencode(b"10:hello12345") -> b"hello12345"
def decode_bencode(bencoded_value):
    if chr(bencoded_value[0]).isdigit():
        first_colon_index = bencoded_value.find(b":")
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        return bencoded_value[first_colon_index+1:]
    else:
        raise NotImplementedError("Only strings are supported at the moment")


def main():
    try:
        command = sys.argv[1]

        command_factory = CommandFactory()
        command: CommandStrategy = command_factory.get_command(command)

        # You can use print statements as follows for debugging, they'll be visible when running tests.
        print("Logs from your program will appear here!", file=sys.stderr)

        bencoded_value = command.execute(sys.argv[2:])

        # json.dumps() can't handle bytes, but bencoded "strings" need to be
        # bytestrings since they might contain non utf-8 characters.
        #
        # Let's convert them to strings for printing to the console.
        def bytes_to_str(data):
            if isinstance(data, bytes):
                return data.decode()

            raise TypeError(f"Type not serializable: {type(data)}")

        # TODO: Uncomment the code below to pass the first stage
        print(json.dumps(bencoded_value, default=bytes_to_str))
    except Exception as e:
        raise NotImplementedError(f"Unknown command {command}")


if __name__ == "__main__":
    main()

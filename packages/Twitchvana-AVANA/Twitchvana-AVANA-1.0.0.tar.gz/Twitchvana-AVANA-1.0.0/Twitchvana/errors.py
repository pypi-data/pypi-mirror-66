class CommandNotFound(Exception):
    """
        Command does not exist.
    """
    def __init__(self, command):
        super().__init__(f'Command not found')

class CommandExists(Exception):
    """
        Command already exists.
    """
    def __init__(self, command):
        super().__init__(f'Command already exists')

class InvalidChannel(Exception):
    """
        Channel does not exist.
    """
    def __init__(self, channel):
        super().__init__(f'Invalid channel')
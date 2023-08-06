stored_commands = []

class Command:
    """
        Command object.

        channel
            str object representing which channel this command belongs to
        name
            str object representing the command's name
        call
            method that is called when the command is invoked
    """
    def __init__(self, channel, name, com):
        self.channel = channel
        self.name = name.lower()
        setattr(self, 'call', com)
    def call(self, ctx):
        pass

    def edit(self, com):
        setattr(self, 'call', com)

def command(name: str, channel: str = None):
    """
        channel can either be a string or a tuple of strings containing names of streamers.

        Decorator to turn a function into a command
    """
    def wrapper(com):
        if not channel:
            command = Command(channel, name, com)
            stored_commands.append(command)
        elif isinstance(channel, tuple):
            for c in channel:
                command = Command(c, name, com)
                stored_commands.append(command)
        else:
            command = Command(channel, name, com)
            stored_commands.append(command)
    return wrapper
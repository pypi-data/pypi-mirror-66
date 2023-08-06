from .errors import CommandExists, CommandNotFound

class Channel:
    """
        Channel object representing a Twitch channel.

        name
            str object representing the channel's name
        commands
            dictionary that maps command names to command objects.
    """
    def __init__(self, bot, name):
        self._bot = bot
        self.name = name
        self.commands = {}

    def add_command(self, command):
        """
            Adds the command to the channel.

            Raises
                ValueError if name is None or Empty
                CommandExists error if command already exists.
        """

        if command.name in self.commands:
            raise CommandExists(command.name)

        self.commands[command.name] = command

    def get_command(self, name):
        """
            Returns the command.

            Raises:
                CommandNotFound if command doesn't exist.
        """
        if not name in self.commands:
            raise CommandNotFound(name)
        
        return self.commands[name]

    def remove_command(self, name):
        if not name in self.commands:
            raise CommandNotFound(name)
        del self.commands[name]

    def send(self, msg: str):
        """
            Sends msg to the channel.
        """
        self._bot.send_in_channel(self.name, msg)

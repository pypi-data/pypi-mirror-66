import re
from .viewer import Viewer
class Context:
    """
        Context object that is created from a message received by the twitch servers. You should never need to create these

        sender
            str object representing the sender's name
        channel
            str object representing the channel the message was sent in
        msg
            str object representing the message sent
        
        is_command
            boolean representing wether or not it is a command
        command_name
            str object representing the name of the command, None if it isn't a command
        args
            union of str objects representing the arguments, None if it isn't a command
        mentions
            union of str objects representing mentioned users, None if it isn't a command
    """
    def __init__(self, twitch_bot, data : str, msg : str):
        self._bot = twitch_bot

        # Data is in the format of ":<user>!<user>@<user>.tmi.twitch.tv COMM #<CHANNEL> :"
        # msg is the message sent by <user> in plain text

        channel = re.search('#.+ ', data)[0][1:-1]     # Grabs the #<CHANNEL> and removes the #
        self.channel = twitch_bot.channels[channel]

        sender  = re.search(':.+!', data)[0][1:-1]     # Grabs the :<user>! and removes : and !
        self.sender = Viewer(sender, self.channel)

        self.msg = msg

        # Command specific
        self.is_command = msg.startswith(twitch_bot.prefix)
        splt = msg.split(' ')
        self.command_name = splt[0][len(twitch_bot.prefix):].lower() if self.is_command else None
        self.args = splt[1:] if self.is_command else None
        self.mentions = [msg[1:] for msg in re.findall('@[a-zA-Z]+', msg)] if self.is_command else None # Finds all the @<user> in the message and stores the names in a list, removes the @

    def send(self, msg : str):
        """
            Wrapper for Channel.send
            Sends a message in the same channel as the original message is from.
        """
        self.channel.send(msg)
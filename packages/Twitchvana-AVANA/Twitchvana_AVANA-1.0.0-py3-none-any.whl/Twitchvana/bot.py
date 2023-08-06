import threading
import errno
import sys
import re
import random
import time

from .tsocket import create_socket
from .channel import Channel
from .context import Context
from .command import command, Command, stored_commands
from .errors import CommandNotFound, CommandExists, InvalidChannel

class Bot():
    """
        The main bot class
    """
    def __init__(self, oauth : str, user_name : str, channels : list, client_id : str = None, prefix : str ='!'):
        self.name = user_name
        
        self.client_id = client_id
        
        self.socket = create_socket(oauth, user_name)
        self.channels = {channel_name: Channel(self, channel_name) for channel_name in channels}

        self.prefix = prefix

        self.RUNNING = True

        self.global_commands = {}

        for com in stored_commands:
            try:
                self.add_command(com)
            except Exception as e:
                print(f'Could not add command "{com.name}": {e}')

        self.message_limit_msgs = 20
        self.message_limit_time = 30

        self.message_limit_left = 20
        self.last_limit_reset_time = 0

        if not client_id:
            print(f'--- NOTE No Client-ID given, some functionality might be limited.')

    # Handlers

    def handle_command(self, ctx : Context):
        """
            Handles the command invoked by a user.
        """
        try:
            # Look if the command is in global commands
            com = self.global_commands[ctx.command_name]
        except:
            # Else see if it's a valid channel and pick the command
            try:
                channel = self.channels[ctx.channel.name]
                com = channel.get_command(ctx.command_name)
            except Exception as e:
                # Else call the command error event
                self.event_command_error(ctx, e)
                return
        
        # TODO | Should probably work with asyncio-based programming instead of thread-based
        thread = threading.Thread(target=com.call, args=(self, ctx))
        thread.start()

    # Add

    def add_command(self, command : Command):
        """
            Adds a command to the bot.

            Raises
                InvalidChannel if the channel doesn't exist.
                CommandExists if the command already exists.

            Also propagates all errors.
        """
        if not command.name:
            raise ValueError('Command name is None or empty')
        if command.name in self.global_commands:    
            raise CommandExists(command.name)
        
        if not command.channel:
            self.global_commands[command.name] = command

        else:
            if not command.channel in self.channels:
                raise InvalidChannel(command.channel)
            
            self.channels[command.channel].add_command(command)

    def get_command(self, channel: str, name: str):
        if channel in self.channels:
            com = self.channels[channel].get_command(name)
            return com
        raise InvalidChannel(channel)
    
    # Decorators

    def event(self, com):
        """
            Decorator for events.
        """
        setattr(self, com.__name__, com)


    def event_message(self, ctx: Context):
        """
            Event that is invoked when a message is received.
        """
        if ctx.sender.name == self.name:
            return

        if ctx.is_command:
            self.handle_command(ctx)

    def event_join(self):
        """
            Event that is invoked when the bot has finished joining all streams. 
        """
        print(f'--- Joined {len(self.channels)} channels ({", ".join([self.channels[c].name for c in self.channels])})')

    def event_command_error(self, ctx : Context, e : Exception):
        print(f'Could not handle command {ctx.command_name}: "{e}"')

    # idk
    def start(self):
        """
            Starts the bot.
        """
        print(f'--- Starting the bot')
        self._join_initial_channels()

        self.event_join()

        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()

        while self.RUNNING:
            try:
                time.sleep(1)

                if time.time() - self.last_limit_reset_time >= self.message_limit_time:
                    self.last_limit_reset_time = time.time()
                    self.message_limit_left = self.message_limit_msgs

            except KeyboardInterrupt:
                self.RUNNING = False
                print(f'ERROR Keyboard Interrupt, exciting code')
            except Exception as e:
                print(f'ERROR Error "{e}" occured')

    def _join_initial_channels(self):
        """
            Joins the inital channels.
        """
        for user in self.channels:
            self._send_socket_msg(f'JOIN #{user}')

    def _send_socket_msg(self, msg : str):
        """
            Encodes the message into bytes and sends it.
        """
        if self.message_limit_left > 0:
            self.message_limit_left -= 1
            self.socket.send(f'{msg}')
        else:
            print(f'ERROR DID NOT SEND MESSAGE "{msg}" DUE TO LIMIT BEING REACHED.')

    def send_in_channel(self, channel : str, msg : str):
        """
            Sends a message in a channel.
        """
        self._send_socket_msg(f'PRIVMSG #{channel} :{msg}')

    def run(self):
        """
            Runs the bot.
        """
        while True:
            try:
                msg = self.socket.recv(4096)
            except Exception as e:
                print(f'ERROR Error {str(e)} occured.')
                sys.exit(0)
            else:

                data, msg = split_socket_data(msg.decode())
                
                if not data: continue

                # Check if it's the PING message and respond 
                if msg == 'PING :tmi.twitch.tv':
                    self._send_socket_msg('PONG :tmi.twitch.tv')
                else:
                    context = Context(self, data, msg)
                    self.event_message(context)

def split_socket_data(msg):
    """
        Takes a message received by Twitch's servers and splits it into (data, msg) pair
        where data is information about the sender and msg is the message itself.
    """
    # TODO TEMPORARY SOLUTION
    is_ping = re.search('^PING', msg)
    if is_ping:
        return 'twitch', 'PING :tmi.twitch.tv'

    data = re.search('^:.+!.+@.+ :', msg[:])
    if not data:    
        return None, None
    data = data[0]
    msg = msg.replace(data, '').replace('\r\n', '')
    return data, msg
import requests
from .user_data_fetcher import get_user_data, get_user_ids

class Viewer:
    """
        Object representing a Viewer in a specific channel.

        name
            str representing the viewers's name
        channel
            channel object representing the channel
        
        PROPERTIES:
            mention
                returns @<user_name>
            id
                int representing the viewer's id
            is_moderator
                boolean representing whether or not the viewer is a moderator in channel
            is_subscriber
                boolean representing whether or not the viewer is a subscriber in channel
            is_bot
                boolean representing whether or not the viewer is a bot
    """
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel
        self._client_id = self.channel._bot.client_id
        
        self._data = None

    @property
    def name(self):
        return self._name

    @property
    def channel(self):
        return self._channel

    @property
    def client_id(self):
        return self._client_id

    @property
    def mention(self):
        return '@' + self.name

    @property
    def is_moderator(self):
        badges = [badge['id'] for badge in self.data['badges']]
        return any(x in badges for x in ('moderator', 'broadcaster'))

    @property
    def is_subscriber(self):
        badges = [badge['id'] for badge in self.data['badges']]
        return any(x in badges for x in ('subscriber', 'founder'))

    @property
    def is_bot(self):
        return self.data['is_verified_bot']

    @property
    def id(self):
        return self.data['_id']

    @property
    def data(self):
        if not self.client_id:
            raise AttributeError('No client id.')
        if not self._data:
            self.data = get_user_data(self.name, self.channel.name, self.client_id)
        return self._data
    @data.setter
    def data(self, value):
        if self._data:
            raise AttributeError('Cannot set attribute data once it has been set once.')
        self._data = value
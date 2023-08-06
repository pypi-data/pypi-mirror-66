import requests
URL_FOR_USER_ID = 'https://api.twitch.tv/kraken/users?login='
URL_FOR_USER_DATA = 'https://api.twitch.tv/kraken/users/{user_id}/chat/channels/{channel_id}?api_version=5'


def get_user_ids(users: list, client_id : str):
    """
        Returns a list of (user_name, user_id) tuples.
    """
    url = url_for_user_id(users)

    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': client_id
    }

    r = requests.get(url, headers=headers)
    data = r.json()

    user_name_id_pairs = []
    for user in data['users']:
        user_name_id_pairs.append((user['display_name'], user['_id']))
    return user_name_id_pairs

def get_user_data(user, channel, client_id: str):
    """
        Returns a json containing data about user in channel.
    """
    if isinstance(user, str) and isinstance(channel, str):
        ids = get_user_ids([user, channel], client_id)
        user_id = ids[0][1]
        channel_id = ids[1][1]
    elif isinstance(user, int) and isinstance(channel, int):
        user_id = user
        channel_id = channel
    else:
        raise ValueError('Not matching types')

    url = url_for_user_data(user_id, channel_id)
    headers = {'Client-ID': client_id}
    r = requests.get(url, headers=headers)
    data = r.json()

    return data

def url_for_user_id(users: list):
    """
        Returns a url that returns user ids. Users must be a list of strings representing user names.
    """
    return URL_FOR_USER_ID + ','.join(users)

def url_for_user_data(user_id : str, channel_id : str):
    """
        Returns a url that returns user data. 
    """
    return f'https://api.twitch.tv/kraken/users/{user_id}/chat/channels/{channel_id}?api_version=5'
class ClientInfo:

    language = 'en-US'

    def __init__(self, raw_client_info):
        key_values = raw_client_info.split(';')
        for key_value in key_values:
            key, value = key_value.split('=')
            setattr(self, key, value)

class UserAgent:

    language = 'en-US'

    def __init__(self, raw_user_agent):
        key_values = raw_user_agent.split(';')
        for key_value in key_values:
            key, value = key_value.split('=')
            setattr(self, key, value)

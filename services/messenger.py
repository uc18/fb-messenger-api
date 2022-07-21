from fbchat import Client
from fbchat.models import *


def get_client(email: str, password: str, user_agent: str, cookies=None) -> Client:
    return Client(email, password, user_agent, max_tries=1, session_cookies=cookies)


from socket import *
from youku客户端.conf import settings


def get_client():
    client = socket(AF_INET,SOCK_STREAM)
    client.connect((settings.host,settings.port))
    return client







from socket import *
from conf import settings

def client_conn():

    client = socket(AF_INET,SOCK_STREAM)

    client.connect((settings.host,settings.port))

    return client


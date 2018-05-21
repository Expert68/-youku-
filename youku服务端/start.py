import os,sys
from youku服务端.server import tcpserver

path = os.path.dirname(__file__)
sys.path.append(path)

if __name__ == '__main__':
    tcpserver.server_run()
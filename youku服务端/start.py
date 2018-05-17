
import os,sys

path = os.path.dirname(__file__)

sys.path.append(path)

from server import tcpserver

if __name__ == '__main__':
    tcpserver.server_run()
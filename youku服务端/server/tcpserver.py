import json
from socket import *
import struct
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from threading import current_thread
from youku服务端.conf import settings
from youku服务端.interface import common_interface,admin_interface,user_interface
from youku服务端.server import user_data

server_pool = ThreadPoolExecutor(10)
mutex = Lock()
user_data.mutex = mutex
dispatch_dic = {
    'login': common_interface.login,
    'register': common_interface.register,
    'upload': admin_interface.upload_movie,
    'delete_movie': admin_interface.delete_movie,
    'download_movie': user_interface.download_movie,
    'release_notice': admin_interface.release_notice,
    'buy_member': user_interface.buy_member,
    'get_movie_list': user_interface.get_movie_list,
    'check_notice': user_interface.check_notice,
    'check_download_record': user_interface.check_download_record,
    'check_movie': admin_interface.check_movie
}

def server_run():
    server = socket(AF_INET,SOCK_STREAM)
    server.bind(settings.server_address)
    server.listen(5)

    while True:
        conn,addr = server.accept()
        print('%s连接成功' %str(addr))
        server_pool.submit(working,conn,addr)

def working(conn,addr):
    print(current_thread().name)
    while True:
        try:
            header_dic_len_bytes = conn.recv(4)
            if not header_dic_len_bytes:break
            header_dic_bytes = conn.recv(struct.unpack('i',header_dic_len_bytes)[0])
            header_dic = json.loads(header_dic_bytes.decode('utf-8'))
            header_dic = str(addr)

            dispatch(header_dic,conn)

        except Exception as e:
            print(e)
            conn.close()
            mutex.acquire()
            if str(addr) in user_data.alive_user:
                user_data.alive_user.pop(str(addr))
            mutex.release()

            print('%s断开链接' %str(addr))
            break

def dispatch(header_dic,conn):
    if header_dic not in dispatch_dic:
        back_dic = {'flag':False,'msg':'没有该功能'}
        send_back(back_dic,conn)
    else:
        dispatch_dic[header_dic['type']](header_dic,conn)

def send_back(header_dic,conn):
    header_dic_bytes = json.dumps(header_dic).encode('utf-8')
    header_dic_len = struct.pack('i',header_dic_bytes)
    conn.send(header_dic_len)
    conn.send(header_dic_bytes)








    


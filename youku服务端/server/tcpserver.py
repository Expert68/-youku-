from socket import *
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from threading import current_thread,Thread
from conf import settings
import struct
import json
from interface import common_interface,admin_interface,user_interface,login_user_data
import time

server_pool = ThreadPoolExecutor(2)
mutex = Lock()

dispatch_dic={
    'register': common_interface.register,
    'delete_movie': admin_interface.delete_movie,
    'release_notice': admin_interface.release_notice,
    'buy_member': user_interface.buy_member,
    'get_movie_list': user_interface.get_movie_list,
    'check_notice': user_interface.check_notice,
    'check_download_record': user_interface.check_download_record
}

def working(conn,addr):
    print(current_thread().name())
    while True:
        try:
            head_struct = conn.recv(4)
            if not head_struct:break
            head_len = struct.unpack('i',head_struct)[0]
            head_json = conn.recv(head_len).decode('utf-8')
            head_dic = json.loads(head_json)

            head_dic['addr'] = addr[1]

        except Exception:
            conn.close()

            mutex.acquire()
            if addr[1] in login_user_data.alive_user:
                login_user_data.alive_user.pop(addr[1])

            mutex.release()

            print('客户端：%s：断开连接' %str(addr))

            break

def dispatch(head_dic,conn):

    if head_dic['type'] == 'login':
        back_dic = common_interface.login(head_dic,mutex)
        send_back(back_dic,conn)

    elif head_dic['type'] == 'download_movie':
        back_dic=uesr_interface.download_movie(head_dic)
        send_back(back_dic,conn)

        with open(back_dic['path'],'rb') as f:
            for line in f:
                conn.send(line)

    elif head_dic['type'] == 'upload':
        back_dic = admin_interface.upload_movie(head_dic,conn)
        send_back(back_dic,conn)

    else:
        if head_dic['type'] not in dispatch_dic:
            back_dic = {'flag':False,'msg':'请求不存在'}
            send_back(back_dic,conn)

        else:
            back_dic = dispatch_dic[head_dic['type']](head_dic)
            send_back(back_dic,conn)


def send_back(back_dic,conn):
    head_json_bytes = json.dumps(back_dic).encode('utf-8')
    conn.send(struct.pack('i',len(head_json_bytes)))
    conn.send(head_json_bytes)


def server_run():
    socket_server = socket(AF_INET,SOCK_STREAM)
    socket_server.bind(settings.server_address)
    socket_server.listen(5)

    while True:
        conn,addr = socket_server.accept()
        print('客户端：%s链接成功' %str(addr))
        server_pool.submit(working,conn,addr)

    socket_server.close()




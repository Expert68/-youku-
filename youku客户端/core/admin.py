from youku客户端.client import tcpclient
import os
from youku客户端.conf import settings
from youku客户端.lib import common

admin_data = {'session':None}

send_dic = {'type':None,'user_type':None,'session':None}


def admin_register(client):
    while True:
        name = input('用户名：').strip()
        pwd1 = input('密码：').strip()
        pwd2 = input('请再次输入密码：').strip()
        if pwd1 == pwd2:
            send_dic = {'type':'register','user_type':'admin','name':name,'password':common.make_md5(pwd1)}
            back_dic = common.send_data(client,send_dic)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print('两次密码输入不一致，请重新输入')

def admin_login(client):
    while True:
        name = input('用户名：').strip()
        password = input('密码：').strip()
        send_dic = {'type': 'register', 'user_type': 'admin', 'name': name, 'password': common.make_md5(password)}
        back_dic = common.send_data(client,send_dic)
        if back_dic['flag']:
            admin_data['session'] = back_dic['session']
            print(back_dic['msg'])
            break
        else:
            print(back_dic['msg'])

def upload_movie(client):
    if not admin_data['session']:
        print('请先登录')
        return
    while True:
        up_list = common.get_filelist_by_path(settings.BASE_UPLOAD_DIR)
        if not up_list:
            print('暂时没有可上传的电影')
            return
        for i,movie in enumerate(up_list):
            print(i,movie)
        choice = input('请输入电影编号：').strip()
        if choice.isdigit():
            choice = int(choice)
            if choice <= len(up_list):
                file_path = os.path.join(settings.BASE_UPLOAD_DIR,up_list[choice])
                file_md5 = common.get_file_md5(file_path)
                send_dic = {'type':'check_movie','file_md5':file_md5,'session':admin_data['session']}
                back_dic = common.send_data(client,send_dic)
                if back_dic['flag']:
                    is_free = input('是否免费（y/n):').strip()
                    if is_free == 'y':
                        is_free = 1
                    else:
                        is_free = 0
                    file_size = os.path.getsize(file_path)
                    send_dic = {'type':'upload','session':admin_data['session'],'is_free':is_free,'file_md5':file_md5,'file_size':file_size}
                    back_dic = common.send_data(client,send_dic,file_path)
                    if back_dic['flag']:
                        print(back_dic['msg'])
                    else:
                        print(back_dic['msg'])
                else:
                    print(back_dic['msg'])
            else:
                print('请输入范围内的数字')
        else:
            print('请输入整数')



def delete_movie(client):
    if not admin_data['session']:
        print('请先登录')
        return
    while True:
        send_dic = {'type':'get_movie_list','session':admin_data['session'],'movie_type':'all'}
        back_dic = common.send_data(client,send_dic)
        if back_dic['flag']:
            for i,movie in enumerate(back_dic['movie_list']):
                print('%s:%s--%s' %(i,movie[0],movie[1]))
            choice = input('请输入要删除的电影代码：').strip()
            if choice.isdigit():
                choice = int(choice)
                if choice <= len(back_dic['movie_list']):
                    movie_id = back_dic['movie_list'][choice][2]
                    send_dic = {'type':'delete_movie','session':admin_data['session'],'movie_id':movie_id}
                    back_dic = common.send_data(client,send_dic)
                    if back_dic['flag']:
                        print(back_dic['msg'])
                        break
                    else:
                        print(back_dic['msg'])
                else:
                    print('请输入范围内的数字')
            else:
                print('请输入整数')
        else:
            print(back_dic['msg'])




def release_notice(client):
    if not admin_data['session']:
        print('请先登录')
        return
    notice_name = input('请输入公告标题：').strip()
    notice_content = input('请输入公告内容：').strip()
    send_dic = {'type':'release_notice','session':admin_data['session'],'notice_name':notice_name,'notice_content':notice_content}
    back_dic = common.send_data(client,send_dic)
    if back_dic['flag']:
        print(back_dic['msg'])
    else:
        print(back_dic['msg'])







func_dic = {
    '1':admin_register,
    '2':admin_login,
    '3':upload_movie,
    '4':delete_movie,
    '5':release_notice
}

def admin_view():
    client = tcpclient.get_client()
    while True:
        print("""
        1、注册
        2、登录
        3、上传视频
        4、删除视频
        5、发布公告
        """)
        choice = input('请输入编号：').strip()
        if choice == 'q':break
        if choice not in func_dic:continue
        func_dic[choice](client)
    client.close()





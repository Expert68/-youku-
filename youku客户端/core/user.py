from client import tcpclient
from lib import common
from conf import settings
import os
import time

user_data = {'session':None,
             'name':None,
             'is_vip':None
             }

send_dic = {'type':None,'user_type':'user','name':None,'session':None}

def user_register(client):
    print('用户注册')
    while True:
        name = input('请输入手机号:').strip()
        password = input('请输入密码：').strip()
        conf_password = input('请确认密码：').strip()
        if password == conf_password:
            send_dic = {'type': 'register', 'user_type': 'user', 'name': name, 'password': password}
            back_dic = common.send_data(client, send_dic, None)

            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])

        else:
            print('两次密码输入的不一致')

def user_login(client):
    print('用户登录')
    while True:
        name = input('用户名：').strip()
        if name == 'q':break
        password = input('密码：').strip()
        send_dic = {'type':'login','user_type':'admin','name':name,'password':password}

        back_dic = common.send_data(client,send_dic,None)
        if back_dic['flag']:
            user_data['name'] = name
            user_data['session'] = back_dic['session']
            user_data['is_vip'] = back_dic['is_vip']
            print(back_dic['msg'])
            break

        else:
            print(back_dic['msg'])

def buy_membership(client):
    print('购买会员')
    if not user_data['name']:
        print('请先登录')
        return
    if user_data['is_vip']:
        print('已经是会员，无须购买')
        return

    while True:
        buy = input('是否购买会员').strip()
        if buy == 'y':
            send_dic = {'type': 'buy_membership', 'user_type': 'admin', 'name': user_data['name'], 'session': user_data['session']}
            back_dic = common.send_data(client,send_dic,None)
            if back_dic['flag']:
                user_data['is_vip'] = True
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])

        elif buy == 'q':
            break

def get_movie_list(client):
    if not user_data['name']:
        print('请先登录')
        return

    print('查看识破列表')
    while True:
        send_dic = {'type': 'get_movie_list', 'user_type': 'admin', 'name': user_data['name'],
                    'session': user_data['session']}
        back_dic = common.send_data(client,send_dic,None)
        if back_dic['flag']:
            for i,m in enumerate(back_dic['movie_list']):
                print('%s:%s--%s' %(i,m[0],m[1]))
            break

        else:
            print(back_dic['msg'])
            break

def down_free_movie(client):
    if not user_data['name']:
        


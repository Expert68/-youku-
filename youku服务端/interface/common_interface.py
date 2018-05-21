from youku服务端.db import models
from youku服务端.lib import common
from youku服务端.interface import user_interface
from youku服务端.server import user_data as da


def login(user_dic,conn):
    """
    登录功能，登录成功，将用户信息以{'addr':[session,user_id]}的形式，放到内存中，
    多线程操作，必须加锁，锁需要在主线程中生成
    :param user_dic:
    :param conn:
    :return:
    """
    user = models.User.select_one(name=user_dic['name'])
    if user:
        if user.user_type == user_dic['user_type']:
            if user.password == user_dic['password']:
                session = common.get_uuid(user_dic['name'])
                da.mutex.acquire()
                if user_dic['addr'] in da.alive_user:
                    da.alive_user.pop(user_dic['addr'])
                da.alive_user[user_dic['addr']] = [session,user.id]
                da.mutex.release()
                back_dic = {'flag':True,'session':session,'is_vip':user.is_vip,'msg':'login_success'}
                if user_dic['user_type'] == 'user':
                    last_notice = user_interface.check_notice_by_count(1)
                    back_dic['last_notice'] = last_notice
            else:
                back_dic = {'flag':False,'msg':'密码错误'}
        else:
            back_dic = {'flag':False,'msg':'登录类型不匹配'}
    else:
        back_dic = {'flag':False,'msg':'用户不存在'}
    common.send_back(back_dic,conn)

def register(user_dic,conn):
    """
    注册功能
    :param user_dic:
    :param conn:
    :return:
    """
    user = models.User.select_one(name=user_dic['name'])
    if user:
        back_dic = {'flag':False,'msg':'用户已存在'}
    else:
        user = models.User(name=user_dic['name'],password=user_dic['password'],user_type=user_dic['user_type'])
        user.save()
        back_dic = {'flag':True,'msg':'注册成功'}
    common.send_back(back_dic,conn)

    
from conf import settings
import os
from db import models
from lib import common


def upload_movie(user_dic,conn):
    recv_size = 0
    print('------>',user_dic['file_name'])
    path = os.path.join(settings.BASE_MOVIE_LIST,user_dic['file_name'])
    with open(path,'wb') as f:
        while recv_size < user_dic['file_size']:
            recv_data = conn.recv(1024)
            f.write(recv_data)
            recv_size += len(recv_data)


    print('%s:上传成功' %user_dic['file_name'])
    movie = models.Movie(user_dic['file_name'],path,user_dic['is_free'],user_dic['name'])

    movie.save()
    back_dic = {'flag':True,'msg':'上传成功'}
    return back_dic

def delete_movie(user_dic):

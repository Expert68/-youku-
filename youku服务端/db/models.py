from youku服务端.orm_pool.fuckorm_pool import *

class User(Modles):
    table_name = 'user_info'
    id = IntegerFileld('id',primary_key=True)
    name = StringFileld('name')
    password = StringFileld('password')
    locked = IntegerFileld('locked',default=0)
    is_vip = IntegerFileld('is_vip',default=0)
    user_type = StringFileld('user_type')


class Movie(Modles):
    table_name = 'movie'
    id = IntegerFileld('id',primary_key=True)
    name = StringFileld('name')
    path = StringFileld('path')
    is_free = IntegerFileld('is_free',default=1)
    is_delete = IntegerFileld('is_delete',default=0)
    create_time = StringFileld('create_time')
    user_id = IntegerFileld('user_id')
    file_md5 = StringFileld('file_md5')

class Notice(Modles):
    table_name = 'notice'
    id = IntegerFileld('id',primary_key=True)
    name = StringFileld('name')
    content = StringFileld('content')
    user_id = IntegerFileld('user_id')
    create_time = StringFileld('create_time')


class DownloadRecord(Modles):
    table_name = 'download_record'
    id = IntegerFileld('id',primary_key=True)
    user_id = IntegerFileld('user_id')
    movie_id = IntegerFileld('movie_id')





from youku服务端.db import models
import os
from youku服务端.lib import common
def check_notic_by_count(count=None):
    """
    查看功能的方法，供内部调用
    count为None查全部，为1查一条
    :param count:
    :return:
    """
    notice_list = models.Notice.select_many()
    back_notice_list = []
    if notice_list:
        if not count:
            for notice in notice_list:
                back_notice_list.append({notice.name:notice.content})
        else:
            last_row = len(notice_list) - 1
            back_notice_list.append({notice_list[last_row].name:notice_list[last_row].content})
            return back_notice_list
    else:
        return False



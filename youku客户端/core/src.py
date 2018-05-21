from youku客户端.core import admin,user


func_dic = {
    '1':admin.admin_view,
    '2':user.user_view
}


def src():
    while True:
        print("""
        1、管理员视图
        2、用户视图
        """)

        choice = input('请输入编号：').strip()
        if choice == 'q':
            break

        elif choice in func_dic:
            func_dic[choice]()

        else:
            print('请输入正确的编号')



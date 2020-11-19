buinese_name_list = {'admin': 'nku123'}
customer_user_lists = {}
exist_good_lists = {}
all_good_lists = {}
shoppingcar = {}

def initiazation():
    with open('shoppingcar.txt', 'r') as f_obj:
        for line in f_obj:
            temp1 = {}
            line = line.strip()
            temp = line.split('&', 1)
            strs = temp[1].split('&')
            for str1 in strs:
                str1 = str1.split('|')
                product = (str1[0], int(str1[1]))
                temp1[product] = int(str1[2])
            shoppingcar[temp[0]] = temp1

def print_good_list():
    #打印商品列表
    print('--------------------------------------')
    print("商品编号    商品名称    商品价格")
    filename1 = 'good_lists.txt'
    with open(filename1, 'r') as f:
        for line in f:
            line = line.strip()
            line_list = line.split('|')
            line_list[2] = int(line_list[2])
            exist_good_lists[line_list[0]] = line_list
            print("%-11s%-11s%-12s" % (line_list[0], line_list[1], str(line_list[2])+'RMB'))
    print('...')
    print('--------------------------------------')

def recharge(name, filename):
    print('是否进行充值： Y/N')
    choice = input()
    if choice == 'Y' or 'y':
        recharger = input('请输入要充值的金额： ')
        print('--------------------------------------')
        customer_user_lists[name][2] += int(recharger)
        file_data = ""
        with open(filename, 'r') as f_obj:
            for line in f_obj:
                if name in line:
                    temp = line.split('|')
                    line = line.replace(temp[2], str(customer_user_lists[name][2]))
                    line = line + '\n'
                file_data += line
        with open(filename, 'w') as f_obj:
            f_obj.write(file_data)

def choose_good(name):
    print('--------------------------------------')
    print('请输入你要添加的商品编号： ')
    good_id = input()
    print('请输入你要添加的商品数量： ')
    good_number = int(input())
    print('--------------------------------------')
    if name in shoppingcar:
        my_shoppingcar = shoppingcar[name]
    else:
        my_shoppingcar = {}
    if good_id not in exist_good_lists:
        print('抱歉，您想要的商品暂时不存在！')
    else:
        product = (exist_good_lists[good_id][1], exist_good_lists[good_id][2])
        if product not in my_shoppingcar:
            my_shoppingcar[product] = good_number
        else:
            my_shoppingcar[product] += good_number
        shoppingcar[name] = my_shoppingcar
        flag = False
        with open('shoppingcar.txt', 'r') as f:
            for line1 in f:
                if name in line1:
                    flag = True
        if flag == True:
            filedata1 = ""
            with open('shoppingcar.txt', 'r') as f:
                for line1 in f:
                    if name in line1:
                        line1 = line1.strip()
                        line1 = name
                        for item1, value in shoppingcar[name].items():
                            str2 = item1[0] + '|' + str(item1[1]) + '|' + str(value)
                            line1 = line1 + '&' + str2
                        line1 = line1 + '\n'
                    filedata1 += line1
            with open('shoppingcar.txt', 'w') as f1:
                f1.write(filedata1)
        else:
            with open('shoppingcar.txt', 'a') as f:
                line1 = name
                for item1, value in shoppingcar[name].items():
                    str1 = item1[0] + '|' + str(item1[1]) + '|' + str(value)
                    line1 = line1 + '&' + str1
                line1 = line1 + '\n'
                f.write(line1)

def delete_my_good(name):
    if name not in shoppingcar:
        print('您还没有选择任何商品，快去挑选一些吧！')
    else:
        print('--------------------------------------')
        print('请输入你要删除的商品编号： ')
        good_id = input()
        print('请输入你要删除的商品数量： ')
        good_number = int(input())
        print('--------------------------------------')
        my_shoppingcar = shoppingcar[name]
        if good_id not in exist_good_lists:
            print('抱歉，您想删除的商品暂时不存在！')
        else:
            product = (exist_good_lists[good_id][1], exist_good_lists[good_id][2])
            if product not in my_shoppingcar:
                print('您还没有选择这个物品啊！')
            else:
                if (my_shoppingcar[product] - good_number) <= 0:
                    del my_shoppingcar[product]
                    shoppingcar[name] = my_shoppingcar
                    for key in list(shoppingcar.keys()):
                        if not shoppingcar.get(key):
                            del shoppingcar[key]
                else:
                    my_shoppingcar[product] -= good_number
                    shoppingcar[name] = my_shoppingcar
            with open('shoppingcar.txt', 'w') as f:
                for key in list(shoppingcar.keys()):
                    line1 = key
                    for item1, value in shoppingcar[key].items():
                        str1 = item1[0] + '|' + str(item1[1]) + '|' + str(value)
                        line1 = line1 + '&' + str1
                    line1 = line1 + '\n'
                    f.write(line1)

def clear_my_shoppingcar(name):
    # 清空购物车
    if name in shoppingcar:
        my_shoppingcar = shoppingcar[name]
        for key, value in shoppingcar[name].items():
            sum1 = customer_user_lists[name][2] - key[1] * value
        if sum1 >= 0:
            print('----------你已经购买了如下商品----------')
            for key, value in shoppingcar[name].items():
                print("%s:%s" % (key, value))
                file_data = ""
                with open("all_good_lists.txt", 'r') as f_obj1:
                    for line1 in f_obj1:
                        if key[0] in line1:
                            line1 = line1.strip()
                            temp = line1.split('|')
                            line1 = line1.replace(temp[2], str(int(temp[2]) + value * key[1]))
                            line1 = line1 + '\n'
                        file_data += line1
                        product = (key[0], int(key[1]))
                with open('all_good_lists.txt', 'w') as f_obj1:
                    f_obj1.write(file_data)

            file_data = ""
            filename = 'customer_name_lists.txt'
            with open(filename, 'r') as f_obj:
                for line in f_obj:
                    if name in line:
                        temp = line.split('|')
                        line = line.replace(temp[2], str(sum1))
                        line = line + '\n'
                    file_data += line
            with open(filename, 'w') as f_obj:
                f_obj.write(file_data)
            print('您的账户余额还有：%s' % sum1)
            customer_user_lists[name][2] = sum1
            del shoppingcar[name]
            file_data = ""
            with open('shoppingcar.txt', 'r') as f:
                for line3 in f:
                    if name not in line3:
                        file_data += line3
            with open('shoppingcar.txt', 'w') as f:
                f.write(file_data)
        else:
            print('您的账户余额不足，请充值后购买！')
            print('--------------------------------------')
            filename = 'customer_name_lists.txt'
            recharge(name, filename)
    else:
        my_shoppingcar = {}
        print('您还没有购买任何商品！')
        print('--------------------------------------')

def sign():
    name = input('>>u ')
    filename = 'customer_name_lists.txt'
    with open(filename, 'r') as f_obj:
        for line in f_obj:
            line = line.strip()
            line_list = line.split('|')
            line_list[2] = int(line_list[2])
            customer_user_lists[line_list[0]]=line_list
        if name not in customer_user_lists:
            print('用户不存在！')
            print('是否进行注册：Y/N')
            choice = input()
            if choice == 'Y':
                register()
        else:
            passward = input('>>p ')
            if passward == customer_user_lists[name][1]:
                print('登陆成功！')
                print_good_list()
                while True:
                    print('请选择你要进行的操作： ')
                    print('0 添加商品    1 删除商品     2 结算购物车    3 退出')
                    choice = input()
                    if choice == '0':
                        choose_good(name)
                    elif choice == '1':
                        delete_my_good(name)
                    elif choice == '2':
                        clear_my_shoppingcar(name)
                    elif choice == '3':
                        print('欢迎下次光临！ ')
                        break
                    else:
                        print('暂未开通此功能！')
            else:
                print('密码不正确。')

def register():
    print('请输入你的用户名和密码：')
    username = input('>>u ')
    filename = 'customer_name_lists.txt'
    while True:
        with open(filename, 'r') as f_obj:
            for line in f_obj:
                line = line.strip()
                line_list = line.split('|')
                line_list[2] = int(line_list[2])
                customer_user_lists[line_list[0]] = line_list
        if username in customer_user_lists:
            print('用户名已存在，请重新输入：')
            username = input('>>u ')
        else:
            break
    passward = input('>>p ')
    print('请输入你的初始金额： ')
    balance = int(input())
    with open(filename, 'a') as f_obj:
        temp = username + '|' + passward + '|' + str(balance) + '\n'
        f_obj.write(temp)

def delete_good(old_id, filename):
    #删除商品
    if old_id in exist_good_lists:
        file_data = ""
        with open(filename, 'r') as f_obj:
            for line in f_obj:
                if old_id not in line:
                    file_data += line
        with open(filename, 'w') as f_obj:
            f_obj.write(file_data)
    else:
        print('该商品不存在！')

def add_good(good_id, good_name, good_price,filename,filename1):
    #添加商品
    with open(filename, 'a') as f_obj:
        temp = good_id + '|' + good_name + '|' + good_price + '\n'
        f_obj.write(temp)
    with open(filename1, 'a') as f_obj1:
        temp1 = good_name + '|' + good_price + '|' + '0' + '\n'
        f_obj1.write(temp1)

def change_good_price(old_id, new_price,filename):
    #更改商品（主要更改定价）
    file_data = ""
    with open(filename, 'r') as f_obj:
        for line in f_obj:
            if old_id in line:
                temp = line.split('|')
                line = line.replace(temp[2], new_price)
                line = line + '\n'
            file_data += line
    with open(filename, 'w') as f_obj:
        f_obj.write(file_data)
    file_data = ""
    with open('all_good_lists.txt', 'r') as f_obj1:
        for line1 in f_obj1:
            if exist_good_lists[old_id][1] in line1:
                temp1 = line1.split('|')
                line1 = temp1[0] + '|' + new_price + '|' + temp1[2]
                #line1 = line1 + '\n'
            file_data += line1
    with open('all_good_lists.txt', 'w') as f_obj:
        f_obj.write(file_data)
    file_data = ""
    with open('shoppingcar.txt', 'r') as f_obj2:
        for line in f_obj2:
            if exist_good_lists[old_id][1] in line:
                line = line.replace(temp[2], new_price)
                line = line + '\n'
            file_data += line
    with open('shoppingcar.txt', 'w') as f_obj:
        f_obj.write(file_data)

def change_good_list(x):
    #改变商品列表#
    filename = 'good_lists.txt'
    filename1 = 'all_good_lists.txt'
    if x == 0:
        old_id = input('请输入你想要更改的商品编号：')
        new_price = input('请输入新的定价： ')
        change_good_price(old_id, new_price, filename)
        while True:
            print('是否继续更改商品： Y/N')
            choice = input()
            if choice == 'Y':
                print('请输入你想要更改的商品编号：')
                old_id = input('商品编号: ')
                new_price = input('请输入商品定价： ')
                change_good_price(old_id, new_price, filename)
            else:
                break

    elif x == 1:
        print('请输入你想要添加的商品编号及名称：')
        good_id = input('商品编号: ')
        good_name = input('商品名称： ')
        print('请输入商品定价： ')
        good_price = input('商品价格： ')
        add_good(good_id, good_name, good_price, filename, filename1)
        while True:
            print('是否继续添加商品： Y/N')
            choice = input()
            if choice == 'Y':
                print('请输入你想要添加的商品编号及名称：')
                good_id = input('商品编号: ')
                good_name = input('商品名称： ')
                good_price = input('请输入商品定价： ')
                add_good(good_id, good_name, good_price, filename, filename1)
            else:
                break

    elif x == 2:
        old_id = input('请输入你想要删除的商品编号：')
        delete_good(old_id, filename)
        while True:
            print('是否继续删除商品： Y/N')
            choice = input()
            if choice == 'Y':
                old_id = input('请输入你想要删除的商品编号：')
                delete_good(old_id, filename)
            else:
                break
    else:
        print('暂时没有该功能！')

def buinese_sign():
    name = input('>>u ')
    if name not in buinese_name_list:
        print('管理用户不存在！')
    else:
        passward = input('>>p ')
        if passward == buinese_name_list[name]:
            print('登陆成功！')
            print_good_list()
            print('请选择你要执行的操作：')
            print('0 更改商品    1 添加商品    2 删除商品')
            choice = int(input())
            change_good_list(choice)
        else:
            print('你输入的密码不正确！')

def customer_system():
    print("请选择你要执行的操作：")
    print("0 登录，1 注册，2 退出登录")
    print('--------------------------------------')
    b = int(input())
    print('--------------------------------------')
    if b == 0:
        sign()
    elif b == 1:
        register()
    elif b == 2:
        while True:
            break
    else:
        print('暂时没有这项服务！')

def buinese_system():
    print("请选择你要执行的操作：")
    print("0 登录，1 退出登录")
    b = int(input())
    if b == 0:
        buinese_sign()
    elif b == 1:
        while True:
            break

def welcome_system():
    print('--------------------------------------')
    print("欢迎进入购物车界面！")
    print("请选择您的身份：0 顾客，1 商家")
    print('--------------------------------------')
    choice = input()
    print('--------------------------------------')
    choice = int(choice)
    if choice == 0:
        customer_system()
    else:
        buinese_system()

if __name__ == "__main__":
    initiazation()
    with open('all_good_lists.txt', 'r') as f_obj:
        for line in f_obj:
            line = line.strip()
            temp = line.split('|')
            temp[2] = int(temp[2])
            all_good_lists[temp[0]] = temp
    welcome_system()

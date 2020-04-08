#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import pymysql

host = "127.0.0.1"
user = "root"
password = ""
port = 3306
#后端库名
database1 = "loonflownew"
#前端库名
database2 = "shutongflow"
loonselect_sql = "SELECT username FROM account_loonuser;"
shutselect_sql = "SELECT username,password FROM user;"
looninsert_sql = "INSERT INTO account_loonuser(\
password,last_login,username,alias,email,phone,dept_id,is_active,is_admin,creator,gmt_created,\
gmt_modified,is_deleted,is_workflow_admin) VALUES ( \
  %s, '2020-04-05 14:10:33', %s, '', %s, \
  '', '0', '1', '0', '', '2020-04-05 13:51:38', '2020-04-05 14:10:32', '0', '0');"


def shutuser_select():
    conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database2)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(shutselect_sql)
    shutuser_dic_li = cursor.fetchall()
    cursor.close()
    conn.close()
    return shutuser_dic_li


def user_dic(loonuser_list):
    new_user_dic_li = []
    shutuser_dic_li = shutuser_select()  # type:list
    for shutuser in shutuser_dic_li:
        if shutuser["username"] not in loonuser_list:
            new_user_dic_li.append(shutuser)
    return new_user_dic_li


def loonuser_insert():
    conn = pymysql.connect(host=host, user=user, password=password, port=port, database=database1)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute(loonselect_sql)
    loonuser_dic_li = cursor.fetchall()
    loonuser_list = [i["username"] for i in loonuser_dic_li]
    new_user_dic_li = user_dic(loonuser_list)
    if new_user_dic_li:
        data = []
        for i in new_user_dic_li:
            email = "%s@qq.com" % i["username"]
            usertup = (i["password"], i["username"], email)
            data.append(usertup)
        cursor.executemany(looninsert_sql, data)
        conn.commit()
        cursor.close()
        conn.close()
        print("用户更新完成")
    else:
        print("没有用户同步")





if __name__ == '__main__':
    loonuser_insert()

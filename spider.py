import pymysql
import time
import traceback
import requests
import json

def get_conn():
    """
    :return:连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="localhost",
                           user="root",
                           db="cov",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def get_tencent_data():
    """
    :ruturn:返回历史数据和当日详细数据
    """
    # url="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)
    data_all = json.loads(res['data'])

    history = {}
    for i in data_all["chinaDayList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        dead = i["dead"]
        heal = i["heal"]
        # nowConfirm=i["nowConfirm"]
        # nowSevere=i["nowSevere"]
        deadRate = i["deadRate"]
        healRate = i["healRate"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
        # "nowConfirm":nowConfirm,"nowSevere":nowSevere,"deadRate":deadRate,"healRate":healRate}
    for i in data_all["chinaDayAddList"]:
        ds = "2020." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")
        ds = time.strftime("%Y-%m-%d", tup)
        confirm = i["confirm"]
        suspect = i["suspect"]
        dead = i["dead"]
        heal = i["heal"]
        deadRate = i["deadRate"]
        healRate = i["healRate"]
        history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})

    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    r1 = requests.get(url1, headers)
    res1 = json.loads(r1.text)
    data_all_details = json.loads(res1['data'])
    details = []
    updata_time = data_all_details["lastUpdateTime"]
    data_country = data_all_details["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]  # 省名
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            healRate = city_infos["total"]["healRate"]
            deadRate = city_infos["total"]["deadRate"]
            details.append([updata_time, province, city, confirm, confirm_add, heal, dead])
    return history, details


def get_foreign_data():
    """
    :ruturn:返回历史数据和当日详细数据
    """
    # url="https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    r = requests.get(url, headers)
    res = json.loads(r.text)
    data_all = json.loads(res['data'])

    foreign = {}
    for i in data_all["foreignList"]:
        update_time = "2020." + i["date"]
        tup = time.strptime(update_time, "%Y.%m.%d")
        update_time = time.strftime("%Y-%m-%d", tup)
        country = i["name"]
        confirm = i["confirm"]
        dead = i["dead"]
        foreign[country] = {"update_time": update_time, "confirm": confirm, "dead": dead}
    return foreign


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def update_details():
    """
    更新details表
    :return:
    """
    cursor=None
    conn=None
    try:
        li=get_tencent_data()[1]  #0历史数据字典  1最新详细数据
        conn,cursor=get_conn()
        sql="insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
        sql_query="select %s=(select update_time from details order by id desc limit 1)"
        cursor.execute(sql_query,li[0][0])
        if not cursor.fetchone()[0]:
            print(f"{time.asctime()}开始更新数据")
            for item in li:
                cursor.execute(sql,item)
            conn.commit()
            print(f"{time.asctime()}更新最新数据完毕")
        else:
            print(f"{time.asctime()}已是最新数据！")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn,cursor)


def update_foreign():
    cursor = None
    conn = None
    try:
        dic = get_foreign_data()
        # print(f"{time.asctime()}开始插入历史数据")
        conn, cursor = get_conn()
        sql = "update `foreign` set update_time=%s,confirm=%s,dead=%s where country=%s"
        sql_query = "select * from `foreign` where country=%s"
        sql1 = "insert into `foreign` values(%s,%s,%s,%s)"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql1, [k, v.get("update_time"), v.get("confirm"), v.get("dead")])

            if (cursor.execute(sql_query, k) != [k, v.get("update_time"), v.get("confirm"), v.get("dead")]):
                cursor.execute(sql, [v.get("update_time"), v.get("confirm"), v.get("dead"), k])

            else:
                print(f"{time.asctime()}已是最新数据！")

        conn.commit()
        print(f"{time.asctime()}插入wg数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def update_history():
    """
    更新历史数据
    :return:
    """
    cursor = None
    conn = None
    try:
        dic = get_tencent_data()[0]
        print(f"{time.asctime()}开始跟新历史数据")
        conn, cursor = get_conn()
        sql = "insert into history values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"),
                                     v.get("suspect"), v.get("suspect_add"),
                                     v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])

        conn.commit()
        print(f"{time.asctime()}更新历史数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)



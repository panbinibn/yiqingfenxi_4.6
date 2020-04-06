import time
import pymysql




def get_time():
        time_str = time.strftime("%Y{}%m{}%d{} %X")
        return time_str.format("年","月","日")

def query(sql,*args):
    """
    封装通用查询
    :parameter sql:
    :param args:
    :return:返回查询到的结果（（），（））形式
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_conn():
    """
    :return:连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="120.55.57.80",
                           user="zjh",
                           password="zjh",
                           db="yiqing_fenxi",
                           charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()

def get_c1_data():
    """
    :return:返回大屏c1数据
    """
    #取时间戳最新的一组数据
    #sql = "select sum(confirm)," \
    #    "(select suspect from history order by ds desc limit 1)," \
     #   "sum(heal)," \
     #   "sum(dead)" \
    #    "from details" \
     #   "where update_time=(select update_time from details order by update_time desc limit 1)"
    sql="select sum(confirm),(SELECT suspect FROM history ORDER BY ds DESC limit 1),sum(heal),sum(dead) from details where update_time=(select update_time from details order by update_time desc limit 1)"
    res = query(sql)
    return res[0]

def get_c2_data():
    """
    :return:各省数据
    """
    sql="select province,sum(confirm) from details "\
        "where update_time=(select update_time from details "\
        "order by update_time desc limit 1)" \
        "group by province"
    res = query(sql)
    return res

def get_l1_data():
    sql="select ds,confirm,suspect,heal,dead from history"
    res=query(sql)
    return res

def get_l2_data():
    sql="select ds,confirm_add,suspect_add from history"
    res=query(sql)
    return res

def get_r1_data():
    sql='select city,confirm from '\
        '(select city,confirm from details '\
        'where update_time=(select update_time from details order by update_time desc limit 1)'\
        'and province not in ("湖北","北京","上海","天津","重庆")' \
        'union all '\
        'select province as city,sum(confirm) as confirm from details '\
        'where update_time=(select update_time from details order by update_time desc limit 1)'\
        'and province in ("北京","上海","天津","重庆") group by province) as a '\
        'order by confirm desc limit 5'
    res=query(sql)
    return res

def get_r2_data():
    sql='select country,confirm,dead from `foreign` order by confirm desc limit 5'
    res=query(sql)
    return res

def get_all_data():
    sql=' select "中国" as country,sum(confirm) as confirm  from details UNION  SELECT country,confirm from `foreign`'
    #sql='select "中国" as country,sum(confirm) as confirm  from details '
    res=query(sql)
    return res

def get_form_data():
    sql='SELECT country,confirm,dead FROM `foreign`'
    #sql='select "中国" as country,sum(confirm) as confirm  from details '
    res=query(sql)
    return res


if __name__=="__main__":
    print(get_form_data())
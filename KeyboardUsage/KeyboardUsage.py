from pynput import keyboard
import sys
import MySQLdb
import datetime
import json
from PIL import Image

dict = {};
char_arr = [];

# 打开数据库，并返回一个数据库连接对象
def openMysqlConnection():
    conn = MySQLdb.connect('localhost', 'root', 'root', 'testdb', charset='utf8');
    print(conn)
    cursor = conn.cursor()
    cursor.close()
    return conn;

# 关闭数据库连接
def closeMysqlConnection(db):
    db.close()

# 保存键盘使用的数据
def saveUsageRecord():
    conn = openMysqlConnection()
    cursor = conn.cursor()
    now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    dictJson = json.dumps(dict)
    data = str(dictJson)
    sql = "INSERT keyboard_usage(recordData, createTime) VALUES (%s, %s)"
    print(sql)
    cursor.execute(sql,(data, now_date))
    cursor.close()
    conn.commit()
    closeMysqlConnection(conn)

# 退出键盘监听，并调用保存数据的方法
def exitListener(char_arr, keyStr):
    if(keyStr == 'pause'):
        saveUsageRecord()
        return False
    #if(keyStr == 'ctrl_l' and len(char_arr) == 0):
    #    char_arr.append(keyStr)
    #elif(len(char_arr) > 0 and len(char_arr) < 3 and char_arr[0] == 'ctrl_l'):
    #    char_arr.append(keyStr)
    #if(len(char_arr) == 3 and char_arr[0] == 'ctrl_l' and char_arr[1] == 'c' and char_arr[2] == 'd'):
    #    saveUsageRecord()
    #    return False
    #else:
    #    char_arr.clear()

# 键盘监听的主要方法
def on_press(key):
    try:
        if(dict.get(str(key.char)) == None):
            dict[str(key.char)] = 1
        else:
            dict[str(key.char)] += 1
        print(dict)
        isExit = exitListener(char_arr, key.char)
        if(isExit == False):
            return False
    except AttributeError:
        keyStr = str(key).split('.')[1]
        if(dict.get(keyStr) == None):
            dict[keyStr] = 1
        else:
            dict[keyStr] += 1
        print(dict)
        isExit = exitListener(char_arr, keyStr)
        if(isExit == False):
            return False

# 监听器的注册
listener = keyboard.Listener(on_press=on_press)

def main():
    listener.start()
    # 判断今天是否已经存有数据，如果有的话，则dict为今天数据
    # 如果没有，则dict保持为新对象
    conn = openMysqlConnection()
    cur = conn.cursor()
    now_date = datetime.datetime.now().strftime("%Y-%m-%d")
    sql = "select * from keyboard_usage where createTime = %s"
    cur.execute(sql, now_date)
    result = cur.fetchone()
    if(result != None):
        dict = result[2]
    conn.close()
    listener.join()
        
if __name__ == "__main__":
    main()




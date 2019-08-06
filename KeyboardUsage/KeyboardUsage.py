from pynput import keyboard
import sys
import MySQLdb

dict = {};
char_arr = [];

def on_press(key):
    try:
        global char_arr
        print(dict)
        print(char_arr)
        if(len(char_arr) < 3):
            char_arr.append(key.char)
        else:
            if(char_arr[0] == 'ctrl_l' and char_arr[1] == 'c' and char_arr[2] == 'd'):
                return False
            else:
                char_arr = []
        if(dict.get(str(key.char)) == None):
            dict[str(key.char)] = 1
        else:
            dict[str(key.char)] += 1
        print(dict)
    except AttributeError:
        keyStr = str(key).split('.')[1]
        if(len(char_arr) < 3):
            char_arr.append(keyStr)
        else:
            char_arr = []
        if(dict.get(keyStr) == None):
            dict[keyStr] = 1
        else:
            dict[keyStr] += 1
        if(key == key.esc):
            return False
        print(dict)

listener = keyboard.Listener(on_press=on_press)

def openMysqlConnection():
    conn = MySQLdb.connect('localhost', 'root', 'root', 'testdb', charset='utf8');
    print(conn)
    cursor = conn.cursor()
    cursor.close()
    return conn;

def closeMysqlConnection(db):
    db.close()

def main():
    listener.start()
    print("main run")
    conn = openMysqlConnection()
    cursor = conn.cursor()
    cursor.execute("select version()")
    result = cursor.fetchall();
    for item in result:
        print(item)
    listener.join()
        

if __name__ == "__main__":
    main()




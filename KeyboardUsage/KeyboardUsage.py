from pynput import keyboard
import sys
import MySQLdb

dict = {};


def on_press(key):
    try:
        if(dict.get(str(key.char)) == None):
            dict[str(key.char)] = 1
        else:
            dict[str(key.char)] += 1
        print(dict)
    except AttributeError:
        keyStr = str(key).split('.')[1]
        if(dict.get(keyStr) == None):
            dict[keyStr] = 1
        else:
            dict[keyStr] += 1
        if(key == key.esc):
            return False
        print(dict)

#def on_release(key):
#    print('{0} released'.format(key))

def openMysqlConnection():
    conn = MySQLdb.connect('localhost', 'root', 'root', 'sakila', charset='utf8');
    print(conn)
    cursor = conn.cursor()
    cursor.execute("select * from actor")
    result = cursor.fetchall();
    for item in result:
        print(item)
    cursor.close()
    return conn;

def closeMysqlConnection(db):
    db.close()

        
# #Collect events until released
#with keyboard.Listener(
#        on_press=on_press) as listener:
#    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(on_press=on_press)

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




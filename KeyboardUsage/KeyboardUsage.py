from pynput import keyboard
import MySQLdb

dict = {};

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
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
        if(key == key.ctrl_l and key == key.tab):
            return False
        print(dict)

def on_release(key):
    print('{0} released'.format(key))

def openMysqlConnection():
    db = MySQLdb.connect('localhost', 'root', 'root', 'testdb', charset='utf8');
    return db;

def closeMysqlConnection(db):
    db.close()

# Collect events until released
with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press)
listener.start()





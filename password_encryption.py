import pymysql, hashlib, os

def init():
    global conn, cursor
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='XXX', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("use test")
def close():
    global conn, cursor
    cursor.close()
    conn.close()

def generate_salt():
    return os.urandom(16).hex()
def hash_password(password, salt):
    return hashlib.sha256((password + salt).encode()).hexdigest()


def save_user(username, password):
    salt = generate_salt()
    hashed_password = hash_password(password, salt)

    init()
    cursor.execute("insert into user(name, pwd, salt) values (%s, %s, %s)", (username, hashed_password, salt))
    conn.commit()
    close()


def authenticate_user(username, password):
    init()
    cursor.execute("select pwd, salt from user where name = %s", username)
    result = cursor.fetchone()
    close()

    if result:
        stored_password = result['pwd']
        salt = result['salt']
        hashed_password = hashlib.sha256((password + salt).encode()).hexdigest()
        if stored_password == hashed_password:
            print("Authentication successful")
        else:
            print("Incorrect password")
    else:
        print("User not found")

if __name__ == "__main__":
    save_user("shaoyihao", "abc")
    authenticate_user("shaoyihao", "ab")
    authenticate_user("shaoyihao", "abc")

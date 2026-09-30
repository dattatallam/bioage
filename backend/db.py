import pymysql
from config import DB

_DB = dict(DB, cursorclass=pymysql.cursors.DictCursor)


def conn():
    return pymysql.connect(**_DB)

def init_db():
    with conn() as c, c.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(80) NOT NULL,
            email VARCHAR(120) NOT NULL UNIQUE, password_hash VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
        cur.execute("""CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY, user_id INT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, real_age INT NULL,
            predicted_age FLOAT NOT NULL, age_gap FLOAT NULL, inputs_filled INT NOT NULL,
            inputs JSON NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)""")
        c.commit()

def q(sql, args=(), one=False, commit=False):
    with conn() as c, c.cursor() as cur:
        cur.execute(sql, args)
        if commit:
            c.commit(); return cur.lastrowid
        return cur.fetchone() if one else cur.fetchall()


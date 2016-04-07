import sqlite3
from datetime import datetime


def _prepare_db(db_full_path):
    conn = sqlite3.connect(db_full_path)
    csr = conn.cursor()
    csr.execute("create table if not exists keywords(word text, category text, create_time text);CREATE UNIQUE INDEX idx_word_category ON keywords(word, category);")
    conn.commit()
    conn.close()


def _exists(word, category):
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    sql_search = 'select * from keywords where word like ? and category like ?' #here use like to avoid case sensitive
    cur.execute(sql_search, (word, category,))
    word_in_db = cur.fetchone()
    conn.close()
    return word_in_db is not None


def add_key_word(word, category):
    sql_add = 'insert into keywords(word, category, create_time) values (?,?,?)'
    if not _exists(word, category):
        conn = sqlite3.connect("data.db")
        cur = conn.cursor()
        cur.execute(sql_add, (word, category, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),))
        conn.commit()
        conn.close()


def get_related_words(word):
    word = word.strip()
    word.strip()
    sql = 'select word, category, create_time from  keywords where category like ? or word like ?'
    conn = sqlite3.connect("data.db")
    cur = conn.cursor()
    cur.execute(sql, (word, word, ))
    rows = []
    for row in cur.fetchall():
        rows.append({'word':row[0], 'category':row[1], 'create_time':row[2]})
    conn.close()
    return rows
    #cur.execute('insert into keywords(word, category, create_time) values (?,?,?)', ())
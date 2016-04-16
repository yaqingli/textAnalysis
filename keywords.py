import sqlite3
from datetime import datetime


class WordInfo:
    '''Word entity'''
    id = -1
    name = ''
    description = ''
    create_time = datetime.now()


class WordContext:
    '''
    Class wordsconnection is used to add data into sqlite db.
    '''
    #_dbName = 'data.db'
    _cursor = None


    def __init__(self, sqlite_connetion):
        '''
        initialize this class
        :param sqlite_connetion: sqlite3 connection
        :return:
        '''
        self._cursor = sqlite_connetion.cursor()

    def get_word_for_prompt(self, word, limit):
        '''
        Get words start with word
        :param word: word to search
        :param limit: start with
        :return:
        '''
        word = word.strip()
        sql = "select name from word where name like ? limit ?" #+str(int(limit)) # for safe
        csr = self._cursor
        csr.execute(sql, (word+'%', limit, ))
        rows = csr.fetchall()
        words_in_db = []
        for row in rows:
            words_in_db.append(row[0])
        return words_in_db


    def find_word(self, word):
        '''
        find the word in word table
        :param word: word name
        :return: word
        '''
        sql_exists_word = 'select id, name, description, create_time from word where name = ? COLLATE NOCASE'
        csr = self._cursor
        csr.execute(sql_exists_word, (word, ))
        row = csr.fetchone()
        word_in_db = None
        if row:
            word_in_db = {'id':row[0], 'name':row[1], 'description':row[2], 'create_time':row[3]}
        return word_in_db


    def get_related_words(self, word):
        word = word.strip()
        word_in_db = self.find_word(word)
        rows = []
        if word_in_db:
            sql = 'select id1, name1, id2, name2, create_time from  vw_keywords where id1 = ? or id2 = ?'
            #sql = 'select id1, id2, create_time from connection where id1 = ? or id2 = ?'
            csr = self._cursor
            csr.execute(sql, (word_in_db['id'], word_in_db['id'], ))
            for row in csr.fetchall():
                rows.append({'id1':row[0], 'word1':row[1], 'id2':row[2], 'word2':row[3], 'create_time':row[4]})
        return rows





    def find_or_add_word(self, word_info):
        '''
        Add word here, it should be json or dictionary
        :param word_info: {'name':'Hello', 'description':'This is only test'}
        '''
        id = None
        csr = self._cursor
        word_in_db = self.find_word(word_info['name'])
        if word_in_db:
            id = word_in_db['id']
        else:
            sql_add_word = 'insert into word(name, description, create_time) values (?,?,?)'
            csr.execute(sql_add_word, (word_info['name'], word_info['description'], '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),))
            id = csr.lastrowid
        return id


    def add_connection(self, connection):
        '''
        Add connected words
        :param connection: {'word1':'hello', 'word2':'world', 'direction':3, 'description':'this is description'}
        :return:
        '''
        id1 = self.find_or_add_word({'name':connection['word1'], 'description':''})
        id2 = self.find_or_add_word({'name':connection['word2'], 'description':''})
        id = self._find_or_add_connection(id1, id2, connection['direction'], connection['description'])
        return id




    def _find_or_add_connection(self, id1, id2, direction,description):
        id = None
        csr =self._cursor
        sql_search = 'select id, id1, id2, direction, description, create_time from connection where id1 = ? and id2 = ?' #here use like to avoid case sensitive
        csr.execute(sql_search, (id1, id2,))
        word_in_db = csr.fetchone()
        if word_in_db:
            id = word_in_db[0]
        else:
            sql_add_connection = 'insert into connection(id1, id2, direction, description, create_time) values (?, ?, ?, ?, ?)'
            csr.execute(sql_add_connection, (id1, id2, direction, description, '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),))
            id = csr.lastrowid
        return id





    def _prepare_db(db_full_path):
        conn = sqlite3.connect(db_full_path)
        csr = conn.cursor()
        csr.execute("create table if not exists keywords(word text, category text, create_time text);CREATE UNIQUE INDEX idx_word_category ON keywords(word, category);")
        conn.commit()
        conn.close()



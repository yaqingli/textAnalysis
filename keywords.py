import sqlite3
from datetime import datetime
from enum import Enum


#enums
class SearchDirection(Enum):
    down = 1
    up = 2

#Entities from webapp
class Connection_RTO(object):
    word1 = ''
    word2 = ''
    has_direction = False
    description = ''
    def __init__(self, word1, word2, has_direction, description):
        self.word1 = word1
        self.word2 = word2
        self.has_direction = has_direction
        self.description = description


#Entities for communication between db and code
class Entity(object):
    id = -1
    create_time = None
    update_time = None

    def __init__(self, id, create_time, update_time):
        self.id = id
        self.create_time = create_time
        self.update_time = update_time

    @classmethod
    def create_with_id(cls, id, create_time):
        now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        return cls(id, create_time, now)


class WordInfo(Entity):
    '''Word entity'''
    name = ''
    description = ''

    def __init__(self, id, name, description, create_time, update_time):
        Entity.__init__(self, id, create_time, update_time)
        self.name = name
        self.description = description

    @classmethod
    def create_with_content(cls, name, description):
        now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        return cls(-1, name, description, now, now)


class ConnectionInfo(Entity):
    id1 = -1
    id2 = -1
    has_direction = False
    description = ''
    def __init__(self, id, id1, id2, has_direction, description, create_time, update_time):
        Entity.__init__(self, id, create_time, update_time)
        self.id1 = id1
        self.id2 = id2
        self.has_direction = has_direction
        self.description = description

    @classmethod
    def create_with_content(cls, id1, id2, has_direction, description):
        now = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())
        return cls(-1, id1, id2, has_direction, description, now, now)


#context
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

    def find_words_by_ids(self, ids):
        '''
        find the words by id collection
        :param ids: id collection
        :return: WordInfo entities
        '''
        sql = 'select id, name, description, create_time, update_time from word where id in (%s)'%','.join('?'*len(ids))
        csr = self._cursor
        csr.execute(sql, ids)
        rows = csr.fetchall()
        words = [WordInfo(row[0], row[1], row[2], row[3], row[4]) for row in rows]
        return words

    def get_connections(self, word, down_level=3, up_level=1):
        '''
        Get related words
        :param word: string, word
        :return: connections
        '''
        word = word.strip()
        word_in_db = self._find_word(word)
        connections = []
        if word_in_db:
            connections.extend(self._get_connections(word_in_db.id, SearchDirection.down, down_level))
        return connections


    def add_connection(self, connection_rto):
        '''
        Add connected words
        :param connection: {'word1':'hello', 'word2':'world', 'has_direction':0, 'description':'this is description'}
        :return:
        '''
        id1 = self.find_or_add_word(WordInfo.create_with_content(connection_rto.word1, ''))
        id2 = self.find_or_add_word(WordInfo.create_with_content(connection_rto.word2, ''))
        id = self._find_or_add_connection(ConnectionInfo.create_with_content(id1, id2, connection_rto.has_direction, connection_rto.description))
        return id

    def find_or_add_word(self, word_info):
        '''
        Add word here, it should be type of WordInfo
        :param word_info: WordInfo
        '''
        id = None
        csr = self._cursor
        word_in_db = self._find_word(word_info.name)
        if word_in_db:
            id = word_in_db.id
        else:
            sql_add_word = 'insert into word(name, description, create_time, update_time) values (?,?,?,?)'
            now = Helper.get_current_time()
            csr.execute(sql_add_word, (word_info.name, word_info.description, now, now, ))
            id = csr.lastrowid
        return id

    #private parts
    def _find_word(self, word):
        '''
        find the word in word table
        :param word: word name
        :return: word
        '''
        sql_exists_word = 'select id, name, description, create_time, update_time from word where name = ? COLLATE NOCASE'
        csr = self._cursor
        csr.execute(sql_exists_word, (word, ))
        row = csr.fetchone()
        word_in_db = None
        if row:
            word_in_db = WordInfo(row[0], row[1], row[2], row[3], row[4])
        return word_in_db

    def _get_connections(self, id, search_direction, levels):
        '''
        Get the connections to a direction
        :param id:
        :param search_direction:
        :param levels: minimal 1
        :return:
        '''
        csr = self._cursor
        ancestor_id_collection = []
        id_collection = [id]
        connections = []
        for i in range(levels):
            if search_direction == SearchDirection.down and len(id_collection)>0:
                sql = 'select id, id1, id2, has_direction,description, create_time, update_time from connection where has_direction = 1 and id2 in (%s)'%','.join('?'*len(id_collection))
                csr.execute(sql, id_collection)
                rows = csr.fetchall()
                if len(rows) > 0:
                    temp_connections = [ConnectionInfo(row[0], row[1], row[2], row[3], row[4], row[5], row[6]) for row in rows]
                    connections.extend(temp_connections)
                    id_collection = [c.id1 for c in temp_connections if c.id1 not in ancestor_id_collection]
                    ancestor_id_collection.extend(id_collection)
                    print(id_collection)
                    if not id_collection:
                        break
                else:
                    break
        return connections


    def _find_or_add_connection(self, connection_info):
        id = None
        csr =self._cursor
        sql_search = 'select id, id1, id2, has_direction, description, create_time from connection where id1 = ? and id2 = ?' #here use like to avoid case sensitive
        csr.execute(sql_search, (connection_info.id1, connection_info.id2,))
        word_in_db = csr.fetchone()
        if word_in_db:
            id = word_in_db[0]
        else:
            sql_add_connection = 'insert into connection(id1, id2, has_direction, description, create_time, update_time) values (?, ?, ?, ?, ?, ?)'
            now = Helper.get_current_time()
            csr.execute(sql_add_connection, (connection_info.id1, connection_info.id2, connection_info.has_direction, connection_info.description, now, now, ))
            id = csr.lastrowid
        return id


class Helper:
    @staticmethod
    def _prepare_db(db_full_path):
        conn = sqlite3.connect(db_full_path)
        csr = conn.cursor()
        csr.execute("create table if not exists keywords(word text, category text, create_time text);CREATE UNIQUE INDEX idx_word_category ON keywords(word, category);")
        conn.commit()
        conn.close()

    @staticmethod
    def get_current_time():
        return '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now())

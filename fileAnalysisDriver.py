
from datetime import datetime


import pymongo
#from mysql import connector
import ntpath
import pathAnalysis

#C:\Users\billi\OneDrive\Library\ITKnowledge\Python\python_tutorial.pdf


def analyze_files(path):
    file_paths = pathAnalysis.get_path_info(path)
    print(len(file_paths))
    file_paths = [path['full_path'] for path in file_paths if path['isfile'] and path['file_extension']=='pdf']
    print(len(file_paths))
    with pymongo.MongoClient("localhost", 27017) as client:
        for file_path in file_paths:
            print(file_path)
            try:
                t1 = datetime.now()
                content = to_text(file_path)
                duration = (datetime.now() - t1).seconds
                log_document(client, file_path, content, 'pdf', duration)
            except Exception as e:
                if client:
                    log_document(client, file_path, str(e), 'pdf', 0)
                print(e)


def log_document(mongo_client, file_path, content, file_type, duration):
    '''
    log the parsed doc
    :param file_path: file path
    :param content: content parsed from file
    :param file_type: file type, can be pdf, txt
    :return:
    '''
    db = mongo_client.dbFilesAnalysis
    db.tblFiles.insert_one({'file_path' : file_path, 'content' : content, 'file_type': file_type, 'duration':duration,'insert_time_utc':datetime.utcnow()})
    mongo_client.close()

#count the data with Counter


def test_count_wors():
    txt = 'Python programming — text and web mining\n\nFinn'
    result = count_words(txt)
    assert(len(result)==7)

#Storage part

#store the words and count into database
#data is a collection
#data: {{'fileid':1, 'word':'is', 'count':10, 'create_time':'2016-04-02 16:57:29.558867'},{'fileid':1, 'word':'are', 'count':5, 'create_time':'2016-04-02 16:57:29.558868'}}
def write_words_statistics_to_db(data):
    cnx = connector.connect(user='python', password='123456',
                              host='127.0.0.1',
                              database='words')
    add_word_sql = "INSERT INTO words_count(FileId, word, count, create_time) VALUES (%(fileid)s, %(word)s, %(count)s, %(create_time)s)"
    cursor = cnx.cursor()
    for item in data:
        cursor.execute(add_word_sql,item)
    cnx.commit()
    cursor.close()
    cnx.close

#get filename from file_path
def add_file_to_db(file_path):
    head, tail = ntpath.split(file_path)
    add_file_sql = 'insert into file(name, full_path, create_time) values (%s, %s, %s)'
    fileid = 0
    try:
        cnx = connector.connect(user='python', password='123456',host='127.0.0.1',database='words')
        cursor = cnx.cursor()
        cursor.execute(add_file_sql, (tail, file_path, '{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.now())))
        fileid = cursor.lastrowid
        cursor.close()
        cnx.commit()
    except Exception as e:
        raise e
    finally:
        if cnx.is_connected():
            cnx.close
    return fileid


def _get_file_id(file_path):
    get_file_sql = """SELECT Id FROM File WHERE full_path = %s"""
    fileid = None
    try:
        cnx = connector.connect(user='python', password='123456',host='127.0.0.1',database='words')
        cursor = cnx.cursor()
        cursor.execute(get_file_sql, (file_path,))
        single_line = cursor.fetchone()
        if single_line:
            fileid = single_line[0]
        cursor.close() #make sure there is only one item in it
    except Exception as e:
        raise e
    finally:
        if cnx.is_connected():
            cnx.close()
    return fileid


def try_add_file_to_db(file_path):
    fileid = _get_file_id(file_path)
    if not fileid:
        fileid = add_file_to_db(file_path)
    return fileid


#analyze file and write them into database
def analyze_file(file_path):
    fileid = try_add_file_to_db(file_path)
    txt = to_text(file_path)
    words_count = count_words(txt)
    data = []
    for key, value in words_count.items():
        data.append({'fileid':fileid, 'word':key, 'count':value, 'create_time':'{:%Y-%m-%d %H:%M:%S.%f}'.format(datetime.now())})
    write_words_statistics_to_db(data)

if __name__ == "__main__":
    file_path = r'D:\MyFiles\baiduyun\ITKnowledge\BI\DataWarehouse\Case Study A Data Warehouse for an Academic Medical Center.pdf'
    to_text(file_path)
    a = 'adda'
    a.split()
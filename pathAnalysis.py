from os import listdir
from os.path import join, isdir, isfile, getsize
import sqlite3


def get_path_info(root):
    files = []
    total_size = 0
    for file_name in listdir(root):
        file_full_path = join(root, file_name)
        if isfile(file_full_path):
            files.append({'full_path':file_full_path, 'parent_path_name':root,'tail_name':file_name, 'isfile':True,'file_size':getsize(file_full_path)})
            total_size += getsize(file_full_path)
        elif isdir(file_full_path):
            (child_files, child_size) = get_path_info(file_full_path)
            files = files + child_files
            total_size += child_size
            files.append({'full_path':file_full_path, 'parent_path_name':root,'tail_name':file_name, 'isfile':False, 'file_size':child_size})
    return files, total_size


def create_sqlitedb():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    sql_create_table = 'create table file_info(full_path text, parent_path_name text, tail_name text, isfile int, file_size real)'
    c.execute(sql_create_table)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    paths, total_size = get_path_info(r"C:\Users\billi\OneDrive\Library\ITKnowledge")#(r"C:\Python")
    conn = sqlite3.connect('example.db')
    c = conn.cursor()
    sql_insert = 'insert into file_info(full_path, parent_path_name, tail_name, isfile, file_size) values (?, ?, ?, ?, ?)'
    c.executemany(sql_insert, [(path['full_path'], path['parent_path_name'], path['tail_name'], path['isfile'], path['file_size']/1024/1024) for path in paths])
    conn.commit()
    conn.close()
    #for path in paths:
    #print(path['full_path'], path['parent_path_name'], path['tail_name'], path['isfile'], path['file_size'])
from bottle import route, run, template, static_file,request, view
import json
from keywords import WordContext
import sqlite3
from collections import defaultdict


_dbName = 'data.db'


#todo: Research where to implement the add function
#todo: Research where to implement the update function

@route('/test/template')
@view('testtml')
def test():
    return {'name':'Bill'}


#new version here
@route('/')
@route('/search')
@route('/search/')
def search_view():
    return template('thewords.html', request=request)

@route('/search/searchWordStartWith')
def searchWordStartWith():
    word = request.params.get('word', '', type=str)
    if word:
        conn = sqlite3.connect(_dbName)
        k = WordContext(conn)
        words = k.get_word_for_prompt(word, 10)
        conn.close()
        return json.dumps({'words':words})
    else:
        return json.dumps({'words':[]})


@route('/search/related/')
@route('/search/related')
def searchRelated():
    word = request.params.get('word', '', type=str)
    conn = sqlite3.connect(_dbName)
    k = WordContext(conn)
    related_words = k.get_related_words(word)
    conn.close()
    wordsDict = defaultdict()
    for item in related_words:
        wordsDict[item['id1']] = item['word1']
        wordsDict[item['id2']] = item['word2']
    words = [{'id': k, 'name': v} for (k, v) in wordsDict.items()]
    return json.dumps({'related_words':related_words, 'words':words})

#add word in a page
@route('/addwordbycategory')
def add_word_by_category_view():
    return template('addwords_by_category.html', {'categories': ''})


@route('/addwordbycategory', method="post")
@view('addwords_by_category.html')
def add_words():
    words = request.params.get('words').strip().strip('\t').rstrip(';')
    categories = request.params.get('categories').strip().strip('\t').rstrip(';')
    word_collection = [word.strip() for word in words.split(';')]
    category_collection = [category.strip() for category in categories.split(';')]
    with sqlite3.connect(_dbName) as conn:
        wc = WordContext(conn)
        for word in word_collection:
            for category in category_collection:
                wc.add_connection({'word1':word, 'word2':category, 'direction': 2, 'description':''})

    return {'categories': categories}


run(host='localhost', port=8080)
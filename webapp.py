from bottle import route, run, template, static_file,request, view
import keywords


@route('/keywords/search/')
@route('/keywords/search/<category>')
@view('keywords.tpl')
def search(category=''):
    result = {'words':[]}
    category_in_form = request.params.get('category')
    if category_in_form:
        category = category_in_form
    if category:
        result['words'] = keywords.get_related_words(category)
    result['category'] = category
        #content = '</br>'.join([','.join((wordline['word'],wordline['category'],wordline['create_time'])) for wordline in words])
    return result
    #return template('<b>Hello {{name}}</b>!', name=name)


@route('/keywords/addword')
@view('addwords.html')
def add_word_view():
    return {'categories': ''}


@route('/keywords/addword', method="post")
@view('addwords.html')
def add_words():
    words = request.params.get('word').strip().strip('\t').rstrip(';')
    categories = request.params.get('category').strip().strip('\t').rstrip(';')
    word_collection = [word.strip() for word in words.split(';')]
    category_collection = [category.strip() for category in categories.split(';')]
    for word in word_collection:
        for category in category_collection:
            keywords.add_key_word(word, category)
    return {'categories': categories}


@route('/test/template')
@view('testtml')
def test():
    return {'name':'Bill'}





run(host='localhost', port=8080)
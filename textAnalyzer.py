from collections import Counter
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
'''
Implement text related analysis functionality
'''

class Node(object):
    children = []
    parent = None
    value = None

    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None

    def add_child(self, node):
        self.children.append(node)
        node.parent = self
        return node

    def get_ancestor(self, level = 1):
        node = self
        for i in range(level):
            node = node.parent
        return node


def getTree(s, indent):
    '''
    Analyze the data
    :param s:
    :return:
    '''
    root = None
    current_node = None
    last_indent = 0
    for item in s.split('\n'):
        current_indent = countIndent(item, indent)
        item_content = item.lstrip(indent)
        if current_indent - last_indent <= 0:
            if not current_node:
                current_node = Node(item_content)
                root = current_node
            else:
                current_node = current_node.get_ancestor(last_indent-current_indent+1).add_child(Node(item_content))
        else:
            current_node = current_node.add_child(Node(item_content))
        last_indent  = current_indent
    return root


def countIndent(txt, indent):
    count = 0
    for c in txt:
        if c == indent:
            count += 1
        else:
            break
    return count


def count_words(text):
    '''count the words'''
    #seperates = ['\n', ' ', ',' ,'\x0c', '—']
    #ignore_words = ('the', 'a')
    result = Counter()
    temp = ''
    for c in text:
        if ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
            temp += c.lower()
        else:
            if temp:
                result[temp] += 1
                temp = ''

    #last word
    if temp:
        result[temp] += 1
        temp = ''

    return result


def get_pdf_file_content(file_path):
        '''Read words from a pdf file'''
        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)
        page_count = 0

        with open(file_path, 'rb') as fp:
            for page in PDFPage.get_pages(fp):
                interpreter.process_page(page)
                page_count += 1

        converter.close()
        text = output.getvalue()
        output.close()
        return text, page_count

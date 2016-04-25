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
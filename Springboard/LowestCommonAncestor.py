'''
class Node:
    def __init__(self, info):
        self.info = info
        self.left = None
        self.right = None

    // this is a
    node
    of
    the
    tree, which
    contains
    info as data, left, right


'''

def lca(root, v1, v2):
  #Enter your code here
    if (root.info < v1 and root.info > v2) or (root.info > v1 and root.info < v2):
        return root
    elif root.info < v1 and root.info < v2:
        return lca(root.right, v1, v2)
    elif root.info > v1 and root.info > v2:
        return lca(root.left, v1, v2)
    elif root.info == v1 or root.info == v2:
        return root


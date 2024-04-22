class node:
    def __init__(self,value=None):
        self.value=value
        self.left_child=None
        self.right_child=None

class BinarySearchTree:
    def __init__(self):
        self.root=None

    def insert(self,value):
        if self.root==None:
            self.root=node(value)
        else:
            self._insert(value,self.root)

    def _insert(self,value,cur_node):
        if value<cur_node.value:
            if cur_node.left_child==None:
                cur_node.left_child=node(value)
            else:
                self._insert(value,cur_node.left_child)
        elif value>cur_node.value:
            if cur_node.right_child==None:
                cur_node.right_child=node(value)
            else:
                self._insert(value,cur_node.right_child)
        else:
            print('Value already in tree!')

    def print_tree(self):
        if self.root!=None:
            self._print_tree(self.root)


    def _print_tree(self,cur_node):
        if cur_node!=None:
            self._print_tree(cur_node.left_child)
            print(str(cur_node.value))
            self._print_tree(cur_node.right_child)

def fill_tree(tre,num_elems=100,max_int=1000):
    from random import randint
    for cur_elem in [10, 30,20,25]:

        tre.insert(cur_elem)
    return tre

tree=BinarySearchTree()
tree=fill_tree(tree)
tree.print_tree()
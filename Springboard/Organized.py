class TreeNode:
    def __init__(self,name):
        self.name=name
        self.children=[]
        self.parent=None

    def add_child(self,value):
        value.parent=self
        self.children.append(value)
    def _level(self,max_level):
        i=1
        l=self.parent
        while l!=None:
            i+=1
            l=l.parent
        return i

    def prt(self,max_level):
        n=self._level(max_level)
        if n<=max_level:
            print(' '*2*n+'|'+'__'+self.name)
        for child in self.children:
            child.prt(max_level)


root = TreeNode("Global")

india = TreeNode("India")

gujarat = TreeNode("Gujarat")
gujarat.add_child(TreeNode("Ahmedabad"))
gujarat.add_child(TreeNode("Baroda"))

karnataka = TreeNode("Karnataka")
karnataka.add_child(TreeNode("Bangluru"))
karnataka.add_child(TreeNode("Mysore"))

india.add_child(gujarat)
india.add_child(karnataka)

usa = TreeNode("USA")

nj = TreeNode("New Jersey")
nj.add_child(TreeNode("Princeton"))
nj.add_child(TreeNode("Trenton"))

california = TreeNode("California")
california.add_child(TreeNode("San Francisco"))
california.add_child(TreeNode("Mountain View"))
california.add_child(TreeNode("Palo Alto"))

usa.add_child(nj)
usa.add_child(california)

root.add_child(india)
root.add_child(usa)

root.prt(1)
print('\n')
root.prt(2)
print('\n')
root.prt(3)
print('\n')
root.prt(4)
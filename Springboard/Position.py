class TreeNode:
    def __init__(self,data,position):
        self.data=data
        self.position=position
        self.children=[]
        self.parent=None

    def add_child(self,child):
        child.parent=self
        self.children.append(child)

    def level(self):
        i=1
        p=self.parent
        while p!=None:
            i+=1
            p=p.parent
        return i

    def print_tree(self,stat):
        if stat==1:
            prt=self.data+'->'+self.position
        elif stat==2:
            prt=self.data
        else:
            prt=self.position
        n=self.level()
        print(' '*2*n+'|'+'__'+prt)
        for child in self.children:
            child.print_tree(stat)

infra_head = TreeNode("Vishwa","Infrastructure Head")
infra_head.add_child(TreeNode("Dhaval","Cloud Manager"))
infra_head.add_child(TreeNode("Abhijit", "App Manager"))

cto = TreeNode("Chinmay", "CTO")
cto.add_child(infra_head)
cto.add_child(TreeNode("Aamir", "Application Head"))

# HR hierarchy
hr_head = TreeNode("Gels","HR Head")

hr_head.add_child(TreeNode("Peter","Recruitment Manager"))
hr_head.add_child(TreeNode("Waqas", "Policy Manager"))

ceo = TreeNode("Nilupul", "CEO")
ceo.add_child(cto)
ceo.add_child(hr_head)

ceo.print_tree(1)
print('\n')
ceo.print_tree(2)
print('\n')
ceo.print_tree(3)
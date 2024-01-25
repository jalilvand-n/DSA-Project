def LANMAN(input_str):
    output = 0
    input_bytes = input_str.encode('utf-16le')
    for i in range(0, len(input_bytes), 2):
        output += (input_bytes[i] | (input_bytes[i + 1] << 8))
    return output

class Person:
    def __init__ (self, name):
        self.name = LANMAN(name)
        self.realname = name
        self.parent = None
        self.Height=0
        #self.Depth=0
        self.farthestchild=None
def set_parents(parent,child):
    child.parent=parent
    if child.Height+1>parent.Height:
        parent.Height=child.Height+1
        T=parent
        while T.parent!=None:
            pre_T=T
            T=T.parent
            T.parent.Height=pre_T+1
        if child.farthestchild==None:
            parent.farthestchild=child
        else:
            parent.farthestchild=child.farthestchild
   # parent.num=max(child.num+1,parent.num)
def Depth(p1):
    T=p1
    count=int(0)
    while T.parent!=None:
        T=T.parent
        count+=1
    return count
def check_parents(p1,p2):
    if p1.parent==None:
        return False
    elif p1.parent==p2:
        return True
    elif check_parents(p1.parent,p2)==True:
        return True
def check_brothers(p1,p2):
    if p1.parent==p2.parent:
        return True
    else:
        return False
def common_ancestor(p1,p2):
    D1=Depth(p1)
    D2=Depth(p2)
    if D1>D2:
        while D2!=Depth(p1):
            p1=p1.parent
    elif D2<D1:
        while Depth(p2)!=D1:
            p2=p2.parent
    while p1.name!=p2.name:
        p1=p1.parent
        p2=p2.parent
    print(p1.realname)
    return p1.name
def check_cousins(p1,p2):
    if(check_brothers(p1,p2)==False and check_parents(p1,p2)==False and check_parents(p2,p1)==False):
        return True
    else:
        return False
def farthest_child(p):
    return p.Height
sara=Person("Sara")
mother=Person("Mother")
grandmother=Person("GrandMather")
aunt=Person("Aunt")
jo=Person("Jo")
lona=Person("Lona")
baby=Person("Baby")
set_parents(lona,baby)
set_parents(mother,sara)
set_parents(aunt,jo)
set_parents(aunt,lona)
set_parents(grandmother,mother)
set_parents(grandmother,aunt)
print(sara.Height)
common_ancestor(baby,jo)
print(aunt.farthestchild.realname)

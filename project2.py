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
        self.num=0
        # self.children = [LANMAN(i) for i in children]
def set_parents(parent,child):
    child.parent=parent
    parent.num=child.num+1
    T=parent
    while T.parent!=None:
        T=T.parent
        T.parent.num+=1
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
    if p1.num>p2.num:
        while p2.num!=p1.num:
            p2=p2.parent
    elif p2.num>p1.num:
        while p2.num!=p1.num:
            p1=p1.parent
    while p1.name!=p2.name:
        p1=p1.parent
        p2=p2.parent
    print(p1.realname)
    return p1.name
sara=Person("Sara")
mother=Person("Mother")
grandmother=Person("GrandMather")
set_parents(mother,sara)
set_parents(grandmother,mother)
common_ancestor(sara,mother)

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
        # self.children = [LANMAN(i) for i in children]
def check_parents(p1,p2):
    if p1.parent==None:
        return False
    elif p1.parent==p2:
        return True
    elif check_parents(p1.parent,p2)==True:
        return True
sara=Person("Sara")
mother=Person("Mother")
grandmother=Person("GrandMather")
sara.parent=mother
mother.parent=grandmother
T=sara
while(T.parent!=None):
    print(T.parent.name)
    T=T.parent
print(check_parents(sara,grandmother))
print(check_parents(grandmother,sara))


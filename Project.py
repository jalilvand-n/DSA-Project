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
        self.children = []
class Family:
    def __init__(self):
        self.family = {}
    def Add(self, person):
        if person not in self.family:
            self.family[person] = Person(person)
    def Del(self, person):
        if person in self.family:
            self.family[person] = None
        else:
            print("This person is not in family.")
    def Find(self, person):
        if person in self.family.values():
            return person.name
        else:
            print("This person is not in family.")
    def Size(self):
        return len(self.family)
    def find_farthest_relation(self):
        farthest = None
        max_distance = -1
        for person in self.family.values():
            for other in self.family.values():
                if person != other:
                    distance = self._find_distance(person, other)
                    if distance > max_distance:
                        max_distance = distance
                        farthest = (person, other)
        return farthest

    def _find_distance(self, person1, person2):
        queue = [(person1, 0)]
        visited = set()
        while queue:
            current, dist = queue.pop(0)
            if current == person2:
                return dist
            visited.add(current)
            for neighbor in current.parents + current.children:
                if neighbor not in visited:
                    queue.append((neighbor, dist + 1))
        return -1
def set_parents(parent,child):
    parent.children.append(child)
    child.parent=parent
    child.num=parent.num+1
def check_parents(p1,p2):
    if p1.parent==None:
        return False
    elif p1.parent==p2:
        return True
    elif check_parents(p1.parent,p2)==True:
        return True
def check_sibling(p1,p2):
    if p1.parent==p2.parent:
        return True
    else:
        return False
Chelchele = Family()
while True:
    print("Enter")
    print('1 to make a new family')
    print("2 to add member to current family")
    print("3 to delete member from current family")
    print("4 to find a member of current family")
    print("5 to get the size of current family")
    print("6 to check parent-child relationship")
    print("7 to check sibling relationship")
    print("8 to check distant relationship")
    print("9 to find common ancestor")
    print("10 to find the farthest born")
    print("11 to find the most distant relationship")
    print("0 to exit")
    n = input()
    if n == 1:
        Chelchele.root= LANMAN(input("Enter root's name: "))
        Chelchele.Add(Chelchele.root)
    elif n == 2:
        if(Chelchele.root == None):
            print("Please make a family first!")
            break
        else:
            p = input("Enter the name of new member: ")
            Chelchele.Add(input("Enter the name of new member: "))
            set_parents(Person(input("Enter parent name: ")), p)
    elif n == 3:
        Chelchele.Del(input("Enter the name: "))      
    elif n == 4:
        Chelchele.Find(input("Enter the name:"))
    elif n == 5:
        Chelchele.Size()
    elif n == 6:
        check_parents(input("Enter the child name: "), input("Enter the parent name: "))
    elif n == 7:
        check_sibling(input("Enter the first name: "), input("Enter the second name: "))
    elif n == 11:
        Chelchele.find_farthest_relation()
    elif n == 0:
        break

sara=Person("Sara")
mother=Person("Mother")
grandmother=Person("GrandMather")
set_parents(mother,sara)
set_parents(grandmother,mother)
T=sara
while(T.parent!=None):
    print(T.parent.name)
    T=T.parent
print(check_parents(sara,grandmother))
print(check_parents(grandmother,sara))
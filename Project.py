import struct
import math


def left_rotate(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def md5(message):
    message = message.encode()
    T = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
    s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + \
        [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    original_length = len(message)
    bit_length = original_length * 8
    message += b'\x80'
    message += b'\x00' * ((56 - (original_length + 1) % 64) % 64)
    message += struct.pack('<Q', bit_length)

    # Process the message in 16-word blocks
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]

        # Initialize hash value for this chunk
        aa = a
        bb = b
        cc = c
        dd = d

        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16

            # Perform the operation
            temp = d
            d = c
            c = b
            b = b + \
                left_rotate(
                    (a + f + T[j] + struct.unpack('<I', chunk[g*4:g*4+4])[0]), s[j])
            a = temp

        # Update the hash values
        a = (a + aa) & 0xFFFFFFFF
        b = (b + bb) & 0xFFFFFFFF
        c = (c + cc) & 0xFFFFFFFF
        d = (d + dd) & 0xFFFFFFFF
    return struct.pack('<I', a) + struct.pack('<I', b) + struct.pack('<I', c) + struct.pack('<I', d)


class Person:
    def __init__(self, name):
        self.name = md5(name).hex()
        self.realname = name
        self.parent = None
        self.Height = 0
        self.children = []
        self.farthestchild = None


class Family:
    def __init__(self):
        self.family = {}

    def Add(self, person):
        if person not in self.family.keys():
            self.family[person] = Person(person)

    def Del(self, person):
        if person in self.family.keys():
            self.family[person] = None
        else:
            print("This person is not in family.")

    def Find(self, person):
        if person in self.family.keys():
            print(self.family[person].name)
            return self.family[person].name
        else:
            print("This person is not in family.")

    def Size(self):
        print(len(self.family))
        return len(self.family)
    
    def set_parents(self, parent, child):
        self.family[child].parent = self.family[parent]
        if self.family[child].Height+1 > self.family[parent].Height:
            self.family[parent].Height = self.family[child].Height+1
            T = self.family[parent]
            while T.parent != None:
                pre_T = T
                T = T.parent
                T.Height = pre_T.Height+1
            if self.family[child].farthestchild == None:
                self.family[parent].farthestchild = self.family[child]
            else:
                self.family[parent].farthestchild = self.family[child].farthestchild

    def Depth(self, person):
        T = self.family[person]
        count = int(0)
        while T.parent != None:
            T = T.parent
            count += 1
        return count

    def check_parents(self, person1, person2):
        if person1 not in self.family.keys():
            print("The child is not in family.")
            return False
        if person2 not in self.family.keys():
            print("The parent is not in family.")
            return False
        if self.family[person1].parent == None:
            print(self.family[person1].name, "is not the parent of", self.family[person2].name)
            return False
        elif self.family[person1].parent == self.family[person2]:
            print(self.family[person1].name, "is the parent of", self.family[person2].name)
            return True
        elif self.check_parents(self.family[person1].parent, self.family[person2]) == True:
            print(self.family[person1].name, "is the parent of", self.family[person2].name)
            return True

    def check_sibling(self, person1, person2):
        if person1 not in self.family.keys():
            print("The first person is not in family.")
            return False
        if person2 not in self.family.keys():
            print("The second person is not in family.")
            return False
        if self.family[person1].parent == self.family[person2].parent:
            print("They are siblings")
            return True
        else:
            print("They are not siblings")
            return False

    def check_distant_relationship(self, person1, person2):
        if person1 not in self.family.keys():
            print("The first person is not in family.")
            return False
        if person2 not in self.family.keys():
            print("The second person is not in family.")
            return False
        if (self.check_sibling(person1, person2) == False and self.check_parents(person1, person2) == False and self.check_parents(person2, person1) == False):
            print("They are distantly related")
            return True
        else:
            print("They are not distantly related")
            return False

    def common_ancestor(self, person1, person2):
        if person1 not in self.family.keys():
            print("The first person is not in family.")
            return 
        if person2 not in self.family.keys():
            print("The second person is not in family.")
            return 
        D1 = self.Depth(person1)
        D2 = self.Depth(person2)
        if D1 > D2:
            while D2 != D1:
                self.family[person1] = self.family[person1].parent
                D1-=1
        elif D2 > D1:
            while D2 != D1:
                self.family[person2] = self.family[person2].parent
                D2 -= 1
        while self.family[person1].name != self.family[person2].name:
            self.family[person1] = self.family[person1].parent
            self.family[person2] = self.family[person2].parent
        print(self.family[person1].name)
        return self.family[person1].name

    def find_farthest_relation(self):
        distances = {} 

        for member in self.family.values():
            if member.parent is None:
                distances[member.name] = 0
            else:
                distances[member.name] = distances[member.parent.name] + 1

        farthest_members = max(distances, key=distances.get)
        farthest_distance = distances[farthest_members]

        second_farthest_members = []
        second_farthest_distance = farthest_distance - 1
        for member, distance in distances.items():
            if distance == second_farthest_distance:
                second_farthest_members.append(member)

        return farthest_members, second_farthest_members


Chelchele = Family()


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
while True:
    n = input("Please enter your choice: ")
    if n == "1":
        Chelchele.Add((input("Enter the name of ancestor: ")))
    elif n == "2":
        if (Chelchele.family == None):
            print("Please make a family first!")
            break
        else:
            person1 = input("Enter the name of child: ")
            Chelchele.Add(person1)
            parent=input("Enter the name of parent: ")
            Chelchele.Add(parent)
            Chelchele.set_parents(parent, person1)
    elif n == "3":
        Chelchele.Del(input("Enter the name: "))
    elif n == "4":
        Chelchele.Find(input("Enter the name:"))
    elif n == "5":
        Chelchele.Size()
    elif n == "6":
        Chelchele.check_parents(input("Enter the child name: "),input("Enter the parent name: "))
    elif n == "7":
        Chelchele.check_sibling(
            input("Enter the first name: "), input("Enter the second name: "))
    elif n == "8":
        Chelchele.check_distant_relationship(
            input("Enter the first name: "), input("Enter the second name: "))
    elif n == "9":
        Chelchele.common_ancestor(
            input("Enter the first name: "), input("Enter the second name: "))
    elif n == "10":
        Chelchele.farthest_born(
            input("Enter the name: "))
    elif n == "11":
        print(Chelchele.find_farthest_relation())
    elif n == "0":
        print("Thank you")
        print("We hope you enjoyed meeting the mysterious Chelchele family [^-^]")
        break

import numpy as np

NameToKey = {'Refle': 1, 'Abs': 2, 'Scatt': 3}
AbsCoeffs = {'Concrete': [0.02,0.02,0.03,0.03,0.04,0.05,0.05], 
              'AbsPanels': [0.15,0.7,0.9,0.6,0.85,0.9,0.9],
              'Door': [0.14,0.10,0.06,0.08,0.10,0.10,0.10]}
ScattCoeffs = {'Concrete': [0.30,0.50,0.60,0.60,0.70,0.70,0.70], 
              'AbsPanels': [0.20,0.40,0.50,0.50,0.60,0.60,0.60],
              'Door': [0.20,0.40,0.50,0.50,0.60,0.60,0.60]}
room_dim = [4.0, 3.4, 6.0]
PanelSize = [0.3,1.33]

def PanelsToChange(Current_RT60, Needed_RT60, room_dim):
    V = np.prod(room_dim)
    Panel_Surface = np.prod(PanelSize)
    Current_Abs = 0.161*V/Current_RT60
    Needed_Abs = 0.161*V/Needed_RT60
    AbsFromSinglePanel = Panel_Surface*(AbsCoeffs['AbsPanels'][2]-AbsCoeffs['Concrete'][2])
    PanelsToChange = (Needed_Abs-Current_Abs)//AbsFromSinglePanel
    return PanelsToChange

class Node:
    def __init__(self, data, position):
        self.Type = data
        self.Position = position
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insertAtBegin(self, data, position):
        new_node = Node(data, position)
        if self.head is None:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node

    def insertAtEnd(self, data, position):
        new_node = Node(data, position)
        if self.head is None:
            self.head = new_node
            return
 
        current_node = self.head
        while(current_node.next):
            current_node = current_node.next
 
        current_node.next = new_node

    def updateNode(self, val, index):
        current_node = self.head
        position = 0
        if position == index:
            current_node.Type = val
        else:
            while(current_node != None and position != index):
                position = position+1
                current_node = current_node.next
 
            if current_node != None:
                current_node.Type = val
            else:
                print("Index not present")

    def returnAtIndex(self,index):
        if self.head == None:
            return None
        
        current_node = self.head
        position = 0
        while(current_node != None and position != index):
            current_node = current_node.next
            position += 1
        if current_node != None:
            return current_node.Type, current_node.Position
        else:
            print("Index not present")
            return None

PanelOrder = LinkedList() 
PanelOrder.insertAtBegin(NameToKey['Refle'], 14)
PanelOrder.insertAtEnd(NameToKey['Refle'], 5)
PanelOrder.insertAtEnd(NameToKey['Refle'], 12)
PanelOrder.insertAtEnd(NameToKey['Refle'], 16)
PanelOrder.insertAtEnd(NameToKey['Refle'], 3)
PanelOrder.insertAtEnd(NameToKey['Refle'], 7)
PanelOrder.insertAtEnd(NameToKey['Refle'], 10)
PanelOrder.insertAtEnd(NameToKey['Refle'], 18)
PanelOrder.insertAtEnd(NameToKey['Refle'], 1)
PanelOrder.insertAtEnd(NameToKey['Refle'], 9)
PanelOrder.insertAtEnd(NameToKey['Refle'], 13)
PanelOrder.insertAtEnd(NameToKey['Refle'], 15)
PanelOrder.insertAtEnd(NameToKey['Refle'], 4)
PanelOrder.insertAtEnd(NameToKey['Refle'], 6)
PanelOrder.insertAtEnd(NameToKey['Refle'], 11)
PanelOrder.insertAtEnd(NameToKey['Refle'], 17)
PanelOrder.insertAtEnd(NameToKey['Refle'], 2)
PanelOrder.insertAtEnd(NameToKey['Refle'], 8)

x = PanelsToChange(2.4,1.1,room_dim)
print(f'Changing {int(x)} panels to Absorption')

if x > 18:
    print('Only 18 panels available')
    x = 18

DPanels = int(input(f"Enter the number of diffusion panels to put ({18-x} Available): "))
if DPanels > 18-x :
    print("Not a valid number, using 0")
    DPanels = 0

for i in range(18):
    if i < x:
        PanelOrder.updateNode(NameToKey['Abs'],i)
    elif i < x + DPanels:
        PanelOrder.updateNode(NameToKey['Scatt'],i) 
    else:
        PanelOrder.updateNode(NameToKey['Refle'],i) 


def GetPanels(PanelOrder):
    PanelArray = {}
    for i in range(18):
        currentPanel_Type, currentPanel_Pos = PanelOrder.returnAtIndex(i)
        PanelArray[currentPanel_Pos] = currentPanel_Type
    return PanelArray

PanelArray = GetPanels(PanelOrder)
for i in range(1,19):
    print(PanelArray[i])
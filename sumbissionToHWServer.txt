#! /usr/bin/python
import sys
boardName=sys.argv[3]
#print()
fin=boardName=open(sys.argv[1],"r")
fout=open(sys.argv[2],"w")
boardInput=""
counter=0
for line in fin:
    if(counter>0 and counter<10):
        boardInput+=line
        counter+=1
    if(sys.argv[3] in line):
        print(line)
        counter+=1

print(boardInput)
# boards=fin.read().strip()
#
# boards=boards.split("\n\n")
# #print(boards)
# endi=0
# for i in range(len(boards)):
#
#     #print(boardName)
#     if (sys.argv[3] in boards[i][0]):
#         boards[i]=boards[i].split("\n")
#         endi=i
#         break
# boardInput=boards[endi]
# boardInput=boardInput.split("\n")[1:]
# boardInput="\n".join(boardInput)
# print(boardInput+"\n")

Cliques=[[0,1,2,3,4,5,6,7,8],
[9,10,11,12,13,14,15,16,17],
[18,19,20,21,22,23,24,25,26],
[27,28,29,30,31,32,33,34,35],
[36,37,38,39,40,41,42,43,44],
[45,46,47,48,49,50,51,52,53],
[54,55,56,57,58,59,60,61,62],
[63,64,65,66,67,68,69,70,71],
[72,73,74,75,76,77,78,79,80,],
[0,9,18,27,36,45,54,63,72],
[1,10,19,28,37,46,55,64,73],
[2,11,20,29,38,47,56,65,74],
[3,12,21,30,39,48,57,66,75],
[4,13,22,31,40,49,58,67,76],
[5,14,23,32,41,50,59,68,77],
[6,15,24,33,42,51,60,69,78],
[7,16,25,34,43,52,61,70,79],
[8,17,26,35,44,53,62,71,80],
[0,1,2,9,10,11,18,19,20],
[3,4,5,12,13,14,21,22,23],
[6,7,8,15,16,17,24,25,26],
[27,28,29,36,37,38,45,46,47],
[30,31,32,39,40,41,48,49,50],
[33,34,35,42,43,44,51,52,53],
[54,55,56,63,64,65,72,73,74],
[57,58,59,66,67,68,75,76,77],
[60,61,62,69,70,71,78,79,80]
]

class Board:




  def __init__(self,boardString):
    self.values=[]
    self.backTrackCounter=0
    self.dependenceStack=[]
    self.assumptions=[]
    counter = 0
    boardString=boardString.split("\n")
    for row in boardString:
      row=row.split(",")
      for num in row:

        if(num=="_"):

          newCell = Cell(counter,0)
          self.values.append(newCell)
          counter+=1
        else:
          if(num == ""):
            x=3 #this is just meant to do nothing
          else:
            newCell = Cell(counter,int(num))
            self.values.append(newCell)
            self.dependenceStack.append(newCell.pos)
            counter+=1
  def resetOptions(self):
    for cell in self.values:
      if(cell.value==0):
        cell.fixOptions(board,True)
  def doForcedVals(self):
    consistency=True
    foundNew=True
    while(foundNew and consistency):
      foundNew=False

      for cell in self.values:
        returnVal = cell.fixOptions(self)
        if(returnVal == 1):
          foundNew=True
          self.dependenceStack.append(cell.pos)
        if(returnVal == -1):

          #print("The following board is bad because of" +str(cell.pos))

          consistency=False

    #if(not consistency):
      #board.printBoard()  #print(foundNew,consistency)
    return consistency
  def printBoard(self):
    for i in range(9):
      string = ""
      for j in range(9):
        string+=str(self.values[9*i+j].value)+","
      print(string)
    print("\n")




def getCliqueIndices(pos):
  rowClique = int(pos/9)
  colClique = 9 + pos%9
  topMidBottom = int(pos/27)
  leftMidRight = int((pos%9)/3)
  boxClique = 18+3*topMidBottom+leftMidRight
  return [rowClique,colClique,boxClique]

class Cell:

  def fixOptions(self,board,resetOptions=False,dontForceThru=True):
    if(resetOptions):
      self.options=[1,2,3,4,5,6,7,8,9]
    if(self.value!=0 and dontForceThru):
      return 0
    ans=len(self.options)
    for clique in self.cliques:
      clique=Cliques[clique]
      for val in clique:
        if(val!=self.pos and board.values[val].value in self.options):
          self.options.remove(board.values[val].value)
    if(len(self.options)==0):
      return -1
    if(len(self.options)<ans and len(self.options)>1):
      return 0
    if(len(self.options)==1):
      if(self.options[0]!=self.value and self.value!=0):
        return -2
      self.value=self.options[0]
      return 1
    else:
      return 0

  def __init__(self,pos,value=0):
    self.value=value
    self.pos=pos
    self.cliques = getCliqueIndices(pos)
    self.options=[1,2,3,4,5,6,7,8,9]
    self.bashedOutButAmNot=[]

#returns 1 if found new info, 0 if didn't, -1 if inconsistent
board = Board(boardInput)
board.printBoard()
board.doForcedVals()
#print(board.values[1].options)
def makeAssumption(board,pos):
  board.assumptions.append(pos)
  board.dependenceStack.append(pos)

  for i in board.values[pos].options:
    if(not i in board.values[pos].bashedOutButAmNot):

      board.values[pos].value=i
      break
  #print("Made assumption on position: "+str(pos)+", saying that it was "+str(board.values[pos].value))

def reverseAssumption(board,pos):

  #board.values[pos].bashedOutButAmNot.append(board.values[pos].value)
  board.backTrackCounter+=1
  #print("Board dependence stack", board.dependenceStack)
  #print("Assumption stack", board.assumptions)
  while(board.dependenceStack[-1]!=pos):
    #print("Im doing this a lot")
    board.values[board.dependenceStack[-1]].value=0
    board.values[board.dependenceStack[-1]].options=[1,2,3,4,5,6,7,8,9]
    board.dependenceStack=board.dependenceStack[:-1]
  board.values[board.dependenceStack[-1]].bashedOutButAmNot.append(board.values[board.dependenceStack[-1]].value)
  board.values[board.dependenceStack[-1]].value=0
  board.dependenceStack=board.dependenceStack[:-1]
  board.assumptions=board.assumptions[:-1]
  board.resetOptions()
  board.doForcedVals()
  if(len(board.values[pos].options)==len(board.values[pos].bashedOutButAmNot)):
    #print("we are out of options, so the last assumption was wrong")
    board.values[pos].bashedOutButAmNot=[]

    reverseAssumption(board,board.assumptions[-1])

def solve(board):
  x=board.doForcedVals()
  while(len(board.dependenceStack)<81):
    pos=80
    if(len(board.dependenceStack)>30):
      for i in range(81):
        if(board.values[i].value==0):
          pos=i
          break
    else:
      minOpts=8
      for i in range(81):
        if(board.values[i].value==0 and len(board.values[i].options)<minOpts ):
          pos=i
          if(len(board.values[i].options)==2):
            break
    makeAssumption(board,pos)
    #board.printBoard()
    if(board.doForcedVals()==False):
        reverseAssumption(board,pos)
    #board.printBoard()
solve(board)
board.printBoard()
print(board.backTrackCounter)
for i in range(9):
    string=""
    for j in range(9):
        string+=str(board.values[9*i+j].value)+","
    string=string[:-1]
    string+="\n"
    fout.write(string)

#! /usr/bin/python
import sys
l = sys.argv
fin=open(l[1],"r")
fout=open(l[2],"w")
boardInput = """_,_,4,1,_,_,5,2,7
2,1,3,7,_,_,_,_,_
_,_,7,6,2,4,_,_,_
3,5,_,2,7,_,_,_,_
_,_,_,_,3,_,8,7,5
_,4,_,_,_,6,_,1,3
4,7,2,_,1,_,_,5,_
_,3,1,_,6,2,_,_,9
9,_,_,_,_,_,1,8,_"""

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
            x=3
          else:
            newCell = Cell(counter,int(num))
            self.values.append(newCell)
            counter+=1

  def doForcedVals(self):
    consistency=True
    foundNew=True
    while(foundNew and consistency):
      foundNew=False
      consistency=True
      for cell in self.values:
        returnVal = cell.fixOptions(self)
        if(returnVal == 1):
          foundNew=True
        if(returnVal == -1):
          print(cell.pos)
          consistency=False
      #print(foundNew,consistency)
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
  def fixOptions(self,board,dontForceThru=True):
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



board = Board(boardInput)

board.doForcedVals()
board.printBoard()

unsurePositions = []

#returns 1 if found new info, 0 if didn't, -1 if inconsistent


def solve(board):
  board.doForcedVals()
  for i in range(81):
    if(board.values.value==0):
      unsurePositions.append(i)
      getCliqueIndicies(pos)

swappedBoard=fin.read().strip()

# def swappedVals(swappedBoard):
board = Board(swappedBoard)
badVals=[]
for cell in board.values:


  cellRet = cell.fixOptions(board,False)
  #print(cell.pos,cellRet)

  if(cellRet==-2):
    badVals.append(str(cell.pos))

fout.write(",".join(badVals))

#board.printBoard()

import cell
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

          newCell = cell.Cell(counter,0)
          self.values.append(newCell)
          counter+=1
        else:
          if(num == ""):
            x=3 #this is just meant to do nothing
          else:
            newCell = cell.Cell(counter,int(num))
            self.values.append(newCell)
            self.dependenceStack.append(newCell.pos)
            counter+=1
  def resetOptions(self):
    for cell in self.values:
      if(cell.value==0):
        cell.fixOptions(self,True)
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

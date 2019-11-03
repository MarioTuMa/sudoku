import board
def getCliqueIndices(pos):
  rowClique = int(pos/9)
  colClique = 9 + pos%9
  topMidBottom = int(pos/27)
  leftMidRight = int((pos%9)/3)
  boxClique = 18+3*topMidBottom+leftMidRight
  return [rowClique,colClique,boxClique]

CliqueFile=open("cliques.csv","r")
#cliques.csv contains all cliques, where a clique is a group of 9 squares that all must be distinct
Cliques=[]
for line in CliqueFile:
    line=line.split(",")
    for i in range(len(line)):
        line[i]=int(line[i])
    Cliques.append(line)

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

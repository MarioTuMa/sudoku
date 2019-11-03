#! /usr/bin/python
import sys
import cell
import board

import datetime
dt_started = datetime.datetime.utcnow()

boardName=sys.argv[3]
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

board = board.Board(boardInput)
board.printBoard()
board.doForcedVals()

def makeAssumption(board,pos):
  board.assumptions.append(pos)
  board.dependenceStack.append(pos)

  for i in board.values[pos].options:
    if(not i in board.values[pos].bashedOutButAmNot):

      board.values[pos].value=i
      break

def reverseAssumption(board,pos):
  board.backTrackCounter+=1
  while(board.dependenceStack[-1]!=pos):
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
    if(board.doForcedVals()==False):
        reverseAssumption(board,pos)

solve(board)
board.printBoard()
dt_ended = datetime.datetime.utcnow()
elapsed = (dt_ended - dt_started).total_seconds()
print("Number of wrong assumptions: "+str(board.backTrackCounter))
print("Time elapsed: "+str(elapsed))

#outputting to csv
for i in range(9):
    string=""
    for j in range(9):
        string+=str(board.values[9*i+j].value)+","
    string=string[:-1]
    string+="\n"
    fout.write(string)

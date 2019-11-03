#! /usr/bin/python
#takes in a full board with two swapped values and returns the indicies of the swapped values
import sys
import cell
import board
l = sys.argv
fin=open(l[1],"r")
fout=open(l[2],"w")

swappedBoard=fin.read().strip()
board = Board(swappedBoard)
badVals=[]
for cell in board.values:
  cellRet = cell.fixOptions(board,False)
  if(cellRet==-2):
    badVals.append(str(cell.pos))
fout.write(",".join(badVals))

#board.printBoard()

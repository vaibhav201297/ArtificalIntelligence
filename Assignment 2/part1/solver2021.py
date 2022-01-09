#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Vaibhav Vishwanath : 2000912419
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#


from os import curdir
from typing import Match, final
import sys
import numpy as np
import copy
import time
from queue import PriorityQueue

from numpy.lib.shape_base import split
ROWS=5
COLS=5


def heuristic(puzzle):
    #Used the goal puzzle to calculate actual position of tile
    goal_puzzle=np.arange(1,26).reshape(5,-1)
    #print(goal_puzzle)
    heu=[]
    sum=0
    #The 2 dictionaries counts the number of elements away from its actual position and multiplies it with the weights assigned below
    heu_count={0:0,1:0,2:0,3:0,4:0}
    heu_weights={0:0,1:0.25,2:0.5,3:0.75,4:1}
    for i in range(5):
        rowH=[]
        for j in range(5):
            #print(puzzle[i][j])
            result=np.where(goal_puzzle[:]==puzzle[i][j])
            #print(result)
            row=result[0][0]
            col=result[1][0]
            dis=dist(i,j,row,col)
            rowH.append(dis)
            heu_count[dis]+=1
            sum+=dist(i,j,row,col)
        heu.append(rowH) 
    #heu is the 2d array with the minimum distance of each tile to reach its actual position
    #print(heu)
    final_result=0
    for i in heu_count:
        final_result=final_result+heu_weights[i]*heu_count[i]
    corners=(heu[0][0]+heu[4][0]+heu[0][4]+heu[4][4])/4
    top_bottom=(heu[0][1]+heu[0][2]+heu[0][3]+heu[4][1]+heu[4][2]+heu[4][3])/6
    left_right=(heu[1][0]+heu[2][0]+heu[3][0] + heu[1][4]+heu[2][4]+heu[3][4])/6
    inner_ring=(heu[1][1]+heu[2][1]+heu[3][1]+heu[3][2]+heu[3][3]+heu[2][3]+heu[1][2]+heu[1][3])/8

    
    # Below heuristic solves board0 in 0.01 seconds and board0.5 in 0.2s
    #return corners + top_bottom +left_right + inner_ring

    #Below heuristic solves board0 in 
    #return corners+top_bottom+left_right+0.5*inner_ring




    #Below heuristic is not optimal for board0.5 -- DONT USE
    #return 0.25*corners + 0.25*left_right +0.25*top_bottom + 0.5*inner_ring
    
    #print(heu_count[1]+heu_count[2]+heu_count[3]+heu_count[4])

    #Solves board0 in 0.01sec and board0.5 in 1.5 seconds and board3 in 15.45seconds
    #[Board3 is a test board where all elements are placed correctly except 24 and 25] 
    #This heuristic starts exploring all states after 7-8 levels
    return final_result
    
    




'''
Old Heuristic Based on sum of distances of each tile from its actual position
def heuristic(puzzle):
    goal_puzzle=np.arange(1,26).reshape(5,-1)
    #print(goal_puzzle)
    heu=[]
    sum=0
    for i in range(5):
        rowH=[]
        for j in range(5):
            #print(puzzle[i][j])
            result=np.where(goal_puzzle[:]==puzzle[i][j])
            #print(result)
            row=result[0][0]
            col=result[1][0]
            rowH.append(dist(i,j,row,col))
            sum+=dist(i,j,row,col)
        heu.append(rowH) 
    #print(heu)
    #arr1=np.asarray(heu) 
    #print(np.average(arr5))
    #print(np.average(arr6))
    #print(arr7)
    #print(arr1)
    #print(arr2)
    #print(arr3)
    #print(arr4)
    return sum
'''                

def printable_board(board):
    return [ ('%3d ')*5  % board[j:(j+5)] for j in range(0, 5*5, 5) ]

'''
Calculate distance of tile from its actual position
'''



def dist(r1,c1,r2,c2):
    rm=0
    cm=0
    if(abs(r1-r2)>2):
        if(abs(r1-r2)==4):
            rm=1
        else:
            rm=2
    else:
        rm=abs(r1-r2)
    if(abs(c1-c2)>2):
        if(abs(c1-c2)==4):
            cm=1
        else:
            cm=2
    else:
        cm=abs(c1-c2)
    return rm+cm


#LEFT MOVE
def left(puzzle,row):
    puzzle=puzzle[0:row][:] +[puzzle[row][1:]+puzzle[row][0:1]] +puzzle[row+1:][:]
    #print(puzzle)
    return puzzle

#RIGHT MOVE
def right(puzzle,row):
    puzzle=puzzle[0:row][:] +[puzzle[row][4:]+puzzle[row][0:4]] +puzzle[row+1:][:]
    #print(puzzle)
    return puzzle

#UP MOVE
def up(puzzle,column):
    c=copy.deepcopy(puzzle)
    

    temp=c[0][column]
    
    for i in range(0,5-1):
        for j in range(0,5):
            if(j==column):
                c[i][j]=c[i+1][j]
                #print(puzzle[i][j])  
    c[5-1][column]=temp
    #print(copy)
    return c

#DOWN MOVE
def down(puzzle,column):
    c=copy.deepcopy(puzzle)
    temp=c[5-1][column]
    for i in range(5-1,-1,-1):
        for j in range(0,5):
            if(j==column):
                c[i][j]=c[i-1][j]
    c[0][column]=temp
    #print(puzzle)
    return c

    
#USED FOR CLOCKWISE ROTATE 
def rotate(puzzle,up,down,left,right,isOuter):
    c=copy.deepcopy(puzzle)
    counter=16 if isOuter else 8
    temp=c[up+1][left]
    while(counter>=0):
        for i in range(left,right+1):
            current=c[up][i]
            c[up][i]=temp
            temp=current
            counter-=1
                
        for i in range(up+1,down+1):
            current=c[i][right]
            c[i][right]=temp
            temp=current
            counter-=1
        for i in range(right-1,left-1,-1):
            current=c[down][i]
            c[down][i]=temp
            temp=current
            counter-=1
        for i in range(down-1,up-1,-1):
            current=c[i][left]
            c[i][left]=temp
            temp=current
            counter-=1
    return c

#USED FOR COUNTER_CLOCKWISE ROTATE
def anti_rotate(puzzle,up,down,left,right,isOuter):
    c=copy.deepcopy(puzzle)
    counter=16 if isOuter else 8
    temp=puzzle[up][left+1]
    while(counter>=0):
        for i in range(up,down+1):
            current=c[i][up]
            c[i][up]=temp
            temp=current
            counter-=1
        for i in range(left+1,right+1):
            current=puzzle[down][i]
            c[down][i]=temp
            temp=current
            counter-=1
        for i in range(down-1,up-1,-1):
            current=c[i][right]
            c[i][right]=temp
            temp=current
            counter-=1
        for i in range(right-1,left-1,-1):
            current=c[up][i]
            c[up][i]=temp
            temp=current
            counter-=1
        return c


#CLOCKWISE ROTATE MOVE
def Clockwise(puzzle,isOuter):
    if isOuter:
        puzzle=rotate(puzzle,0,5-1,0,5-1,isOuter) 
        return puzzle
    else:
        puzzle=rotate(puzzle,1,5-2,1,5-2,isOuter) 
        return puzzle
#ANTI-CLOCKWISE ROTATE MOVE
def AntiClockwise(puzzle,isOuter):
    if isOuter:
        puzzle=anti_rotate(puzzle,0,5-1,0,5-1,isOuter)
        return puzzle
    else:
        puzzle=anti_rotate(puzzle,1,5-2,1,5-2,isOuter)
        return puzzle

'''
def check_visited(succ,visited):
    #print("VISTED ARRAY LENGTH"+str(len(visited)))
    #print(type(visited))
    for a,b in visited:
        for i,j,k in succ:
            a1=np.asarray(i,dtype=object)
            b1=np.asarray(a,dtype=object)
            #print(a1)
            #print(b1)
            if np.array_equal(a1,b1):
                succ.remove((i,j,k))
    #print(len(succ))
    #print(len(heuristics))
    return succ
'''
# return a list of possible successor states
def successors(puzzle,visited,level):
    level=level+1
    s1=left(puzzle,0)
    s2=left(puzzle,1)
    s3=left(puzzle,2)
    s4=left(puzzle,3)
    s5=left(puzzle,4)
    s6=right(puzzle,0)
    s7=right(puzzle,1)
    s8=right(puzzle,2)
    s9=right(puzzle,3)
    s10=right(puzzle,4)
    s11=up(puzzle,0)
    s12=up(puzzle,1)
    s13=up(puzzle,2)
    s14=up(puzzle,3)
    s15=up(puzzle,4)
    s16=down(puzzle,0)
    s17=down(puzzle,1)
    s18=down(puzzle,2)
    s19=down(puzzle,3)
    s20=down(puzzle,4)
    s21=Clockwise(puzzle,True)
    s22=Clockwise(puzzle,False)
    s23=AntiClockwise(puzzle,True)
    s24=AntiClockwise(puzzle,False)
    successors=[
        (s1,"L1",level+heuristic(s1)),(s2,"L2",level+heuristic(s2)),(s3,"L3",level+heuristic(s3)),(s4,"L4",level+heuristic(s3)),(s5,"L5",level+heuristic(s5)),
        (s6,"R1",level+heuristic(s6)),(s7,"R2",level+heuristic(s7)),(s8,"R3",level+heuristic(s8)),(s9,"R4",level+heuristic(s9)),(s10,"R5",level+heuristic(s10)),
        (s11,"U1",level+heuristic(s11)),(s12,"U2",level+heuristic(s12)),(s13,"U3",level+heuristic(s13)),(s14,"U4",level+heuristic(s14)),(s15,"U5",level+heuristic(s15)),
        (s16,"D1",level+heuristic(s16)),(s17,"D2",level+heuristic(s17)),(s18,"D3",level+heuristic(s18)),(s19,"D4",level+heuristic(s19)),(s20,"D5",level+heuristic(s20)),
        (s21,"Oc",level+heuristic(s21)),(s22,"Ic",level+heuristic(s22)),(s23,"Occ",level+heuristic(s23)),(s24,"Icc",level+heuristic(s24))
    ]
    #print(len(successors))
    #successors=check_visited(successors,visited)
    for i,j,k in successors:
        #print(i)
        if i not in visited:
            visited.append(i)
        else:
            successors.remove((i,j,k))
    
    #print(len(visited))
    #print(heu)
    #successors.sort(key=lambda x:x[2])
    
    #heu.sort()
    #print(heu)
    return successors,level,visited



# check if we've reached the goal
def is_goal(state):
    counter=1
    for i in range(5):
        for j in range(5):
            if(not(state[i][j]==counter)):
                return False
            else:
                counter+=1
    return True

        

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """ 
    

    final_board=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
    initial_puzzle=list(np.asarray(list(initial_board)).reshape((5,5)).tolist())
    #print(initial_puzzle)
    final_puzzle=list(np.asarray(list(final_board)).reshape((5,5)).tolist())

    #print(aa)
    #print(left(down(up(right(up(down(down(initial_puzzle,4),0),3),2),1),3),4))
    #print(down(right(left(right(AntiClockwise(AntiClockwise(AntiClockwise(initial_puzzle,True),False),True),2),0),1),2))
    #print(left(up(right(down(AntiClockwise(initial_puzzle,True),4),0),0),4))
    #print(Clockwise(right(AntiClockwise(left(up(down(down(initial_puzzle,4),0),1),4),False),2),False))
    #print(ll)
    ih=heuristic(initial_puzzle)
    
    #print(heuristic(AntiClockwise(initial_puzzle,False)))
    #print(heuristic(left(initial_puzzle,1)))
    #print(heuristic(right(initial_puzzle,3)))
    #print(ih)
    #print(aa)
    level=0
    counter=0
    #limit=250
    fringe=PriorityQueue()
    fringe.put((level+ih,[initial_puzzle,'',level]))
    visited=[]
    visited.append(initial_puzzle)
    
    
    while(not fringe.empty()):
        counter+=1
        #print(counter)
        heu,state=fringe.get()
        (current,moves,level)=(state[0],state[1],state[2])
        #print(heu)
        #print(current)
        #print(moves)
        #print(level)
        #print(qq)
        if is_goal(current):
            #print(fringe[0][1])
            route=moves.split('|')
            #print(route)
            #print(fringe[0][1].split('|'))
            return route[1:]
        
        #print("Move Taken: "+moves+ " with heuristic of "+str(heu))
        temp,level,visited=successors(current,visited,level)
        for i,j,k in temp:
            fringe.put((k,(i,moves+'|'+j,level)))
            #print(len(fringe.queue))
            #fringe.append((i,moves+'|'+j,k,level))
            ##]print("LEVEL "+str(level)+"  "+ str(k)+"  "+str(moves+"|"+j))
            #print(i)
        #fringe.sort(key=lambda x:x[2])
        
    return ""
        

# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))
    test=sys.argv[1]
    #test="board1.txt"
    start_state = []
    #with open(sys.argv[1], 'r') as file:
    with open(test, 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    #print(start_state)
    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))
    

    
    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    t0=time.time()
    route = solve(tuple(start_state))
    t1=time.time()
    #print("Solution found in "+str(t1-t0)+" seconds with " + str(len(route)) + " moves:" + "\n" + " ".join(route))
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))

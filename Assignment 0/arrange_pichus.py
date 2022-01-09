#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Vaibhav Vishwanath | Username : vavish
#
# Based on skeleton code in CSCI B551, Fall 2021.
# All work except for the skeleton code has been written by me. Any code taken from sites have been cited accordingly
import re
import sys
import numpy as np
# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]

# Count total # of pichus on house_map
def count_pichus(house_map):
	return sum([ row.count('p') for row in house_map ] )

# Return a string with the house_map rendered in a human-pichuly format
def printable_house_map(house_map):
	return "\n".join(["".join(row) for row in house_map])

# Function to return the row string of the position where an agent is about to be placed	
def get_row_string(house_map,pichu_locs):
	matrix=np.asarray(house_map)
	row=matrix[pichu_locs[0][0]]
	#print(row)
	row_string=''
	for i in row:
		row_string+=i
	#print(row_string)
	return row_string
	
# Function to return the column string of the position where an agent will be placed	
def get_col_string(house_map,pichu_locs):
	matrix=np.asarray(house_map)
	col=matrix[:,pichu_locs[0][1]]
	col_string=''
	for i in col:
		col_string+=i
	#print(col_string)
	return col_string

#Function to return the diagonal strings from the position the agent will be placed
#Taken from StackOverflow--------------------https://stackoverflow.com/questions/6313308/get-all-the-diagonals-in-a-matrix-list-of-lists-in-python--------------------
def get_diagonals(house_map,pichu_locs):
	matrix=np.asarray(house_map)
	major=np.diagonal(matrix,offset=(pichu_locs[0][1]-pichu_locs[0][0]))
	minor=np.diagonal(np.rot90(matrix),offset=(-matrix.shape[1]+(pichu_locs[0][1]+pichu_locs[0][0])+1))
	major_diagonal=''
	minor_diagonal=''
	for i in major:
		major_diagonal+=i
	for i in minor:
		minor_diagonal+=i
	#print(major_diagonal)
	#print(minor_diagonal)
	return (major_diagonal,minor_diagonal)
##-----------------------X-------------------------- End of Code from Stack Overflow-------------------------------------------------------------------------------------


#Function checks if the position on the map is safe from other agents or not
def safe(house_map,safe_pichu):
	pichu_locs=[(i,j) for i in range(len(house_map)) for j in range(len(house_map[0])) if house_map[i][j]=='p']
	pichu_locs=list(set(pichu_locs)-set(safe_pichu))
	#print(pichu_locs)
	#print(safe_pichu)
	result1=True
	result2=True
	result3=True
	result4=True
	for i in range(len(safe_pichu)):
		if pichu_locs[0][0]==safe_pichu[i][0]:
			#print('Same Row')
			rowString=get_row_string(house_map,pichu_locs)
			result1=bool(re.search("[p]\\.*[p]",rowString))
			'''
			for j in range( abs(pichu_locs[0][1]-safe_pichu[i][1])+1 ):
				#print(pichu_locs[0][1])
				#print(safe_pichu[i][1])
				rowString+=house_map[0][j]
			print("Row String:"+rowString)	
			if("X@" in rowString[1:len(rowString)-1]):
				result=True
			else:
				result=False
			'''	
			#Inverting Result flag because the regex returns value if pattern is matched	
			result1= not result1
			
			
		if pichu_locs[0][1]==safe_pichu[i][1]:
			#print('Same Column')
			colString=get_col_string(house_map,pichu_locs)
			'''
			#print(pichu_locs[0][1])
			#print(safe_pichu[0][1])
			for j in range(abs(pichu_locs[0][0]-safe_pichu[i][0])+1 ):
				colString+=house_map[j][0]
			print("ColString:"+colString)
			if("X@" in colString[1:len(colString)-1]):
				result=True
			else:
				result=False
			'''
			result2=bool(re.search("[p]\\.*[p]",colString))
			#Inverting Result flag because the regex returns value if pattern is matched	
			result2=not result2
			
		if(pichu_locs[0][1]-pichu_locs[0][0] == (safe_pichu[i][1]-safe_pichu[i][0])):
			#print('Same Diagonal1')
			(diag1,diag2)=get_diagonals(house_map,pichu_locs)
			#Check both diagonal strings to see if there is a conflict with another agent
			result3=( ((diag1.count('p')==1) or not(bool(re.search("[p]\\.*[p]",diag1)))) and (diag2.count('p')==1 or not bool(re.search("[p]\\.*[p]",diag2))))
			
		if(pichu_locs[0][1]+pichu_locs[0][0] == (safe_pichu[i][1]+safe_pichu[i][0])):
			#print('Same Diagonal2')
			(diag1,diag2)=get_diagonals(house_map,pichu_locs)
			#print("Diagonal 1:"+diag1)
			#print("Diagonal 2:"+diag2)
			#Check both diagonal strings to see if there is a conflict with another agent
			result4=( ((diag1.count('p')==1) or not(bool(re.search("[p]\\.*[p]",diag1)))) and (diag2.count('p')==1 or not bool(re.search("[p]\\.*[p]",diag2))))
			
	if(result1 and result2 and result3 and result4):
		safe_pichu.append(pichu_locs[0])
	
		
	#print("Is Safe?"+str(result1 and result2 and result3 and result4))
	return result1 and result2 and result3 and result4
				
		

# Add a pichu to the house_map at the given position, and return a new house_map (doesn't change original)
def add_pichu(house_map, row, col):
	return house_map[0:row] + [house_map[row][0:col] + ['p',] + house_map[row][col+1:]] + house_map[row+1:]

#Tried to use a heuristic but did not work correctly. 	
'''
def visible_dots(row,col,house_map):
	#Same Row Elements
	count1=0
	count2=-0
	count3=0
	count4=0
	#print("Row& column :"+str(row)+","+str(col))
	#Count Visible Dots in Same Row
	i=col-1
	while(i>=0 and house_map[row][i] not in 'X@'):
		if(house_map[row][i]=='.'):
			count1+=1
		i=i-1
	i=col+1
	while(i<len(house_map[0]) and house_map[row][i] not in 'X@' ):
		if(house_map[row][i]=='.'):
			count1+=1	
		i=i+1
	#print("Dots in Same Row :"+str(count1))
	#Same Col Elements
	j=row-1
	while(j>=0 and house_map[j][col] not in 'X@' and not j==row):
		if(house_map[j][col]=='.'):
			count2+=1
		j=j-1
	j=row+1
	while(j<len(house_map) and house_map[j][col] not in 'X@'):
		if(house_map[j][col]=='.'):
			count2+=1
		j=j+1
	#print("Dots in Same Column :"+str(count2))
	r,c=row-1,col+1
	#Diag1 Top Right
	while(r>=0 and c<len(house_map[0]) and house_map[r][c] not in 'X@' ):
		if(house_map[r][c]=='.'):
			count3+=1
		r=r-1
		c=c+1

	r,c=row+1,col-1
	#Diag1 Bottom Left
	while(r<len(house_map) and c>=0 and house_map[r][c] not in 'X@' ):
		if(house_map[r][c]=='.'):
			count3+=1
		r=r+1
		c=c-1
	#print("Dots in Diag1  :"+str(count3))
			
	r,c=row+1,col+1
	#Diag 2 Bottom Right
	while(r<len(house_map) and c<len(house_map[0]) and house_map[r][c] not in 'X@'):
		if(house_map[r][c]=='.'):
			count4+=1
		r=r+1
		c=c+1
		
	r,c=row-1,col-1
	#Diag 2 Top Left
	while(r>=0 and c>=0 and house_map[r][c] not in 'X@'):
		if(house_map[r][c]=='.'):
			count4+=1
		r=r-1
		c=c-1
	#print("Dots in Diag2  :"+str(count4))	
	#print(str(count1+count2+count3+count4))
	return count1+count2+count3+count4
'''
# Get list of successors of given house_map state and return only safe successors
def successors(house_map):
	successors=	 [add_pichu(house_map, r, c) for r in range(0, len(house_map)) for c in range(0,len(house_map[0])) if house_map[r][c] == '.']
	#print(len(successors))
	safe_options=[]
	safe_pichu=[(i,j) for i in range(len(house_map)) for j in range(len(house_map[0])) if house_map[i][j]=='p']
	#print(safe_pichu)
	for i in successors:
		if(safe(i,safe_pichu)):
			safe_options.append(i)
	#print(len(safe_options))
	return safe_options

# check if house_map is a goal state
def is_goal(house_map, k):
	return count_pichus(house_map) == k 

'''
def min_visible_dots(fringe):
	dots=[]
	for i in range(len(fringe)):
		dots.append(fringe[i][1])
	return dots.index(min(dots))
'''		
# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_house_map, success), where:
# - new_house_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#


def solve(initial_house_map,k):
	fringe = [(initial_house_map)]
	
	
	safe_pichu=[(i,j) for i in range(len(initial_house_map)) for j in range(len(initial_house_map[0])) if initial_house_map[i][j]=='p']
	while len(fringe) > 0:
		#print(len(fringe))
		
		for new_house_map in successors(fringe.pop(0)):
			
			#print(printable_house_map(new_house_map))
			#pichu_locs=[(i,j) for i in range(len(new_house_map)) for j in range(len(new_house_map[0])) if new_house_map[i][j]=='p']
			#print(pichu_locs)
			#pichu_locs=list(set(pichu_locs)-set(safe_pichu))
			#print(safe_pichu)
			#print('Adding p as it is safe')
			
			#house_map=new_house_map
			#print(visible_dots(safe_pichu[-1][0],safe_pichu[-1][1],house_map))
			#visible_dots(safe_pichu[-1][0],safe_pichu[-1][1],house_map)
			fringe.append(new_house_map)
			#visited.append(new_house_map)
			if is_goal(new_house_map,k):
				return(new_house_map,True)
			if(len(fringe)==0):
				return '',False
			
	return '',False

# Main Function
if __name__ == "__main__":
	house_map=parse_map(sys.argv[1])
	# This is k, the number of agents
	k = int(sys.argv[2])
	print ("Starting from initial house map:\n" + printable_house_map(house_map) + "\n\nLooking for solution...\n")
	solution = solve(house_map,k)
	print ("Here's what we found:")
	print (printable_house_map(solution[0]) if solution[1] else "False: Could not place "+str(k)+" pichus in the grid without conflicts")

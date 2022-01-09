#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by : Vaibhav Vishwanath | Username:vavish
#
# Based on skeleton code provided in CSCI B551, Fall 2021.
# All modifications done to this skeleton code have been done by me.Any code taken from websites have been cited accordingly
import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")][3:]
		
# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
	return 0 <= pos[0] < n  and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
	moves=((row+1,col), (row-1,col), (row,col-1), (row,col+1))
	
	# Return only moves that are within the house_map and legal (i.e. go through open space ".")
	moves=[ move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@" ) ]
	#print(moves)
	return moves

#Define a heuristic to choose a move with the least distance from the Fringe.	

def heuristic(move,curr_dist,house_map):
	exit=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="@"][0]
	dist= curr_dist+ (abs(move[0]-exit[0]) + abs(move[1]-exit[1]) )
	#print(dist)
	return dist
	
#Function which creates the routes based on the current position and next position of Pichu.	
def create_route(move,curr_move,route_string):
	#move is the move taken
	#curr_move is the position before the move
	if(curr_move[0]-move[0]==1):
		route_string+='U'
	if(curr_move[0]-move[0]==-1):
		route_string+='D'
	if(curr_move[1]-move[1]==1):
		route_string+='L'
	if(curr_move[1]-move[1]==-1):
		route_string+='R'
	
	return route_string

#Function to choose the minimum distance node from the fringe
def min_heuristic_index(fringe):
	distances=[]
	for i in range(len(fringe)):
		distances.append(fringe[i][1])
	#print(min(distances))
	return distances.index(min(distances))
			
#Function to create a visited map with all nodes unvisited at the start
def create_visited(a,b):
	visited_map=[  [False for j in range(b)] for i in range(a) ]
	return visited_map
	
# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)

	
def search(house_map):
	# Find pichu start position
	pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
	fringe=[(pichu_loc,0,'')]
	#Create the visited Map and visit the node with Pichu's position
	visited_map=create_visited(len(house_map),len(house_map[0]))
	#print(house_map)
	visited_map[pichu_loc[0]][pichu_loc[1]]=True
	curr_dist=0
	while fringe:
		curr_dist+=1
		#for i in fringe:
		#	print(i)
		(curr_move, dist,route_string)=fringe.pop(min_heuristic_index(fringe))
		
		
		for move in moves(house_map, *curr_move):
			if house_map[move[0]][move[1]]=="@":
				#print(route_string)
				#print(move)
				#print(curr_move)
				route_string=create_route(move,curr_move,route_string)
				#print(route_string)
				visited_map[move[0]][move[1]]=True
				return (len(route_string), route_string)  # return a dummy answer
			else:
				if(not visited_map[move[0]][move[1]]):
					fringe.append((move, heuristic(move,curr_dist,house_map),create_route(move,curr_move,route_string)))
					visited_map[move[0]][move[1]]=True
	#if the fringe has no more moves to explore, return no solution message
	return (-1,"No Routes Found!!!Looks like you're stuck in the maze")
					#print(visited_map)
					#for i in fringe:
					#	print(i)

# Main Function
if __name__ == "__main__":
	house_map=parse_map(sys.argv[1])
	print("Shhhh... quiet while I navigate!")
	solution = search(house_map)
	print("Here's the solution I found:")
	print(str(solution[0]) + " " + solution[1])


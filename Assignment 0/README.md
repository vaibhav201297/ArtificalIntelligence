<h1>Name : Vaibhav Vishwanath </h1> <h1> University ID : 2000912419 </h1>
<h2>Username : vavish </h2>


<h3>Problem Statement:<br/></h3>
To find a path in the given maze from 'p' to '@' whilst avoiding any obstacles on the way. 
				 
<h3> Output Format: <br/></h3>  To return a path string along with the distance traveled from start to finish.<br/>
If no routes are available, then the program must return False.

 
Abstraction : The following section explains the abstractions of the problem <br/>
<ol> 

<li><h5>State Space </h5>  The State Space contains all possible points in the maze which are not an Obstacle </l1>
<li>  <h5>Initial State S0 </h5> The Initial State is a 2 dimension array with the locations of p,@ and obstacles defined in either of map1.txt or map2.txt files </l1>
 <li><h5>Successor Function </h5>  The Successor Function for this problem will be all possible moves which can be made by p - Move Up, Move Down, Move Left. Move Right</li>
 <li><h5>Goal State</h5>  The Goal State is the state when p reaches the '@' node in the maze. The Goal test is Map(row,column)='@'. </li>

 <li><h5>Cost Funtion</h5>  Uniform cost to explore each neigbouring node</h5>
 <li><h5>Heuristic Used</h5> Manhattan Distance </li>
  </ol>

<h4> Overview of Solution </h4>
The skeleton code provided does not work correctly because the fringe has been implemented using a stack. Also , since there is no visited array to track the nodes visited, the code keeps adding 2 adjacent nodes when it is surrounded by obstacles.<br/>
In order to solve the problem, I initially tried to use Breadth First Search without any heuristic defined. But since the no of states to be explored is very substantial, the fringe was taking up a lot of memory.The same node was also being added multiple times.
So, I decided to use a combination of A* and Greedy Algorithm which will choose the heuristc with minimun distance from the fringe and explore it before other nodes. My Heuristic function is based on Manhattan Distance .
f(x) is the distance travelled from the S0
g(x) is the Manhattan distance from the current node to the goal node.

<h3> Problem Statement <br/></h3>
 To arrange 'k' agents in a map such that no 2 agents can "see" each other. See each other here means, no 2 agents in the same row,column or diagonal. The additional caveat of the problem includes obstacles and you defined by an '@' who can obstruct the view between agents. 

<h3> Output Format : <br/></h3>To return a map of 'k' agents placed such that no agents can see one another. If it's not possible to place 'k' agents, then the program must return False 
Abstraction : The following section explains the abstractions of the problem <br/>
<ol> 
<li><h5>State Space </h5>  The State Space contains all possible points in the map where an agent can be placed </l1>
 <li><h5>Initial State S0 </h5>  The Initial State is a 2 dimension array with the locations of the initial agent 'p', Your Position marked by an '@' and obstacles defined in the form of 'X's either in map1.txt or map2.txt files </l1>
 <li><h5>Successor Function </h5>  The Successor Function for this problem will be all possible moves where the agent can be placed without being visible to the agent already present in the map</li>
 <li><h5>Goal State</h5>  The Goal State is the state when 'k' agents have been placed in the map. The Goal test is Count('p',Map) =='k'. If it's not possible then we have to return False </li>
 <li><h5>Cost Funtion</h5>  Uniform cost to place an agent at one of the spots in the map</h5>
  </ol>

A lot of time has been spent on this problem trying to understand the way the skeleton code works. The successor function in the skeleton code returns all the possible places where an agent can be placed regardless of the fact that it is safe or not from the initially present agent in the map.
I tried to use a heuristic based approach to define the number of visible dots at any given location. But that lead to a dead end since there was no possible way of assuring that lesser the number of dots visible for an agent, better the position. Hence, I dropped that idea and tried changing the skeleton code defined 
I modified the successor function to return only the positions of the agent where it is safe to place the next agent. Then, using the fringe as Stack Data structure, it will explre each of the safe states first and try to fit the other agents consequently in the map. If it is unable to do so, Since we are using a stack, it backtracks all the way back and changes the first agent placed at another position and so on until the 'k' agents are placed. If the fringe is empty, then all spaces have been explored and the code returns False. 


<h3> Output using the pytest command </h3>

![Assignment 0 Output using pytest command](https://github.iu.edu/cs-b551-fa2021/vavish-a0/blob/master/A0.png)




<h1> Assignment 1 </h1>
<h3> Zack Seliger : zseliger </h2>
<h3> Siddharth Tata : sitata </h3>

<h4> Assignment 1 Part 1 </h4>

 
Abstraction : The following section explains the abstractions of the problem 1 <br/>
<ol> 

<li><h5>State Space </h5>  The State Space contains all possible configurations of the 25 puzzle. </l1>
<li>  <h5>Initial State $S0$ </h5> The Initial state $S0$ is the initial puzzle which has to be solved ie board0, board0.5 and board1. </l1>
 <li><h5>Successor Function </h5>  The Successor Function for this puzzle is all the possible moves on the current state - Move Rows 1 through 5  Left(L1,L2,L3,L4,L5) and Right(R1,R2,R3,R4,R5) ,Move Columns 1 through 5 up(U1,U2,U3,U4,U5) and down(D1,D2,D3,D4,D5)  and Clockwise(Oc,Ic), Counter-Clockwise(Occ,Icc) Rotation of Outer and Inner rings of the Puzzle  </li>
 <li><h5>Goal State</h5>  The Goal State is the state when all elements in the state are present sequentially from 1 to 25 </li>

 <li><h5>Cost Funtion</h5>  The cost of making any move is uniform in this puzzle</h5>
 <li><h5>Heuristic Used</h5> Board1 has defeated me. I have tried to figure out a lot of heuristics and have done a lot of analysis on heuristics. I tried Normal Manhattan distance first but it overstimates the costs as it does not take into account the wrap-around movements. Misplaced tiles is another heuristic which can be used but it's  </li>
  </ol>

<h4> Overview of Solution </h4>
The search tree for this solution grows exponentialy as each state will have 24 successors . So the branching factor for this puzzle is 24. Hence, it is vital to use a heuristic function which is able to evaluate the state correctly. If we use Breadth First Search for a solution which will take 7 moves to solve, the approximate number of states that have to explored will be approximately $24^7$. <br>
In my solution, I implement search algorithm3. Revisited states are being discarded. In my solution , I have implemented a weighted average based on the tile misplaced distance. If a tile is at the right position, we multiply it by 0, if the distance of any puzzle from its goal position is 1,then we multiply the number of tiles with distance 1 from its position with 0.25. Similarly, we multiply the tiles with a distance 2 with 0.5, distance 3 with 0.75 and distance 4 with 1. There will never be any tile that is 5 places away from its position. <br/>


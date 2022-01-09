<h1> Assignment 1 </h1>

<h3> Vaibhav Vishwanath : vavish </h3>

<h4> Assignment 1 </h4>

 
Abstraction : The following section explains the abstractions of the problem 1 <br/>
<ol> 

<li><h5>State Space </h5>  The State Space contains all possible configurations of the 25 puzzle. </l1>
<li>  <h5>Initial State S0 </h5> The Initial state $S0$ is the initial puzzle which has to be solved ie board0, board0.5 and board1. </l1>
 <li><h5>Successor Function </h5>  The Successor Function for this puzzle is all the possible moves on the current state - Move Rows 1 through 5  Left(L1,L2,L3,L4,L5) and Right(R1,R2,R3,R4,R5) ,Move Columns 1 through 5 up(U1,U2,U3,U4,U5) and down(D1,D2,D3,D4,D5)  and Clockwise(Oc,Ic), Counter-Clockwise(Occ,Icc) Rotation of Outer and Inner rings of the Puzzle  </li>
 <li><h5>Goal State</h5>  The Goal State is the state when all elements in the state are present sequentially from 1 to 25 </li>

 <li><h5>Cost Function</h5>  The cost of making any move is uniform in this puzzle</h5>
 <li><h5>Heuristic Used</h5> Board1 has defeated me. I have tried to figure out a lot of heuristics and have done a lot of analysis on heuristics. I tried Normal Manhattan distance first but it overstimates the costs as it does not take into account the wrap-around movements. Misplaced tiles is another heuristic which can be used but it's  </li>
  </ol>

<h4> Overview of Solution </h4>
The search tree for this solution grows exponentialy as each state will have 24 successors . So the branching factor for this puzzle is 24. Hence, it is vital to use a heuristic function which is able to evaluate the state correctly. If we use Breadth First Search for a solution which will take 7 moves to solve, the approximate number of states that have to explored will be approximately $24^7$. <br>
In my solution, I implement search algorithm3. Revisited states are being discarded. In my solution , I have implemented a weighted average based on the tile misplaced distance. If a tile is at the right position, we multiply it by 0, if the distance of any puzzle from its goal position is 1,then we multiply the number of tiles with distance 1 from its position with 0.25. Similarly, we multiply the tiles with a distance 2 with 0.5, distance 3 with 0.75 and distance 4 with 1. There will never be any tile that is 5 places away from its position. <br/>


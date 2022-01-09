<h1> Assignment 1 </h1>
<h3> Zack Seliger : zseliger </h2>
<h3> Siddharth Tata : sitata </h3>
<h3> Vaibhav Vishwanath : vavish </h3>

<h4> Assignment 1 Part 1 </h4>

 
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

## part3

For this program, I put the people and their preferences into a hash map with the person's name as the key. I initially put all people into a list with a tuple, where the first element of the touple was the name, but I realized that for scoring states, a hash map would be much more performant for fetching people by name. States are stored in the output format. For scoring, I assumed that the 5% chance of spending 60 minutes reprimanding students would average out to the expected value of 3 minutes per student given a large enough sample size.

I started the inital state as `[]`, or no groups. Then, as a successor function, I returned all combinations of adding the "latest" (in python3, dictionaries are ordered, so this should be the order in which they appear in the file) unassigned person to each group of less then 3 people, and the situation where that person forms a new group with just him/herself. Goal states are where there is no unassigned person.

I used breadth first search, weighting how the fringe should be expended by the current cost of the state/groups as they were. This gave the optimal answer as the first answer, but since we are allowed to submit multiple answers, I thought I could try and optimize this. If no answer was submitted, I weighted how the fringe should expand by the number of people that have been assigned, then the current cost if an answer was submitted. I then realized I could speed up the algorithm if I used a different heuristic. So, I switched to create an "estimated" total cost, which was the current total cost, then weighting the unassigned people (n) as `n/3*5`, for if we assigned the rest of the people into groups of 3 and there were no complications. This sped up the answer from `test2.txt` to 1s from ~27s on my machine. Although it may not be consistent, I'm not doing A* so this shouldn't be an issue.

After running rand100.txt and rand200.txt from QA Community and seeing others scores, I realized my solution wasn't good enough. I switched to using local search, where the initial state was n groups for n people, each group being 1 person, and for successors I found the first group of less than 3 and added that group to all other groups where the total was <= 3 people large.

I also changed the fringe to be a priority queue from the python standard library. The score was the total cost of that group + depth of that successor. I found that I could improve my scores on the rand100.txt and rand200.txt by using exponential weights on each type of penalty. I ended up using `num_groups**5 + num_requested**3 + num_size**2 + num_unrequested**10 + depth**1.5`. This improved my score dramatically on rand100 and rand200 but hurt the performance of test3, but I believe it generalizes better for larger datasets which should help against the unseen test cases.

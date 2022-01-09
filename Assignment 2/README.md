# Assignment 2: Games and Bayesian Classifiers

### **Part 1 (Raichu-Vaibhav Vishwanath)** ###
The game of Raichu is a 2 player game which comprises of 3 pieces each : a pichu, a pikachu and raichu. The pichu can move only diagonally or above another opponent piece thus eliminating it. Similarly, the Pikachu can move only vertically and horizontally and can capture opposition pichu and pikachu, A Raichu can move in any direction and can move any number of moves.
For this problem, I have used minimax algorithm with alpha beta pruning . The successors for a current board involves searching all possible moves for the pieces we have remaining. SInce i am searching till depth 4, it will look at all successors at depth 4. 
I have defined the rules for all pieces possible. 
The minimax function has been adapted from the youtube video <a href='https://www.youtube.com/watch?v=l-hh51ncgDI'></a>.
The summary of my code is as follows:
<ul>
	<li> First call the minimax  algorithm with the successors of the initial board state.</li>
	<li> Then, the recursive implementation will look at all possible successors after choosing the first move</li>
	<li> The evaluation or utility function involves subtracting the number of white pichus and black pichus, white pikachus and black pikachus and white raichus and black raichus when the white player is playing. The inverse is done when the player is black. </li>
</ul>
This assignment helped me understand minimax algorithm and how it is used in 2 player games. My game is performing very well but it is unable to defeat the the opponents raichu. I have tried hard to figure out why it is not choosing the move which can be used to eliminate the oppositon Raichu. It is always 

Attached is the output of the my code playing on Tank against Prof. David's AI.
<img src='https://github.iu.edu/cs-b551-fa2021/abhmura-asangar-vavish-a2/blob/master/part1/Tank_op.png' alt='Output Image'>


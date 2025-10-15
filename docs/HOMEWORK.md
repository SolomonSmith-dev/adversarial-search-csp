Homework 2 (15% of total course weight) – Multiagent Search 
California State University San Bernardino, School of Computer Science and Engineering (CSE)
Date of Issue: September 22, 2025, Date of submission: October 29, 2025 – 11:59 pm (PST)
Module: CSE 5120 Introduction to Artificial Intelligence
Maximum group size: 4 members. Take template cover page (page # 8) for submission.
Assessment brief: The games most commonly studied within AI are deterministic, two-player, turn-taking, perfect information, zero-sum games. “Perfect information” is a synonym for “fully observable,” and “zero-sum” means that what is good for one player is just as bad for the other: there is no “win-win” outcome. For games we often use the term move as a synonym for “action” and position as a synonym for “state.” In this homework, you will develop a zero sum (adversarial) tic-tac-toe game (noughts and crosses) by implementing Minimax and its variation called Negamax algorithm which will consist of a MAX (human) and MIN (a computer) players. The human player MAX will play against the machine on a larger tic-tac-toe board where it will move first, and then the MIN player takes turns moving until the game is over. At the end of the game, points are awarded to the winning player and penalties are given to the loser. You will use the extensively studied elements to formulate your game scenario: 
•	S0: The initial state, which specifies how the game is set up at the start. 
•	TO-MOVE(s): The player whose turn it is to move in state s. 
•	ACTIONS(s): The set of legal moves in state s. 
•	RESULT(s,a): The transition model, which defines the state resulting from taking action a in state s.
•	IS-TERMINAL(s): A terminal test, which is true when the game is over and false otherwise. States where the game ended are called terminal states.
•	UTILITY(s,p): A utility function (also called an objective function or payoff function), which defines the final numeric value to player p when the game ends in terminal state s. In chess, the outcome is a win, loss, or draw, with values 1, 0, or 1/22. Some games have a wider range of possible outcomes—for example, the payoffs in backgammon range from 0 to 192.
Your solution should work for the board of any configuration from 3×3 board size 5×5 (or even larger size if your machine permits). In a typical tic-tac-toe board game of size 3×3, the smart opponent (utilizing Minimax) tries for a draw (i.e., the value of the root to be 0) which means at the end of the game no 3 triplet cells (in any of the horizontal, vertical, or diagonal direction) have the connecting symbol chosen by a human player. In this game, you can either choose a nought (0) or a cross (X) as your (human player) symbol. However, in a larger board, the end goal changes where the win is for the player who has the larger number of triplets with matching symbols. For example, in this sketch of a 4×4 board on the right, both players still draw the game with the score of 3 each.
The code for this project consists of 3 Python files which you will need to read and understand in order to complete the assignment. You can download all the code and supporting files as a zip folder from homework 2 link given on Canvas (homework_2_code_files.zip).
For this homework, you will work in groups of size between 2 and 4 with the contribution from each member described very clearly in the report in sufficient detail to assign individual grades. Your homework is based on two parts as given below:
1.	Code implemented for initializing board size and other relevant parameters and drawing the board using pygame library. You will need to install pygame and other required libraries in order to successfully complete your code and run the game
2.	Code implemented for multiagent algorithms in given multiAgents.py file (in Minimax and Negamax functions as indicated in detail below)
3.	Code implemented for playing the game in large_board_tic_tac_toe.py (this is where the missing parts of your continuous loop to play till the end will be completed)
4.	A brief report on what you did for each algorithm (i.e., how you implemented with screenshots) 

File Name	Description
multiAgents.py	Where all of your multi-agent search agents will reside.
large_board_tic_tac_toe.py	The main file that runs tic-tac-toe board games. This file should have the Graphical User Interface created via pygame which should provide all the required features. The features should include drawing the board where the user can configure the size of the board, selecting the symbol to be represented with (X or 0), resetting the game, and showing the score and win state for each player at the end of the game. An optional rough sketch of the GUI is provided which can be modified as per needed.
GameStatus_5120.py	Game Status class where the new board state should be generated and functions should be implemented to (i) check if the current state of the board is terminal, (ii) compute the score at each new move by either the human or computer player), (iii) possible new moves (i.e., the board state where the values of each unoccupied cell should be returned as 0), and (iv) the current state of the board should be returned. 

Files to Edit and Submit: You will need to edit and submit all the above files to implement your algorithms. You can also create an executable of the game as an option (not required) to play on different devices with the runtime environment available. Once you have completed the homework, you are welcome to run your game to take screenshots for your report. You can extend the GUI to allow for two human players to play the game. The default option, however, should be a computer player playing against the human. A sample sketch of the GUI expected with your homework is shown. Please feel free to use your artistic skills to develop professional looking GUI which may help the user feel that a professional game is being played.

 
Figure 1: A sample GUI that should be expected from each group. There is not restriction on how the GUI should look like except the minimum functionality as displayed in the above sketch is mentioned. Your GUI can be different with different layouts, placements of buttons and options of your choice. 




Academic Dishonesty: Your code will be checked against other submissions in the class for logical redundancy. If you copy someone else’s code and submit it with minor changes, they will be detected easily, so please do not try that and submit your own work only. In case of cheating, the University’s academic policies on cheating and dishonesty will strictly apply which may result from the deduction in your grade to expulsion.

Getting Help: If you are having difficulty in implementing the algorithms from the pseudocodes provided in this homework, contact the course staff for help. Office hours and Slack are there for your support. If you are not able to attend office hours, then please inform your instructor to arrange for additional time. The intent is to make these projects rewarding and instructional, not frustrating and demoralizing. You can either complete this homework on your own or discuss the problem and collaborate with another member of the class (or different section). Please clearly acknowledge and mention your group member in your homework report submission who you will collaborate with in this homework. Your report and program (search.py file) will be separately submitted by yourself on Canvas irrespective of your collaboration with your group member. Group discussions are encouraged but copying of programs is NOT recommended. Programming based on your own skills is encouraged.

Tasks for homework 2

1.	Minimax search with alpha-beta pruning and Negamax (10%)
Write an adversarial agent in the provided Minimax function in multiAgents.py. Your minimax agent should work with any board size (from 3 to as large as your machine can support with decent response time), so your algorithm should be a more generalized version of the standard Minimax algorithm that we have studied in the class. Your minimax tree will have multiple layers for each player where for larger board size, the depth of even 4 in your Minimax and Negamax implementation can be overwhelming for your machine. Your code should however also be able to expand the tree to an arbitrary depth which can be accessed from depth argument when your Minimax function will be called from your large_board_tic_tac_toe.py file. The score at each turn should be calculated through get_scores() function in GameStatus_5120.py file. Since this will be a large board game where the terminal state will NOT depend on the values of -1 (loss to the opponent), 0 (draw), or 1 (win for the human player), your score function should return a cumulative score where any triplet with matching symbol for each player should increment a value in your returned score which can then be used to show the winner. The score of 0 will still be a draw, whereas a positive (≥ 1) and negative (≤ -1) score will declare the human player to either be a winner or a loser, respectively. For the implementation of Negamax, please see this tutorial to gain some understanding. It should be noted that almost the entire code written for Minimax algorithm should be adoptable for Negamax except the lines where the value propagated from the depth by Minimax is provided in the code. 
Important: A single search ply is considered to be one human move and the opponent’s response, so depth 2 search will involve human and the opponent moving two times. For further reading and understanding of Minimax (including alpha-beta pruning), please see this short video tutorial with pseudo code. 
Hints and Observations
•	Hint: Implement the algorithm recursively using helper function(s).
•	The correct implementation of minimax will lead to the human player losing the game in some tests. This is not a problem: as it is correct behavior. If your human player always loses, then you’re probably being biased and letting your computer program to win intentionally. If your human player never loses, then your Minimax search may not be implemented correctly, your trees search depth is too shallow, or your score calculation is not correct. Make sure the results are not biased.
•	Human player by default assigned X, but you can change it via the GUI to 0 if you like the symbol 0. 
•	All states in minimax should be GameStates, either passed in to getAction or generated via GameStatus_5120.get_new_state(self, new_move). 
Evaluation: Your code will be checked to determine whether it explores the correct number of game states. Your developed game will be played with a randomly chosen human player from other groups and the score will be provided for your code. Your report will still be valuable with whatever level of implementation you accomplish in your submission. A professional looking GUI with a competitive computer player (played by randomly chosen members from the class) on a board larger than 3×3 will earn the highest grade. In order to evaluate your Minimax and Negamax implementation, initially select the size of the board to 3×3 and play the game a few times with different strategies. An optimal Minimax agent should always end the game in a draw and would not let you win. To test and debug your code, you will be expected to run:
python large_board_tic_tac_toe.py
Which should display the GUI, select the board configuration (size), and start playing by selecting any unoccupied cell of the board of choice (initially all should be blank). 
 
Figure 1: Pseudo-code for the implementation of Minimax algorithm. Please use this as a guide only. You will still need to carefully read multiAgents.py file for helper functions given in the comments and think/reason about the implementation of Minimax in your tic-tac-toe game.

 
Figure 2: Pseudo-code for general-purpose implementation of Minimax algorithm. Please use this as a guide only. You will still need to carefully read multiAgents.py file for helper functions given in the comments and think/reason about the implementation of Minimax in your tic-tac-toe game.
In addition to all the above functionality, your Minimax and Negamax functions should implement an adversarial agent in the provided multiAgents.py file to more efficiently explore the minimax tree. Your agent should work with any size of the board (from 3×3 to larger sizes), so your algorithm should be a generalized version of the standard Alpha-Beta Pruning algorithm. The AlphaBeta minimax values should be identical to the MinimaxAgent minimax values, although the actions it selects can vary because of different tie-breaking behavior.
Note: The correct implementation of alpha-beta pruning will lead to the computer agent drawing the game in almost all the tests. This is not a problem: as it is correct behavior.
 
Figure 3: Pseudo-code for the implementation of the algorithm you should implement for this question. Please use this as a guide only. You will still need to carefully read multiAgents.py file for helper functions given in the comments and think/reason about the implementation of Minimax in Pacman scenario.

2.	Constraint satisfaction problems (5%)

1.	(2.5%) Consider the problem of placing k knights on an n×n chess board such that no two knights are attacking each other, where k is given and k ≤ n2.
•	Choose a CSP formulation. What are the variables in your formulation?
•	What are the possible values of each variable in your formulation?
•	What sets of variables are constrained, and how?

2.	(2.5%) At CSUSB, we have 5 vehicles to take transfer students to a trip to the campus: A, B, C, D, and E and two stops: CGI building and JB Hall. Our job would be to schedule a time slot and a stop for each vehicle to either arrive at or leave the stop. The department gave us four possible time slots: {1, 2, 3, 4} for each stop, during which we can schedule a vehicle to arrive or leave. 
Constraints: 
•	Vehicle B has lost its battery and must arrive in time slot 1. 
•	Vehicle D can only arrive or leave during or after time slot 3. 
•	Vehicle A is running low on fuel but can last until at most time slot 2. 
•	Vehicle D must arrive before Vehicle C leaves, because some students must transfer from D to C. 
•	Vehicles A, B, and C cater to students from CGI and can only use the CGI stop. 
•	Vehicles D and E cater to students from JB Hall and can only use the JB Hall stop. 
•	No two vehicles can reserve the same time slot for the same stop. 

1.	Formulate this problem as a CSP where there is one variable per vehicle, reporting the domains and constraints (e.g., the time slots are {1, 2, 3, 4} and stop are {CGI, JB Hall}. Also, list binary constraints on the classes. Your constraints should be specified formally, which should be implicit rather than explicit with words.
2.	Draw the constraint graph for your problem in item 1.
 
Homework 2 (15%)
 
 
 


CSE 5120 – Introduction to Artificial Intelligence – Fall 2025 

 



 
Submitted to  

Department of Computer Science and Engineering
California State University, San Bernardino, California 

 
by

Student name (CSUSB ID)
(Your collaborator in this homework (if any))
 



 
Date: Month Day, Year
 
 
 
 
 
 
Email: 
•	Your email
•	Your collaborator’s email (if you collaborated with any)

 
Report
Brief description of your work here acknowledging your collaboration with your class fellow (or a friend from other CSE 5120 section), and the capacity at which he/she collaborated with you, followed by the algorithms you implemented.
1.	Minimax algorithm with Alpha-Beta pruning
Your brief explanation of the problem, your code solution, and any documentation with screenshots of your code Evaluation 
2.	Negamax algorithm
Your brief explanation of the problem, your code solution, and any documentation with screenshots of your code Evaluation 
3.	Constraint satisfaction problems
Your explanation and drawings, wherever necessary, numbered according to how the questions are defined in the questions. 


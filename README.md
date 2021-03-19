# ai-project-2

## purpose

Leverages ai search practices to solve an 8 number puzzle as shown below with various algorithms & heuristics, and analyzes the results.

![image of 8 puzzle](https://lh3.googleusercontent.com/proxy/d1o2xjQv_59eKJ2SxYTPtlE_22_SUVB3opvy4niRVH2xwswi181tmKyMw4EugGtSIwdEHFadgD0YnCb0Pp1SVqQRl4Mgw5XvDmgt_UBZ35k1SyUJUw)

## Algorithms

This program implements Iterative Deepening Search and A*. A* search with no selected heuristic is a non-informed breadth first search, which takes a very long time to solve. The bad heuristic is based on the number of tiles correctly positioned on the board, this is better than the uninformed search but still takes a long time to solve. The best implemented heuristic is the Manhattan distance of the board, which is the summation of each tile's distance from it's correct position. 

The python script allows you to play a random game with any valid sized board, and also allows you to custom input a board and feeds you instructions to solve it.

## Run

1. install any dependencies by running `make install` from the root directory
2. run the main python script with `python main.py`. Python 3.8.5 was used to develop but older versions will likely run, possibly with different analytical results.
3. Select if you would like to run the algorithm for analytical purposes, or if you would like to input a custom board to have solved
4. Select the algorithm(s) you want to solve the puzzle with
5. Select the logging level you would like the algorithms to use. By default this is silent, verbose and other modes are mainly for development purposes

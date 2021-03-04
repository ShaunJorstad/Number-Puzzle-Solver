# ai-project-2

## purpose

Leverages ai search practices to solve an 8 number puzzle as shown below with various algorithms & heuristics, and analyzes the results.

![image of 8 puzzle](https://www.google.com/url?sa=i&url=http%3A%2F%2Fwww.aiai.ed.ac.uk%2F~gwickler%2Feightpuzzle-uninf.html&psig=AOvVaw1l6uzxNyG9wh5yav4GQGuk&ust=1614971148526000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCPiN7b-ql-8CFQAAAAAdAAAAABAD)

## Algorithms

This program implements BFS brute force and A\* with various heuristics to solve the puzzle.

## Run

1. install any dependencies by running `make install` from the root directory
2. run the main python script with `python main.py`. Python 3.8.5 was used to develop but older versions will likely run, possibly with different analytical results.
3. Select if you would like to run the algorithm for analytical purposes, or if you would like to input a custom board to have solved
4. Select the algorithm(s) you want to solve the puzzle with
5. Select the logging level you would like the algorithms to use. By default this is silent, verbose and other modes are mainly for development purposes

Implementation of the Markov Decision process to calculate the path with maximum utility to be taken by a car in a city by calculating the utilities gained by taking various paths using value iteration with epsilon = 0.1 and gamma = 0.9. 
# Description
The goal is to navigate autonomous cars throughout the city. The cars can move North, South, East, or West. The city can be represented in a grid/ matrix. There will be some obstacles, such as buildings, road closings, etc. If a car crashes into a building or road closure, SpeedRacer has to pay $100. There is also an expenditure of $1 for gas when at each grid location along the way. The cars will start from a given SpeedRacer parking lot, and will end at another parking lot. When the car arrives at the destination parking lot, $100 is received. The goal is to make the most money over time with the greatest likelihood. The cars will go in the correct direction 70% of the time, with a 10% chance of going in each of the other three directions instead.
Input file: 
First line: strictly positive 32-bit integer s, size of grid [grid is a square of size sxs]
Second line: strictly positive 32-bit integer n, number of cars
Third line: strictly positive 32-bit integer o, number of obstacles
Next o lines: 32-bit integer x, 32-bit integer y, denoting the location of obstacles
Next n lines: 32-bit integer x, 32-bit integer y, denoting the start location of each car
Next n lines: 32-bit integer x, 32-bit integer y, denoting the terminal location of each car
Output file:
n lines: 32-bit integer, denoting the mean money earned in simulation for each car, integer result of floor operation

Example:<br/>
Input.txt -<br/>
3<br/>
1<br/>
1<br/>
0,1<br/>
2,0<br/>
0,0<br/>
Output.txt -<br/>
95<br/>
Policy simulation (Optimal direction/turn to be taken when at the position in the grid) -<br/>
(0, 1): (0, -1)<br/>
(1, 2): (0, -1)<br/>
(0, 0): None<br/>
(2, 1): (0, -1)<br/>
(2, 0): (-1, 0)<br/>
(1, 1): (0, -1)<br/>
(2, 2): (0, -1)<br/>
(1, 0): (-1, 0)<br/>
(0, 2): (1, 0)


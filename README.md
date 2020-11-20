# My Journey Planner

A python GUI project with implementation of advanced Data Structures and Algorithms.

## Topic : Designing, developing and testing a journey planner model for a hypothetical Underground train network.

### Description :
The City Underground tube system is a complex interconnection of stations across the
city area. You are provided with a standard map in pdf format that depicts the network. You may assume that the trains operate from 05:00 until midnight each day. 

## Data Structures Used : Linked List, array
A graph can be represented in List and a Matrix form. Both with its own merits, and pitfalls.
To represent the train system if the city, here we've used List Representation of the nodes in the graph.
List representation not only gives better time complexity, it makes things easier to be interpreted.
In the form 
```
graph = Network(["A","B", 2], ["X","Y",4])
```
This states that there is an edge between A and B and likewise between X and Y, with the travelling time as 2 minutes, and 4 minutes respectively.

## Algorithm Used : Dijkstra Algorithm
Dijkstra Algorithm is a graph search algorithm, which makes searching the shortest path from a single source, with non-negative edges. Thereby producing the shortest path tree out of the graph.

### Limitations
1. It may not give the shortest path, when the weights are negative.

### Dijkastra Algorithm

Important points:
1. Finds the shortest path between two nodes in a graph.
2. Graphs can be directed, or undirected.
3. Uses a greedy approach.
4. Greedy doesn't always provide the optimal solution, so Dijkstra also has drawbacks.
5. Fails for negative weights.
6. Uses a relaxation method to minimise the distance, in case it gets two distances for same end point
7. Time complexity is O(N^2).

## Software implementation

Technical aspects : 
- Python version - 3.6.9
- Tkinter version - 8.6

Details : 
1. The user must enter the exact name of the starting and ending stations, even a small typo could not yield the correct path.
2. In some instances, it may not show the path from A to B, try reversing the order. If there exists a path, it will show from B to A.

It is difficult to evaluate the correctness of the calculated sub-routes
The time complexity of this implementation is O(N*E), where N-> Number of nodes, and E-> Number of edges. On providing a starting point (A), it goes on searching all the nodes which start from A. Searching for all connected nodes internally. It also uses relaxation method, incase a node is visited more than once.


Currently, there is no hard limit for choosing the lines from the first two dropdown. It is automatically decided based on the shortest path.
Even if the To-and-From stations are not according to the previously opted lines (from dropdown), the algorithm works effectively.      

Valid Travelling time : The valid travelling is taken from 5am in morning to 12pm at midnight. Even with this, the To-From section will open only if you've atleast 30 minutes reserved for unprecedented reasons. So actual travellling time is between 5am in morning to 11:30pm at night

If your travel involves too many intermediate stops, the second popup width may be insufficient to show the entire range of intermediate stations. In those cases, you should resize the popup window according to your convienience, so that all intermediate stations are visible.


### How to use the Application : 
1. From the first dropdown menu, choose your starting Line
2. From the second dropdown menu, choose your destination Line
3. Select the time you wish to commute in the third input box in 24hr format.
Eg. if you wish to travel at 3pm in afternoon, fill 1500, or if it is 8:30pm in evening fill 2030
4. With all above information, click the "Submit" button.
5. On submitting, you need to fill two text boxes with the names of the start and destination station
Note : 
1. Make sure, there is no typo in those.
2. If there exists no path from start to finish, or there is a typo it will show error
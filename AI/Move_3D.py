import heapq
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Math import Math
from Settings import *
import random


class Node:
    def __init__(self, position, g=0, h=0, parent=None):
        self.position = position  # position (x, y) in the grid
        self.g = g  # cost from start to this node
        self.h = h  # heuristic cost from this node to the goal
        self.f = g + h  # total cost (f = g + h)
        self.parent = parent  # parent node to trace the path back

    def __lt__(self, other):
        return self.f < other.f  # for heapq priority queue sorting


class Pathfinding:
    def __init__(self, grid):
        self.grid = grid  # grid should be a 2D array (0 = walkable, 1 = obstacle)
        self.rows = len(grid)
        self.cols = len(grid[0])

    def get_neighbors(self, node):
        neighbors = []
        x, y = node.position
        # Define possible moves (up, down, left, right)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 4 directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.rows and 0 <= ny < self.cols and self.grid[nx][ny] == 0:  # Check if within bounds and walkable
                neighbors.append(Node((nx, ny)))
        return neighbors

    def a_star(self, start, goal):
        open_list = []
        closed_list = set()

        start_node = Node(start)
        goal_node = Node(goal)

        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)

            # If we reached the goal, we trace the path back
            if current_node.position == goal_node.position:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]  # Reverse the path to start-to-goal order

            closed_list.add(current_node.position)

            for neighbor in self.get_neighbors(current_node):
                if neighbor.position in closed_list:
                    continue

                neighbor.g = current_node.g + 1  # Assuming each step costs 1
                neighbor.h = abs(neighbor.position[0] - goal_node.position[0]) + abs(neighbor.position[1] - goal_node.position[1])  # Manhattan distance heuristic
                neighbor.parent = current_node

                if not any(neighbor.position == open_node.position and neighbor.f >= open_node.f for open_node in open_list):
                    heapq.heappush(open_list, neighbor)

        return []  # Return empty path if no path found

class Movement:
    def __init__(self, pathfinding: Pathfinding):
        self.pathfinding = pathfinding
        self.current_position = (0, 0)

    def Move_To(self, your_position, target_position):
        path = self.pathfinding.a_star(your_position, target_position)
        return path

    def Move_Random_Direction(self, your_position):
        direction = Math.Vector3(random.randint(-1, 1) * random.random(),
                                 random.randint(-1, 1) * random.random(),
                                 random.randint(-1, 1) * random.random())
        return your_position + direction
    

grid = [
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0]
]

pathfinding = Pathfinding(grid)
movement = Movement(pathfinding)

start = (0, 0)
goal = (4, 4)

path = movement.Move_To(start, goal)
print(f"Path from {start} to {goal}: {path}")

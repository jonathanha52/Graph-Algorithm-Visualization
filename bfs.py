import numpy as np
import pygame
from matrixhelper import *

class BFS:
    def __init__(self):
        self.parent = {}
        self.visited = []
        self.waiting = []
        self.path = []
    def __pathing(self, start, end):
        path = []
        dest = end
        while path[0] != start:
            path.insert(0, self.parent[dest])
            dest = self.parent[dest]
        return path
    def search(self, maze, start, end, callback):
        self.waiting.append(start)
        while self.waiting:
            #print('.')
            frontier = self.waiting.pop(0)
            if frontier == end:
                self.path = self.__pathing(start, end)
                return
            self.visited.append(start)
            successor = [x for x in getNeighbors_pf(start) if maze[x] == 1 and x not in self.visited]
            for v in successor:
                self.waiting.append(v)
                self.parent[v] = frontier
            pygame.event.pump()
            callback(maze, None, self.visited, None)
'''
DOCSTRING TO BE ADDED
'''
import pygame
import time
import numpy
from random import randrange
from matrixhelper import *
#from bfs import BFS
pygame.font.init()
pygame.init()
pygame.display.set_caption('Maze')
#-------------------------------------------------------
WIDTH = 800
HEIGHT = 600
CELLW = 19
CELLH = 19
PADDING = 1
GRID_SIZE = (30,30)
BASE = pygame.display.set_mode((WIDTH,HEIGHT))
MAZE = numpy.zeros(GRID_SIZE)
FNT = pygame.font.SysFont('Calibri', 14)
TXT_OFFSET = 7
#-------------------------------------------------------
WHITE = 255,255,255
BLACK = 0,0,0
BLUE = 72, 77, 224
GREEN = 72, 224, 90
RED = 255, 41, 41
YELLOW = 200, 245, 66
GRAY = 125, 122, 114
#-------------------------------------------------------
BASE.fill(BLACK)
run = True
choose_start = False
choose_end = False
start_point = None
end_point = None
#-------------------------------------------------------
waiting = []
visited = []
parent = {}
path = []
#-------------------------------------------------------
KEY_CHOOSESTART = pygame.K_LCTRL
KEY_CHOOSEEND = pygame.K_LALT
#-------------------------------------------------------
BTN_CLEAR_PATH = pygame.rect.Rect(650,30, 100, 40)
BTN_RESET = pygame.rect.Rect(650,100, 100, 40)
BTN_GENERATE = pygame.rect.Rect(650,170, 100, 40)
BTN_BFS = pygame.rect.Rect(650,240, 100, 40)
BTN_DFS = pygame.rect.Rect(650,310, 100, 40)
BTN_ASTAR = pygame.rect.Rect(650,380,100,40)
BTN_GREEDY = pygame.rect.Rect(650,450,100,40)
TXT_CLEAR_PATH = FNT.render('Clear path', True, WHITE)
TXT_GENERATE = FNT.render('Generate', True, WHITE)
TXT_RESET = FNT.render('Reset', True, WHITE)
TXT_BFS = FNT.render('BFS', True, WHITE)
TXT_DFS = FNT.render('DFS', True, WHITE)
TXT_ASTAR = FNT.render('A*', True, WHITE)
TXT_GREEDY = FNT.render('Greedy', True, WHITE)
#-------------------------------------------------------
def button_render(btn, txt):
    pygame.draw.rect(BASE, BLUE, btn)
    BASE.blit(txt, (btn.centerx-TXT_OFFSET, btn.centery-TXT_OFFSET))
def draw_cell(matrix, frontier = None):
    for row in range(GRID_SIZE[0]):
        for column in range(GRID_SIZE[1]):
            cell = pygame.rect.Rect(column*(CELLW+PADDING) + PADDING,row*(CELLH+PADDING) + PADDING,CELLW,CELLH)
            if matrix[row][column] == 0:
                color = BLACK
            elif matrix[row][column] == 1:
                color = WHITE
            try:
                if (row, column) in waiting:
                    color = BLUE
                if (row, column) in visited:
                    color = GRAY
                if (row, column) in path:
                    color = YELLOW
            except Exception as e:
                pass
            if (row, column) == start_point:
                color = GREEN
            if (row, column) == end_point:
                color = RED
            pygame.draw.rect(BASE, color, cell)
    pygame.display.flip()
def prim(start: tuple):
    #print(start)
    MAZE[start] = 1
    frontier = getNeighbors_prim(start)
    while frontier:
        i = randrange(len(frontier))
        cell_idx = frontier[i]
        frontier.pop(i)
        neighbors = [x for x in getNeighbors_prim(cell_idx) if isValid(x,MAZE.shape[0], MAZE.shape[1])]
        #print(neighbors)
        neighbors = [x for x in neighbors if MAZE[x] == 1] 
        #print(f'Neighbor: {neighbors}')
        try:
            j = randrange(len(neighbors))
            choosen_neighbor = neighbors[j]
            middle = getMiddle(choosen_neighbor, cell_idx)
            if isValid(cell_idx,MAZE.shape[0], MAZE.shape[1]) and MAZE[cell_idx] == 0:
                if isValid(middle,MAZE.shape[0], MAZE.shape[1]):
                    MAZE[middle] = 1
            if isValid(cell_idx,MAZE.shape[0], MAZE.shape[1]):
                frontier = frontier + [x for x  in getNeighbors_prim(cell_idx) if MAZE[x] == 0]
        except Exception as e:
            pass
        if isValid(cell_idx,MAZE.shape[0], MAZE.shape[1]):
            MAZE[cell_idx] = 1
        #print(f'Frontier: {frontier}')
        draw_cell(MAZE, middle)
        pygame.event.pump()
        time.sleep(0.001)
def bfs_search(start, end):
    print(start, end)
    waiting.clear()
    waiting.append(start)
    while waiting:
        #print('.')
        frontier = waiting.pop(0)
        #print(f'Frontier: {frontier}')
        if frontier == end:
            path.clear()
            path.append(end)
            dest = end
            while path[0] != start:
                path.insert(0, parent[dest])
                dest = parent[dest]
                draw_cell(MAZE)
            return
        visited.append(frontier)
        successor = [x for x in getNeighbors_pf(frontier) if isValid(x, MAZE.shape[0], MAZE.shape[1]) and x not in visited]
        successor = [x for x in successor if MAZE[x] == 1]
        #print(f'Successor: {successor}')
        for v in successor:
            waiting.append(v)
            parent[v] = frontier
        draw_cell(MAZE)
        pygame.event.pump()
        time.sleep(0.01)
def dfs_search(start, end):
    print(start, end)
    waiting.clear()
    waiting.append(start)
    while waiting:
        #print('.')
        frontier = waiting.pop()
        #print(f'Frontier: {frontier}')
        if frontier == end:
            path.clear()
            path.append(end)
            dest = end
            while path[0] != start:
                path.insert(0, parent[dest])
                dest = parent[dest]
                draw_cell(MAZE)
            return
        visited.append(frontier)
        successor = [x for x in getNeighbors_pf(frontier) if isValid(x, MAZE.shape[0], MAZE.shape[1]) and x not in visited]
        successor = [x for x in successor if MAZE[x] == 1]
        #print(f'Successor: {successor}')
        for v in successor:
            waiting.append(v)
            parent[v] = frontier
        draw_cell(MAZE)
        pygame.event.pump()
        time.sleep(0.01)
def astar_search(start, end):
    waiting.clear()
    waiting.append(start)
    fScore = {}
    gScore = {}
    for idx, value in numpy.ndenumerate(MAZE):
        if value == 1:
            fScore[idx] = 999
            gScore[idx] = 999
    fScore[start] = l2(start, end)
    gScore[start] = 0
    while waiting:
        waiting.sort(key = lambda x:fScore[x])
        frontier = waiting.pop(0)
        if frontier == end:
            path.clear()
            path.append(end)
            dest = end
            while path[0] != start:
                path.insert(0, parent[dest])
                dest = parent[dest]
                draw_cell(MAZE)
            return
        visited.append(frontier)
        successor = [x for x in getNeighbors_pf(frontier) if isValid(x, MAZE.shape[0], MAZE.shape[1]) and x not in visited]
        successor = [x for x in successor if MAZE[x] == 1]
        for v in successor:
            tentative_gScore = gScore[frontier] + l2(v,frontier)
            if tentative_gScore < gScore[v]:
                gScore[v] = tentative_gScore
                fScore[v] = gScore[v] + l2(v,end)
                parent[v] = frontier
                waiting.append(v)
        draw_cell(MAZE)
        pygame.event.pump()
        time.sleep(0.01)
def greedy_searcher(start, end):
    waiting.clear()
    waiting.append(start)
    '''
    for idx, value in numpy.ndenumerate(MAZE):
        if value == 1:
            fScore[idx] = 99
            gScore[idx] = 99
    fScore[start] = l2(start, end)
    gScore[start] = 0
    '''
    while waiting:
        waiting.sort(key = lambda x:l2(x,end))
        frontier = waiting.pop(0)
        if frontier == end:
            path.clear()
            path.append(end)
            dest = end
            while path[0] != start:
                path.insert(0, parent[dest])
                dest = parent[dest]
                draw_cell(MAZE)
            return
        visited.append(frontier)
        successor = [x for x in getNeighbors_pf(frontier) if isValid(x, MAZE.shape[0], MAZE.shape[1]) and x not in visited]
        successor = [x for x in successor if MAZE[x] == 1]
        for v in successor:
            parent[v] = frontier
            waiting.append(v)
        draw_cell(MAZE)
        pygame.event.pump()
        time.sleep(0.01)
#-------------------------------------------------------
while run: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == KEY_CHOOSESTART:
                choose_start = True
            if event.key == KEY_CHOOSEEND:
                choose_end = True
        elif event.type == pygame.KEYUP:
            if event.key == KEY_CHOOSESTART:
                choose_start = False
            if event.key == KEY_CHOOSEEND:
                choose_end = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cell_x = mouse_x//(CELLW+PADDING)
            cell_y = mouse_y//(CELLH+PADDING)
            if event.button == 1:
                if BTN_GENERATE.collidepoint(mouse_x,mouse_y):
                    if not 1 in MAZE:
                        prim(start_point)
                if BTN_RESET.collidepoint(mouse_x,mouse_y):
                    MAZE = MAZE*0
                    start_point = None
                    end_point = None
                if BTN_CLEAR_PATH.collidepoint(mouse_x,mouse_y):
                    waiting.clear()
                    visited.clear()
                    path.clear()
                    parent.clear()
                if BTN_BFS.collidepoint(mouse_x,mouse_y):
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                    if start_point != None and end_point != None:
                        bfs_search(start_point, end_point)
                    pygame.event.set_allowed(pygame.MOUSEMOTION)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                if BTN_DFS.collidepoint(mouse_x,mouse_y):
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                    if start_point != None and end_point != None:
                        dfs_search(start_point, end_point)
                    pygame.event.set_allowed(pygame.MOUSEMOTION)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                if BTN_ASTAR.collidepoint(mouse_x,mouse_y):
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                    if start_point != None and end_point != None:
                        astar_search(start_point, end_point)
                    pygame.event.set_allowed(pygame.MOUSEMOTION)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                if BTN_GREEDY.collidepoint(mouse_x,mouse_y):
                    pygame.event.set_blocked(pygame.MOUSEMOTION)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
                    if start_point != None and end_point != None:
                        greedy_searcher(start_point, end_point)
                    pygame.event.set_allowed(pygame.MOUSEMOTION)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
                    pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
                if choose_start:
                    start_point = cell_y, cell_x
                if choose_end:
                    if MAZE[cell_y][cell_x] == 1:
                        end_point = cell_y, cell_x
                        
    BASE.fill(BLACK)
    button_render(BTN_CLEAR_PATH, TXT_CLEAR_PATH)
    button_render(BTN_RESET, TXT_RESET)
    button_render(BTN_GENERATE, TXT_GENERATE)
    button_render(BTN_BFS, TXT_BFS)
    button_render(BTN_DFS, TXT_DFS)
    button_render(BTN_ASTAR, TXT_ASTAR)
    button_render(BTN_GREEDY, TXT_GREEDY)
    #pygame.draw.rect(BASE, BLUE, BTN_CLEAR_PATH)
    #pygame.draw.rect(BASE, BLUE, BTN_RESET)
    #pygame.draw.rect(BASE, BLUE, BTN_GENERATE)
    #pygame.draw.rect(BASE, BLUE, BTN_BFS)
    #pygame.draw.rect(BASE, BLUE, BTN_BFS)
    #BASE.blit(TXT_CLEAR_PATH, (BTN_CLEAR_PATH.centerx-TXT_OFFSET, BTN_CLEAR_PATH.centery-TXT_OFFSET))
    #BASE.blit(TXT_RESET, (BTN_RESET.centerx-TXT_OFFSET, BTN_RESET.centery-TXT_OFFSET))
    #BASE.blit(TXT_GENERATE, (BTN_GENERATE.centerx-TXT_OFFSET, BTN_GENERATE.centery-TXT_OFFSET))
    #BASE.blit(TXT_BFS, (BTN_BFS.centerx-TXT_OFFSET, BTN_BFS.centery-TXT_OFFSET))
    #BASE.blit(TXT_DFS, (BTN_BFS.centerx-TXT_OFFSET, BTN_BFS.centery-TXT_OFFSET))
    draw_cell(MAZE)
pygame.quit()
#-------------------------------------------------------
#-------------------------------------------------------

#-------------------------------------------------------







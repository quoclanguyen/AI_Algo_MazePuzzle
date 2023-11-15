from queue import PriorityQueue
import time
import pygame
import numpy as np
from colors import colors
colorData = colors()

def move(GUI, Grid, came_from, current):
    rectList = []
    while current in came_from:
        current = came_from[current]
        if Grid.get(current[0], current[1]) == Grid.start:
            continue  
        if Grid.get(current[0], current[1]) == Grid.key:
            continue  
        Grid.set(current[0], current[1], Grid.gpath)
        rect = [
            GUI.margin + (GUI.margin + GUI.grid.width) * current[1], 
            GUI.margin + (GUI.margin + GUI.grid.height) * current[0], 
            GUI.grid.width, 
            GUI.grid.height
        ]
        rectList.append((rect, current[0], current[1]))
    for rect in rectList[::-1]:
        time.sleep(0.03)
        color = GUI.screen.get_at((rect[0][0] + 4, rect[0][1] + 4))[:3]
        if color == colorData.gridColors[Grid.gpath]:
            pygame.draw.rect(GUI.screen, colorData.darkerPath, rect[0])
        else:
            pygame.draw.rect(GUI.screen, colorData.gridColors[Grid.gpath], rect[0])
        pygame.display.update()
        pygame.display.flip()
    return len(rectList) + 1

def heuristics(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def find_path_with_key(GUI, Grid, algo):
    start, end = Grid.findSGPoint()
    keys = Grid.findKeys()
    if algo == "A-star":
        keys.sort(key = lambda x: heuristics(start, x))
    keys.insert(0, start)
    keys.append(end)
    
    algo_name = {
        "A-star": "a_star", 
        "BFS": "bfs", 
        "DFS": "dfs", 
        "UCS": "ucs"
    }
    algo_details = []
    
    if len(keys) != 2:
        Grid.set(*end, Grid.wall)
        for i in range(len(keys) - 2):
            s = keys[i]
            e = keys[i + 1]
            algo_details += globals()[algo_name[algo]](GUI, Grid, s, e)
            if algo_details[0] == 0:
                break
        Grid.set(*end, Grid.goal)
        if algo_details[0] != 0:
            algo_details += globals()[algo_name[algo]](GUI, Grid, keys[-2], keys[-1])
    else:
        algo_details += globals()[algo_name[algo]](GUI, Grid, start, end)
    
    total_moves = sum(algo_details[::2])
    nodes_visited = sum(algo_details[1:2])
    print("Moves played with {}:".format(algo), total_moves)
    print("Nodes visited: {}\n".format(nodes_visited))

def a_star(GUI, Grid, start, end):
    Grid.generateNeighbors()
            
    count = 0
    states = PriorityQueue()
    states.put((0, count, start))
    states_history = {start}
    came_from = {}

    # inf inf inf
    # inf 0   inf --> g = 0 at the start point
    # inf inf inf

    # inf inf inf
    # inf h   inf --> f = heuristics(...) at the start point
    # inf inf inf

    g_score = [float("inf") for row in Grid.data for _ in row]
    g_score[start[0]*Grid.size + start[1]] = 0
    f_score = [float("inf") for row in Grid.data for _ in row]
    f_score[start[0]*Grid.size + start[1]] = heuristics(start, end)

    while not states.empty():
        current = states.get()[2] # start point
        states_history.remove(current)
        if current == end:
            return move(GUI, Grid, came_from, end), count
        for nei in Grid.neighbors[current[0]*Grid.size + current[1]]: # grid around current point
            temp_g_score = g_score[current[0]*Grid.size + current[1]] + 1
            if temp_g_score < g_score[nei[0]*Grid.size + nei[1]]:
                came_from[nei] = current
                g_score[nei[0]*Grid.size + nei[1]] = temp_g_score
                f_score[nei[0]*Grid.size + nei[1]] = temp_g_score + heuristics(nei, end)   # f = g + h
                if nei not in states_history:
                    count += 1
                    states.put((f_score[nei[0]*Grid.size +nei[1]], count, nei))
                    states_history.add(nei)
    return 0, 0

def ucs(GUI, Grid, start, end):
    Grid.generateNeighbors()
            
    count = 0
    states = PriorityQueue()
    states.put((0, count, start))
    states_history = {start}
    came_from = {}

    g_score = [float("inf") for row in Grid.data for _ in row]
    g_score[start[0] * Grid.size + start[1]] = 0

    while not states.empty():
        current = states.get()[2] # start point
        states_history.remove(current)
        if current == end:
            return move(GUI, Grid, came_from, end), count
        for nei in Grid.neighbors[current[0]*Grid.size + current[1]]: # grid around current point
            temp_g_score = g_score[current[0]*Grid.size + current[1]] + 1
            if temp_g_score < g_score[nei[0]*Grid.size + nei[1]]:
                came_from[nei] = current
                g_score[nei[0]*Grid.size + nei[1]] = temp_g_score
                if nei not in states_history:
                    count += 1
                    states.put((g_score[nei[0]*Grid.size + nei[1]], count, nei))
                    states_history.add(nei)
    return 0, 0

def bfs(GUI, Grid, start, end):
    Grid.generateNeighbors()

    count = 0
    states = []
    states.append((count, start))
    states_history = {start}
    came_from = {}

    while len(states) != 0:
        current = states.pop(0)[1]
        if current == end:
            came_from.pop(start)
            return move(GUI, Grid, came_from, end), count
        for nei in Grid.neighbors[current[0]*Grid.size + current[1]]: # grid around current point
            if (nei in came_from):
                if (came_from[nei] not in came_from):
                    came_from[nei] = current
            else:
                came_from[nei] = current

            if nei not in states_history:
                count += 1
                states.append((count, nei))
                states_history.add(nei)
    return 0, 0

def dfs(GUI, Grid, start, end):
    Grid.generateNeighbors()
    count = 0
    states = []
    states.append((count, start))
    states_history = {start}
    came_from = {}

    while len(states) != 0:
        current = states.pop()[1]
        if current == end:
            came_from.pop(start)
            return move(GUI, Grid, came_from, end), count
        for nei in Grid.neighbors[current[0]*Grid.size + current[1]]: # grid around current point
            if (nei in came_from):
                if (came_from[nei] not in came_from):
                    came_from[nei] = current
            else:
                came_from[nei] = current

            if nei not in states_history:
                count += 1
                states.append((count, nei))
                states_history.add(nei)
    return 0, 0
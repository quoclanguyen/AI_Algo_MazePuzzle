from queue import PriorityQueue
import time
import pygame
import numpy as np
from colors import colors

colorData = colors()
speed = 0.01

def stimulate(GUI, nei):
    GUI.grid.set(*nei, GUI.grid.stimulate)
    rect = calcRect(GUI, nei)
    time.sleep(speed)
    pygame.draw.rect(GUI.screen, colorData.gridColors[GUI.grid.stimulate], rect)
    pygame.display.update()

def calcDirection(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    if (x2 == x1):
        return "right" if y2 > y1 else "left"
    return "down" if x2 > x1 else "up"

def calcRect(GUI, current):
    rect = [
        GUI.margin + (GUI.margin + GUI.grid.width) * current[1], 
        GUI.margin + (GUI.margin + GUI.grid.height) * current[0], 
        GUI.grid.width, 
        GUI.grid.height
    ]
    return rect

def move(GUI, Grid, came_from, current):
    global speed
    rectList = []
    while current in came_from:
        rect = calcRect(GUI, current)
        current = came_from[current]
        if Grid.get(current[0], current[1]) != Grid.start and Grid.get(current[0], current[1]) != Grid.key:
            Grid.set(current[0], current[1], Grid.gpath)
        if Grid.get(current[0], current[1]) == Grid.key:
            continue
        rectList.append((rect, current))
    rectList.reverse()
    for i in range(len(rectList) - 1):
        time.sleep(speed)
        pygame.draw.rect(GUI.screen, colorData.gridColors[Grid.gpath], rectList[i][0])
        playerPath = "./images/player_{}.png".format(calcDirection(rectList[i][1], rectList[i + 1][1]))
        playerImg = pygame.image.load(playerPath).convert_alpha()
        playerImg = pygame.transform.scale(playerImg, (Grid.width, Grid.height))
        GUI.screen.blit(playerImg, rectList[i][0])
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
    if algo == "Astar":
        keys.sort(key = lambda x: heuristics(start, x))
    keys.insert(0, start)
    keys.append(end)
    
    algo_name = {
        "Astar": "a_star", 
        "BFS": "bfs", 
        "DFS": "dfs", 
        "UCS": "ucs",
        "Greedy": "greedy",
        "ID": "ideep",
        "Beam": "beam"
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
    rect = GUI.buttons["Exit"].rect
    infoX = rect.x - 70
    infoY = rect.y + 100
    rect = [
        infoX,
        infoY,
        1000,
        50
    ]
    pygame.draw.rect(GUI.screen, colorData.bgColor, rect)
    infoMove = GUI.font.render(
        "Moves played with {}: {}".format(algo, total_moves),
        True,
        colorData.darkerPath
    )
    GUI.screen.blit(
        infoMove, 
        (infoX, infoY))
    infoMove = GUI.font.render(
        "Nodes visited: {}".format(nodes_visited),
        True,
        colorData.darkerPath
    )
    GUI.screen.blit(
        infoMove, 
        (infoX, infoY + 20))

def a_star(GUI, Grid, start, end):
    Grid.generateNeighbors()
    # keys = Grid.findKeys()
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
                    if nei != end:
                        stimulate(GUI, nei)
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
                    if nei != end:
                        stimulate(GUI, nei)
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
                if nei != end:
                    stimulate(GUI, nei)
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
                if nei != end:
                    stimulate(GUI, nei)
    return 0, 0

def greedy(GUI, Grid, start, end):
    Grid.generateNeighbors()

    count = 0
    states = PriorityQueue()
    states.put((0, count, start))
    states_history = {start}
    came_from = {}

    f_score = [float("inf") for row in Grid.data for _ in row]
    f_score[start[0]*Grid.size + start[1]] = heuristics(start, end)

    while not states.empty():
        current = states.get()[2] # start point
        if current == end:
            came_from.pop(start, None)
            return move(GUI, Grid, came_from, end), count
        for nei in Grid.neighbors[current[0]*Grid.size + current[1]]: # grid around current point
            f_score[nei[0]*Grid.size + nei[1]] = heuristics(nei, end) 
            if nei not in states_history:
                came_from[nei] = current
                count += 1
                states.put((f_score[nei[0]*Grid.size + nei[1]], count, nei))
                states_history.add(nei)
                if nei != end:
                    stimulate(GUI, nei)
    return 0, 0

def ideep(GUI, Grid, start, end):
    Grid.generateNeighbors()
    count = 0
    states = []
    states.append((count, start))
    states_history = {start}
    came_from = {}
    depth = 0
    depth_limit = 2
    depth_limit_max = (Grid.size ** 2)
    while depth_limit <= depth_limit_max:
        states_history.clear()
        while len(states) != 0:
            current = states.pop()[1]
            depth += 1
            if current == end:
                came_from.pop(start)
                return move(GUI, Grid, came_from, end), count
            if depth == depth_limit:
                break
            for nei in Grid.neighbors[current[0]*Grid.size + current[1]]:
                if (nei in came_from):
                    if (came_from[nei] not in came_from):
                        came_from[nei] = current
                else:
                    came_from[nei] = current
                if nei not in states_history:
                    count += 1
                    states.append((count, nei))
                    states_history.add(nei)
                    if nei != end and nei != start:
                        stimulate(GUI, nei)
        if len(states) == 0:
            states.append((count, start))
        depth = 0
        depth_limit += depth_limit_max / 5
    return 0, 0

def beam(GUI, Grid, start, end):
    Grid.generateNeighbors()

    count = 0
    states = PriorityQueue()
    states.put((0, count, start))
    states.put((0, count, start))
    states_history = {start}
    came_from = {}

    f_score = [float("inf") for row in Grid.data for _ in row]
    f_score[start[0]*Grid.size + start[1]] = heuristics(start, end)

    while not states.empty():
        current_first = states.get()[2] # start point
        if states.qsize() < 2: 
            current_second = current_first
        else:
            current_second = states.get()[2]
        if current_first == end:
            came_from.pop(start, None)
            return move(GUI, Grid, came_from, end), count
        if current_second == end:
            came_from.pop(start, None)
            return move(GUI, Grid, came_from, end), count
        for nei in Grid.neighbors[current_first[0]*Grid.size + current_first[1]]:
            f_score[nei[0]*Grid.size + nei[1]] = heuristics(nei, end)
            if nei not in states_history:
                came_from[nei] = current_first
                count += 1
                states.put((f_score[nei[0]*Grid.size + nei[1]], count, nei))
                states_history.add(nei)
                if nei != end:
                    stimulate(GUI, nei)
        for nei in Grid.neighbors[current_second[0]*Grid.size + current_second[1]]:
            f_score[nei[0]*Grid.size + nei[1]] = heuristics(nei, end)
            if nei not in states_history:
                came_from[nei] = current_second
                count += 1
                states.put((f_score[nei[0]*Grid.size + nei[1]], count, nei))
                states_history.add(nei)
                if nei != end:
                    stimulate(GUI, nei)
    return 0, 0
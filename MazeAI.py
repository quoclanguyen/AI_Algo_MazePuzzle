from queue import PriorityQueue

def move(Grid, came_from, current):
    while current in came_from:
        current = came_from[current]
        if Grid.get(current[0], current[1]) == Grid.start:
            continue  
        Grid.set(current[0], current[1], Grid.gpath)

def heuristics(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(Grid):
    start, end = Grid.findSGPoint()
    Grid.generateNeighbors()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    open_set_history = {start}
    came_from = {}

    g_score = [float("inf") for row in Grid.data for spot in row]
    g_score[start[0]*33 + start[1]] = 0
    f_score = [float("inf") for row in Grid.data for spot in row]
    f_score[start[0]*33 + start[1]] = heuristics(start, end)

    while not open_set.empty():
        current = open_set.get()[2]
        print(current)
        open_set_history.remove(current)
        if current == end:
            move(Grid, came_from, end)
            return True
        for nei in Grid.neighbors[current[0]*33 +current[1]]:
            temp_g_score = g_score[current[0]*33 +current[1]] + 1
            if temp_g_score < g_score[nei[0]*33 +nei[1]]:
                came_from[nei] = current
                g_score[nei[0]*33 +nei[1]] = temp_g_score
                f_score[nei[0]*33 +nei[1]] = temp_g_score + heuristics(nei, end)
                if nei not in open_set_history:
                    count += 1
                    open_set.put((f_score[nei[0]*33 +nei[1]], count, nei))
                    open_set_history.add(nei)
    print(Grid.data)
    print(open_set.empty())
    return False
    
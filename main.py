from MazeGUI import MazeGUI
import numpy as np

margin = 2
size = 100
gridHeight = round(16 / (1 + np.exp(-0.00001 * (size - 12))))

height = (gridHeight + margin) * size + margin
width = height + size * 3 

app = MazeGUI(width, height, margin, size, 'Maze Project')
app.setGridSize(gridHeight, gridHeight)
app.mainLoop()
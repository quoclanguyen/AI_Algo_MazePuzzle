from MazeGUI import MazeGUI

gridSize = 15
margin = 3
size = 33

height = (gridSize + margin) * size + margin
width = round(height * 1.8)

app = MazeGUI(width, height, margin, 'Maze Project')
app.setGridSize(gridSize, gridSize)
app.mainLoop()


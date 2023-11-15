from MazeGUI import MazeGUI
import numpy as np

class MazeApp:
    def __init__(self, size):
        self.margin = 3
        self.size = size
        self.gridHeight = 30

        self.height = 1000
        self.width = 800

        self.app = MazeGUI(self.width, self.height, self.margin, size, 'Maze Project')
        self.app.setGridSize(self.gridHeight, self.gridHeight)
        self.app.mainLoop()

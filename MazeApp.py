from MazeAIGUI import MazeAIGUI
from MazePlayerGUI import MazePlayerGUI
class MazeApp:
    def __init__(self, size, width, height, mode):
        self.margin = 1
        self.width = width
        self.height = height
        self.mode = mode

        self.size = size
        self.gridHeight = round((self.height - self.margin) / self.size) - self.margin
        if self.mode == "ai":
            self.app = MazeAIGUI(self.width, self.height, self.margin, self.size, 'Maze Project')
            self.app.setGridSize(self.gridHeight, self.gridHeight)
            self.app.mainLoop()
        else:
            self.app = MazePlayerGUI(self.width, self.height, self.margin, self.size, 'Maze Project')
            self.app.setGridSize(self.gridHeight, self.gridHeight)
            self.app.mainLoop()

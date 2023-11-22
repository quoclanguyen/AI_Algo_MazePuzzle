from MazeAIGUI import MazeAIGUI
class MazeApp:
    def __init__(self, size, width, height):
        self.margin = 1
        self.width = width
        self.height = height

        self.size = size
        self.gridHeight = round((self.height - self.margin) / self.size) - self.margin

        self.app = MazeAIGUI(self.width, self.height, self.margin, self.size, 'Maze Project')
        self.app.setGridSize(self.gridHeight, self.gridHeight)
        self.app.mainLoop()

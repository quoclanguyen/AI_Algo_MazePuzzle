from MazeAIGUI import MazeAIGUI
class MazeApp:
    def __init__(self, size):
        self.margin = 1
        self.width = 1200
        self.height = 900

        self.size = size
        self.gridHeight = round((self.height - self.margin) / self.size) - self.margin
        print(self.gridHeight)

        self.app = MazeAIGUI(self.width, self.height, self.margin, self.size, 'Maze Project')
        self.app.setGridSize(self.gridHeight, self.gridHeight)
        self.app.mainLoop()

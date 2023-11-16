from MazeGUI import MazeGUI
class MazeApp:
    def __init__(self, size):
        self.margin = 3
        self.size = size
        self.gridHeight = 30

        self.width = 1000
        self.height = 800
    
        self.app = MazeGUI(self.width, self.height, self.margin, self.size, 'Maze Project')
        self.app.setGridSize(self.gridHeight, self.gridHeight)
        self.app.mainLoop()

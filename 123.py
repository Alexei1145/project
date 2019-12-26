import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600))


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 0:
                    pygame.draw.rect(screen, (230, 230, 230), (
                    self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size), 1)
                else:
                    pygame.draw.rect(screen, (230, 230, 230), (
                    self.left + x * self.cell_size, self.top + y * self.cell_size, self.cell_size, self.cell_size))

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        y = (mouse_y - self.top) // self.cell_size
        x = (mouse_x - self.left) // self.cell_size
        if x < 0 or y < 0 or x >= self.width or y >= self.height:
            print('None')
            return None
        return x, y

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def on_click(self, cell):
        x, y = cell
        for i in range(self.width):
            self.board[y][i] = (self.board[y][i] + 1) % 2
        for i in range(self.height):
            self.board[i][x] = (self.board[i][x] + 1) % 2
        self.board[y][x] = (self.board[y][x] + 1) % 2


board = Board(13, 13)
board.set_view(30, 30, 30)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render()
    pygame.display.flip()

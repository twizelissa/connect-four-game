import pygame

# Game settings
rows = 6
cols = 7
square_size = 100
disc_size_ratio = 0.8

# Colours
blue = (23, 93, 222)
yellow = (255, 240, 0)
red = (255, 0, 0)
background = (19, 72, 162)

# Pygame config
pygame.init()
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Connect Four")
screen = pygame.display.set_mode([cols*square_size, rows*square_size])

# Game info
board = [[0 for r in range(rows)] for c in range(cols)]
turn = 1


def draw_board():
	"""
	Draws board[c][r] with c = 0 and r = 0 being bottom left
	0 = empty (background colour)
	1 = yellow
	2 = red
	"""
	screen.fill(blue)

	for r in range(rows):
		for c in range(cols):
			colour = background
			if board[c][r] == 1:
				colour = yellow
			if board[c][r] == 2:
				colour = red

			pygame.draw.circle(screen, colour, (c*square_size + square_size/2, rows*square_size - r*square_size - square_size/2), int(disc_size_ratio * square_size/2))


def place(c):
	"""
	Tries to place the playing colour on the cth column
	:param c: column to place on
	:return: True if placed, False if not placeable
	"""
	global turn

	for r in range(rows):
		if board[c][r] == 0:
			board[c][r] = turn
			if turn == 1:
				turn = 2
			else:
				turn = 1
			return True
	return False


if __name__ == '__main__':
	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP:
				place(pygame.mouse.get_pos()[0]//square_size)

		draw_board()

		pygame.display.update()

	pygame.quit()

import pygame
import pygame.gfxdraw
import random

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
black = (0, 0, 0)
white = (255, 255, 255)

# Pygame config
pygame.init()
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Connect Four")
screen = pygame.display.set_mode([cols*square_size, rows*square_size])
font = pygame.font.SysFont(None, 80)

# Game state
board = [[0 for r in range(rows)] for c in range(cols)]
turn = random.randint(1, 2)
won = None


def reset_game():
	"""
	Resets the game state (board and variables)
	"""
	global board, turn, won
	board = [[0 for r in range(rows)] for c in range(cols)]
	turn = random.randint(1, 2)
	won = None


def place(c):
	"""
	Tries to place the playing colour on the cth column
	:param c: column to place on
	:return: True if placed, False if not placeable
	"""
	global turn, won

	for r in range(rows):
		if board[c][r] == 0:
			board[c][r] = turn

			won = check_win(c, r)
			if won is None:
				if turn == 1:
					turn = 2
				else:
					turn = 1
			return True
	return False


def check_win(c, r):
	"""
	Checks for win/draw from newly added disc
	:param c: co
	:param r:
	:return: True if game is won by most recent player
	"""
	min_col = max(c-3, 0)
	max_col = min(c+3, cols-1)
	min_row = max(r - 3, 0)
	max_row = min(r + 3, rows - 1)

	# Horizontal check
	count = 0
	for ci in range(min_col, max_col + 1):
		if board[ci][r] == turn:
			count += 1
		else:
			count = 0
		if count == 4:
			return turn

	# Vertical check
	count = 0
	for ri in range(min_row, max_row + 1):
		if board[c][ri] == turn:
			count += 1
		else:
			count = 0
		if count == 4:
			return turn

	count1 = 0
	count2 = 0
	# Diagonal check
	for i in range(-3, 4):
		# bottom-left -> top-right
		if 0 <= c + i < cols and 0 <= r + i < rows:
			if board[c + i][r + i] == turn:
				count1 += 1
			else:
				count1 = 0
			if count1 == 4:
				return turn
		# bottom-right -> top-let
		if 0 <= c + i < cols and 0 <= r - i < rows:
			if board[c + i][r - i] == turn:
				count2 += 1
			else:
				count2 = 0
			if count2 == 4:
				return turn

	# Draw check
	if sum([x.count(0) for x in board]) == 0:
		return 0

	return None


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

			# Classical non anti-aliased circle drawing
			# pygame.draw.circle(screen, colour, (c*square_size + square_size//2, rows*square_size - r*square_size - square_size//2), int(disc_size_ratio * square_size/2))

			# Anti-aliased circle drawing
			pygame.gfxdraw.aacircle(screen, c*square_size + square_size//2, rows*square_size - r*square_size - square_size//2, int(disc_size_ratio * square_size/2), colour)
			pygame.gfxdraw.filled_circle(screen, c*square_size + square_size//2, rows*square_size - r*square_size - square_size//2, int(disc_size_ratio * square_size/2), colour)


def draw_win_message():
	"""
	Displays win message on top of the board
	"""
	if won is not None:
		if won == 1:
			img = font.render("Yellow won", True, black, yellow)
		elif won == 2:
			img = font.render("Red won", True, white, red)
		else:
			img = font.render("Draw", True, white, blue)

		rect = img.get_rect()
		rect.center = ((cols * square_size)//2, (rows * square_size)//2)

		screen.blit(img, rect)


def update_view():
	"""
	Updates the pygame view with correct board
	"""
	draw_board()
	draw_win_message()

	pygame.display.update()


if __name__ == '__main__':
	reset_game()

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if won is None:
					place(pygame.mouse.get_pos()[0]//square_size)
				else:
					reset_game()

		update_view()

	pygame.quit()

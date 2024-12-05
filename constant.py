import math
from pygame.locals import USEREVENT
# SCREEN DIMENSIONS
WIDTH, HEIGHT = 800, 750

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GREY = (128, 128, 128)
PANEL = (55, 55, 55)
BACKGROUND = (180, 180, 180)

# DIMESNIONS FOR HEX from https://www.redblobgames.com/grids/hexagons/
RADIUS = 25  # Distance from center to a vertex
WIDTH_HEX = math.sqrt(3) * RADIUS  # Full width of a hexagon
HEIGHT_HEX = 2 * RADIUS  # Full height of a hexagon
HORIZONTAL_SPACING = WIDTH_HEX  # Horizontal spacing
VERTICAL_SPACING = 3/4 * HEIGHT_HEX  # Vertical spacing

# Timer
TIMER_EVENT = USEREVENT + 1

# Game State
GAME_STATES = ['PAUSE', 'RESUME', 'WHITE TURN',
               'BLACK TURN', 'END GAME', 'WHITE WINS', 'BLACK WINS']

# Menu states
STATE_START_MENU = "start_menu"
STATE_OPPONENT_MENU = "opponent_menu"
STATE_DIFFICULTY_MENU = "difficulty_menu"
STATE_END_MENU = "end_menu"

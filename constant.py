import math
from pygame.locals import USEREVENT
# SCREEN DIMENSIONS
WIDTH, HEIGHT = 800, 750

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GREY = (128, 128, 128)
PANEL = (42, 54, 99)
BACKGROUND = (42, 54, 99)
START_MENU_BG_COLOR = (42, 54, 99)  # Dark grey background
BUTTON_COLOR = (181, 159, 120)  # Muted greyish beige
BUTTON_HOVER_COLOR = (179, 164, 138)  # Softer beige
# Steel blue for selected button highlight
BUTTON_BORDER_COLOR = (70, 130, 180)
DISABLED_BUTTON_COLOR = (160, 160, 160)  # Greyed-out button

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

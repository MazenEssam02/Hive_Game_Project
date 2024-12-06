import math
from pygame.locals import USEREVENT
# SCREEN DIMENSIONS
WIDTH, HEIGHT = 800, 750

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GREY = (89, 89, 89)
DARK_BLUE= (54, 69, 125)
START_MENU_BG_COLOR = (42, 54, 99)  
BUTTON_COLOR = (181, 159, 120)  
BUTTON_HOVER_COLOR = (179, 164, 138)  
BUTTON_BORDER_COLOR = (70, 130, 180)
DISABLED_BUTTON_COLOR = (160, 160, 160)  

# DIMESNIONS FOR HEX from https://www.redblobgames.com/grids/hexagons/
RADIUS = 25  # Distance from center to a vertex
WIDTH_HEX = math.sqrt(3) * RADIUS  # Full width of a hexagon
HEIGHT_HEX = 2 * RADIUS  # Full height of a hexagon
HORIZONTAL_SPACING = WIDTH_HEX  # Horizontal spacing
VERTICAL_SPACING = 3/4 * HEIGHT_HEX  # Vertical spacing

# Timer
TIMER_EVENT = USEREVENT + 1


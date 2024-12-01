import math
# SCREEN DIMENSIONS
WIDTH, HEIGHT = 800, 600

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 102, 204)
GREY = (128, 128, 128)

# DIMESNIONS FOR HEX from https://www.redblobgames.com/grids/hexagons/
RADIUS = 25  # Distance from center to a vertex
WIDTH_HEX = math.sqrt(3) * RADIUS  # Full width of a hexagon
HEIGHT_HEX = 2 * RADIUS  # Full height of a hexagon
HORIZONTAL_SPACING = WIDTH_HEX  # Horizontal spacing
VERTICAL_SPACING = 3/4 * HEIGHT_HEX  # Vertical spacing

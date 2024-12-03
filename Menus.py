import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Colors
START_MENU_BG_COLOR = (50, 50, 50)  # Dark grey background
BUTTON_COLOR = (198, 155, 123)  # Muted greyish beige
BUTTON_HOVER_COLOR = (223, 184, 150)  # Softer beige
BUTTON_BORDER_COLOR = (70, 130, 180)  # Steel blue for selected button highlight
TEXT_COLOR = (255, 255, 255)  # White for text
DISABLED_BUTTON_COLOR = (160, 160, 160)  # Greyed-out button

# Fonts
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 32)

# Game states
STATE_START_MENU = "start_menu"
STATE_OPPONENT_MENU = "opponent_menu"
STATE_DIFFICULTY_MENU = "difficulty_menu"
STATE_GAME = "game"
STATE_END_MENU = "end_menu"
current_state = STATE_START_MENU

# Selected options
selected_opponent = None
selected_difficulty = None
show_difficulty_menu = False

def draw_button(text, x, y, width, height, action=None, enabled=True, selected=False):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Determine the color of the button based on hover and enabled state
    if not enabled:
        button_color = DISABLED_BUTTON_COLOR
    else:
        button_color = (
            BUTTON_HOVER_COLOR
            if x < mouse[0] < x + width and y < mouse[1] < y + height
            else BUTTON_COLOR
        )

    # Draw the button itself
    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    
    # Highlight the border if the button is selected (via mouse hover)
    if selected:
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (x - 2, y - 2, width + 4, height + 4), 3, border_radius=10)

    # Draw the text centered on the button
    draw_text(text, small_font, TEXT_COLOR if enabled else (100, 100, 100), screen, x + width // 2, y + height // 2)

    # Handle button click when enabled and mouse hovers over the button
    if enabled and x < mouse[0] < x + width and y < mouse[1] < y + height:
        if click[0] == 1 and action:
            return action()

# Utility function to draw centered text
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

# Start Menu
def start_menu():
    screen.fill(START_MENU_BG_COLOR)
    draw_text("Start Menu", font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)

    options = [
        ("Start Game", lambda: switch_state(STATE_OPPONENT_MENU)),
        ("Quit", quit_game)
    ]

    for i, (text, action) in enumerate(options):
        y_offset = 200 + i * 80
        # Highlight button if hovered
        is_selected = SCREEN_WIDTH // 2 - 100 < pygame.mouse.get_pos()[0] < SCREEN_WIDTH // 2 + 100 and 200 + i * 80 < pygame.mouse.get_pos()[1] < 250 + i * 80
        draw_button(text, SCREEN_WIDTH // 2 - 100, y_offset, 200, 50, action, selected=is_selected)

# Opponent Menu
def opponent_menu():
    global selected_opponent
    screen.fill(START_MENU_BG_COLOR)
    draw_text("Choose Opponent", font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)

    # Define button positions and text for opponent options
    buttons = [
        ("Human vs Human", SCREEN_WIDTH // 2 - 150, 200),
        ("Human vs Computer", SCREEN_WIDTH // 2 - 150, 280),
        ("Computer vs Computer", SCREEN_WIDTH // 2 - 150, 360)
    ]

    # Draw buttons with selection border (only via mouse hover)
    for i, (text, x, y) in enumerate(buttons):
        # Highlight button if it is selected (via mouse hover)
        is_selected = x < pygame.mouse.get_pos()[0] < x + 300 and y < pygame.mouse.get_pos()[1] < y + 50
        draw_button(text, x, y, 300, 50, lambda opponent=text: set_opponent(opponent), selected=is_selected)

    # Show "Next" button if opponent is selected that requires difficulty selection
    if selected_opponent in ["Human vs Computer", "Computer vs Computer"]:
        draw_button(
            "Next",
            SCREEN_WIDTH // 2 - 100,
            500,
            200,
            50,
            lambda: switch_state(STATE_DIFFICULTY_MENU),
            enabled=bool(selected_opponent)
        )
    else:
        # Show "Start Game" if an opponent is selected
        draw_button(
            "Start Game :)",
            SCREEN_WIDTH // 2 - 100,
            500,
            200,
            50,
            lambda: switch_state(STATE_GAME),
            enabled=bool(selected_opponent)
        )

# Difficulty Menu
def difficulty_menu():
    global selected_difficulty
    screen.fill(START_MENU_BG_COLOR)
    draw_text("Select Difficulty", font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)

    options = [
        ("Easy", lambda: set_difficulty("Easy")),
        ("Medium", lambda: set_difficulty("Medium")),
        ("Hard", lambda: set_difficulty("Hard"))
    ]

    for i, (text, action) in enumerate(options):
        y_offset = 200 + i * 80
        # Highlight button if hovered
        is_selected = SCREEN_WIDTH // 2 - 100 < pygame.mouse.get_pos()[0] < SCREEN_WIDTH // 2 + 100 and 200 + i * 80 < pygame.mouse.get_pos()[1] < 250 + i * 80
        draw_button(text, SCREEN_WIDTH // 2 - 100, y_offset, 200, 50, action, selected=is_selected)

    draw_button(
        "Start Game",
        SCREEN_WIDTH // 2 - 100,
        500,
        200,
        50,
        lambda: switch_state(STATE_GAME),
        enabled=bool(selected_difficulty),
    )

# Game Placeholder
def game_running():
    screen.fill(START_MENU_BG_COLOR)
    draw_text(f"Game Running - {selected_difficulty} Mode", font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(f"Opponent: {selected_opponent}", small_font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# End Menu
def end_menu():
    screen.fill(START_MENU_BG_COLOR)
    draw_text("Game Over", font, TEXT_COLOR, screen, SCREEN_WIDTH // 2, 100)

    options = [
        ("Restart", lambda: switch_state(STATE_START_MENU)),
        ("Quit", quit_game)
    ]

    for i, (text, action) in enumerate(options):
        y_offset = 200 + i * 80
        draw_button(text, SCREEN_WIDTH // 2 - 100, y_offset, 200, 50, action)

# Helper Functions
def switch_state(new_state):
    global current_state
    current_state = new_state

def set_opponent(opponent):
    global selected_opponent
    selected_opponent = opponent
    print(f"Selected Opponent: {opponent}")

def set_difficulty(level):
    global selected_difficulty
    selected_difficulty = level
    print(f"Selected Difficulty: {level}")

def quit_game():
    pygame.quit()
    sys.exit()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

    if current_state == STATE_START_MENU:
        start_menu()
    elif current_state == STATE_OPPONENT_MENU:
        opponent_menu()
    elif current_state == STATE_DIFFICULTY_MENU:
        difficulty_menu()
    elif current_state == STATE_GAME:
        game_running()
    elif current_state == STATE_END_MENU:
        end_menu()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

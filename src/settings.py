WINDOW_WIDTH = 900
WINDOW_HEIGHT = 400

PADDING = 20

REACTION_DISTANCE = 50

HOTBAR_WIDTH = WINDOW_WIDTH - 2 * PADDING
HOTBAR_HEIGHT = WINDOW_HEIGHT * 0.2

GAME_WIDTH = WINDOW_WIDTH - (2 * PADDING)
GAME_HEIGHT = WINDOW_HEIGHT - 2 * PADDING - 2*HOTBAR_HEIGHT

WHITE = '#C4A484'
GRAY = '#808080'
LIGHT_BLUE = '#add8e6'

TRASH_SIZE = 80
TRASH_MARGIN = 30
TRASH_POS = WINDOW_WIDTH-2.5*PADDING,2.5*PADDING

ITEM_IMAGE_SIZE = (100, 100)
ITEM_FONT = ("Times New Roman", 24)
ITEM_TYPE_MATERIAL = "Material"
ITEM_TYPE_TOOL = "Tool"

REACTION_DISTANCE = 50

def compute_sizes(window_width, window_height):
    hotbar_height = int(window_height * 0.2)
    hotbar_width = window_width - 2 * PADDING
    game_width = window_width - 2 * PADDING
    game_height = window_height - 2 * PADDING - hotbar_height - 60
    return hotbar_width, hotbar_height, game_width, game_height
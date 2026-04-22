from HB.hotbar import Hotbar
from config import AVAILABLE_MATERIALS
from settings import ITEM_TYPE_MATERIAL


class MaterialsH(Hotbar):
    def __init__(self, window_size, game):
        super().__init__(window_size, game)
        self.items = AVAILABLE_MATERIALS
        self.type = ITEM_TYPE_MATERIAL
        self.active_tab = "Materials"

class ToolsH(Hotbar):
    def __init__(self, window_size, game):
        super().__init__(window_size, game)
        self.items = AVAILABLE_TOOLS
        self.type = ITEM_TYPE_TOOL
        self.active_tab = "Tools"
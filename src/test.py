import pygame
import pytest
from unittest.mock import Mock, patch

from reaction import Reaction
from trash import Trash

import os

RESULT_FILE = "test_results.txt"

def log_result(test_name, outcome):
    with open(RESULT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{test_name}: {outcome}\n")

def test_get_recipe():
    game = Mock()

    obj = Reaction(game)
    obj.reactions = {
        frozenset(["H2", "O2"]): "H2O",
        frozenset(["Na", "Cl"]): {"result": ["NaCl"], "equation": "Na + Cl -> NaCl"},
        frozenset(["C", "O2"]): ["CO", "CO2"]
    }
    obj._matches_result = Mock(side_effect=lambda result, target: target in (result if isinstance(result, list) else [result]))

    recipes = obj.get_recipe("H2O")
    assert set(recipes[0]) == {"H2", "O2"}

    recipes = obj.get_recipe("NaCl")
    assert set(recipes[0]) == {"Na", "Cl"}

    recipes = obj.get_recipe("CO")
    assert set(recipes[0]) == {"C", "O2"}

    recipes = obj.get_recipe("CO2")
    assert set(recipes[0]) == {"C", "O2"}

def test_can_react():
    game = Mock()

    obj = Reaction(game)
    obj.reactions = {
        frozenset(["H2", "O2"]): "H2O"
    }

    item1 = Mock()
    item1.name = "H2"

    item2 = Mock()
    item2.name = "O2"

    item3 = Mock()
    item3.name = "Na"

    item4 = Mock()
    item4.name = "Cl"

    assert obj.can_react(item1, item2) is True
    assert obj.can_react(item3, item4) is False

def test_check():
    game = Mock()

    item1 = Mock()
    item1.name = "H2"
    item1.rect = Mock(centerx=100, centery=100)

    item2 = Mock()
    item2 = Mock()
    item2.name = "O2"
    item2.rect = Mock(centerx=100, centery=100)

    game.world_items = [item1, item2]

    obj = Reaction(game)
    obj.reactions = {
        frozenset(["H2", "O2"]): "H2O"
    }

    result = obj.check(item1, item2)
    assert result is True
    game.spawn_item.assert_called_with("H2O", (100, 100), "Material", parents=[item1, item2], display_label=None)
    assert item1 not in game.world_items
    assert item2 not in game.world_items

def test_check_multiple_results():
    game = Mock()

    item1 = Mock()
    item1.name = "C"
    item1.rect = Mock(centerx=100, centery=100)

    item2 = Mock()
    item2 = Mock()
    item2.name = "O2"
    item2.rect = Mock(centerx=100, centery=100)

    game.world_items = [item1, item2]

    obj = Reaction(game)
    obj.reactions = {
        frozenset(["C", "O2"]): ["CO", "CO2"]
    }

    result = obj.check(item1, item2)
    assert result is True
    game.spawn_item.assert_any_call("CO", (100, 100), "Material", parents=[item1, item2], display_label=None)
    game.spawn_item.assert_any_call("CO2", (140, 100), "Material", parents=[item1, item2], display_label=None)
    assert item1 not in game.world_items
    assert item2 not in game.world_items

def test_check_reaction_removal():
    game = Mock()
    
    item1 = Mock()
    item1.name = "H2"
    item1.rect = Mock(centerx=100, centery=100)

    item2 = Mock()
    item2.name = "O2"
    item2.rect = Mock(centerx=100, centery=100)
    game.world_items = [item1, item2]

    obj = Reaction(game)
    obj.reactions = {
        frozenset(["H2", "O2"]): "H2O"
    }

    result = obj.check(item1, item2)
    assert result is True
    assert item1 not in game.world_items
    assert item2 not in game.world_items
@patch("pygame.image.load")
def test_delete_item(mock_load):
    pygame.init()
    pygame.display.set_mode((1, 1))

    mock_load.return_value = pygame.Surface((50, 50))

    trash = Trash((100, 100), (800, 600))
    world_items = ["item1", "item2", "item3"]

    assert trash.delete_item("item2", world_items) is True
    assert world_items == ["item1", "item3"]
    
    pygame.quit()

@patch("pygame.image.load")
def test_trash_hover(mock_load):
    pygame.init()
    pygame.display.set_mode((1, 1))

    mock_load.return_value = pygame.Surface((50, 50))

    trash = Trash((100, 100), (800, 600))

    assert trash.check_hover((100, 100)) is True
    assert trash.is_hovered is True

    assert trash.check_hover((50, 50)) is False
    assert trash.is_hovered is False
    
    pygame.quit()

@patch("pygame.image.load")
def test_trash_draw(mock_load):
    pygame.init()
    pygame.display.set_mode((1, 1))

    mock_load.return_value = pygame.Surface((50, 50))

    trash = Trash((100, 100), (800, 600))
    surface = Mock()

    trash.is_hovered = False
    trash.draw(surface)
    surface.blit.assert_called_with(trash.image_closed, trash.rect)

    surface.reset_mock()

    trash.is_hovered = True
    trash.draw(surface)
    surface.blit.assert_called_with(trash.image_open, trash.rect)

    pygame.quit()

if __name__ == "__main__":
    tests = [
        ("test_get_recipe", test_get_recipe),
        ("test_can_react", test_can_react),
        ("test_check", test_check),
        ("test_check_multiple_results", test_check_multiple_results),
        ("test_check_reaction_removal", test_check_reaction_removal),
        ("test_delete_item", test_delete_item),
        ("test_trash_hover", test_trash_hover),
        ("test_trash_draw", test_trash_draw),
    ]

    for name, func in tests:
        try:
            func()
            log_result(name, "passed")
        except Exception as e:
            log_result(name, f"failed: {e}")
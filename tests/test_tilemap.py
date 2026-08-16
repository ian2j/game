import objects.tilemap as tmp

WALL_COLOR = (0, 0, 0)
FLOOR_COLOR = (255, 255, 255)


def _small_map(extra_walls=()):
    return tmp.TileMap(
        width=200, height=200, tile_size=20,
        wall_color=WALL_COLOR, floor_color=FLOOR_COLOR, extra_walls=extra_walls,
    )


def test_can_move_on_open_floor():
    tile_map = _small_map()
    assert tile_map.can_move(60, 60, 20, 20) is True


def test_cannot_move_into_border_wall():
    tile_map = _small_map()
    assert tile_map.can_move(0, 60, 20, 20) is False


def test_cannot_move_into_extra_interior_wall():
    tile_map = _small_map(extra_walls=[(slice(3, 5), slice(3, 5))])
    assert tile_map.can_move(60, 60, 20, 20) is False


def test_can_move_clamps_out_of_range_coordinates():
    tile_map = _small_map()
    assert tile_map.can_move(-1000, -1000, 20, 20) is False

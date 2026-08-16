from screens.game_find_pooh import boxes_left_to_right


def test_orders_boxes_by_x_position():
    boxes = {0: {"position_x": 300}, 1: {"position_x": 100}, 2: {"position_x": 200}}
    assert boxes_left_to_right(boxes) == [1, 2, 0]


def test_already_sorted_stays_the_same():
    boxes = {"a": {"position_x": -10}, "b": {"position_x": 50}}
    assert boxes_left_to_right(boxes) == ["a", "b"]

import json

import constants.settings as stt
import objects.game_state as gst


def test_default_state_has_sane_values():
    state = gst.GameState.default()
    assert state.costume in stt.COSTUMES
    assert state.current_room == "main"
    assert state.high_scores == {}


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "savegame.json"
    state = gst.GameState(
        costume="Standard", player_position=(12.0, 34.0), player_direction="left",
        current_room="outside", high_scores={"letter_matching": 4200},
    )
    state.save(path=path)

    loaded = gst.GameState.load_or_default(path=path)
    assert loaded == state


def test_load_or_default_missing_file_returns_default(tmp_path):
    loaded = gst.GameState.load_or_default(path=tmp_path / "does_not_exist.json")
    assert loaded == gst.GameState.default()


def test_load_or_default_corrupted_file_falls_back(tmp_path):
    path = tmp_path / "savegame.json"
    path.write_text("not valid json")
    loaded = gst.GameState.load_or_default(path=path)
    assert loaded == gst.GameState.default()


def test_load_or_default_resets_unknown_costume(tmp_path):
    path = tmp_path / "savegame.json"
    path.write_text(json.dumps({"costume": "NotARealCostume"}))
    loaded = gst.GameState.load_or_default(path=path)
    assert loaded.costume == stt.DEFAULT_COSTUME


def test_record_high_score_keeps_the_better_value():
    state = gst.GameState.default()
    state.record_high_score("catch_stars", 5, higher_is_better=True)
    state.record_high_score("catch_stars", 3, higher_is_better=True)
    assert state.high_scores["catch_stars"] == 5

    state.record_high_score("find_pooh", 4, higher_is_better=False)
    state.record_high_score("find_pooh", 6, higher_is_better=False)
    assert state.high_scores["find_pooh"] == 4

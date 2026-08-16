import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import constants.dimensions as dms
import constants.settings as stt

SAVE_DIR = Path(__file__).resolve().parent.parent / "save"
SAVE_PATH = SAVE_DIR / "savegame.json"

DEFAULT_ROOM = "main"


def _default_player_position():
    return (
        dms.SCREEN_WIDTH / 2 - stt.PLAYER_FRAME_WIDTH * stt.PLAYER_SCALE / 2,
        dms.SCREEN_HEIGHT / 2 - stt.PLAYER_FRAME_HEIGHT * stt.PLAYER_SCALE / 2,
    )


@dataclass
class GameState:
    """Everything about the current player that should survive a screen
    change or a full quit-and-relaunch of the game."""

    costume: str = stt.DEFAULT_COSTUME
    player_position: tuple = field(default_factory=_default_player_position)
    player_direction: str = "down"
    current_room: str = DEFAULT_ROOM
    high_scores: dict = field(default_factory=dict)

    @property
    def player_sprite_sheet(self):
        return stt.COSTUMES[self.costume]

    @classmethod
    def default(cls):
        return cls()

    @classmethod
    def load_or_default(cls, path=SAVE_PATH):
        if not Path(path).exists():
            return cls.default()
        try:
            with open(path, "r") as save_file:
                data = json.load(save_file)
        except (OSError, json.JSONDecodeError):
            return cls.default()

        state = cls.default()
        for key in ("costume", "player_direction", "current_room", "high_scores"):
            if key in data:
                setattr(state, key, data[key])
        if "player_position" in data:
            state.player_position = tuple(data["player_position"])
        if state.costume not in stt.COSTUMES:
            state.costume = stt.DEFAULT_COSTUME
        return state

    def save(self, path=SAVE_PATH):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w") as save_file:
            json.dump(asdict(self), save_file, indent=2)

    def record_high_score(self, minigame_id, score, higher_is_better=True):
        best = self.high_scores.get(minigame_id)
        if best is None or (score > best if higher_is_better else score < best):
            self.high_scores[minigame_id] = score

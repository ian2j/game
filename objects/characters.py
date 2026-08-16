import objects.sprite_sheets as sps


class Player(sps.SpriteSheet):
    """A SpriteSheet that also tracks the facing direction used to pick
    which animation row to play."""

    def __init__(self, name="Player"):
        super().__init__()
        self.name = name
        self.scale = 6
        self.direction = "down"

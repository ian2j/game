import pygame

import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import constants.settings as stt
import functions.audio as aud
import functions.visual as viz
import objects.characters as crs
import objects.doors as drs
import objects.tilemap as tmp
import screens.game_catch_stars
import screens.game_find_pooh
import screens.game_letter_matching
import screens.menu_pause
import screens.scene_base as scb

ANIMATION_SPEED = 100  # ms per animation frame

_CENTERED_SPAWN = (
    dms.SCREEN_WIDTH / 2 - stt.PLAYER_FRAME_WIDTH * stt.PLAYER_SCALE / 2,
    dms.SCREEN_HEIGHT / 2 - stt.PLAYER_FRAME_HEIGHT * stt.PLAYER_SCALE / 2,
)

ROOMS = {
    "main": {
        "spawn": _CENTERED_SPAWN,
        "floor_color": clr.WHITE,
        "wall_color": clr.GREY,
    },
    "outside": {
        "spawn": _CENTERED_SPAWN,
        "floor_color": clr.LIGHT_GREEN,
        "wall_color": clr.DARK_GREEN,
    },
}


def _build_animations(player):
    columns = {"down": 0, "up": 1, "left": 2, "right": 3}
    return {
        direction: [
            viz.get_frame(
                sheet=player.sprite_sheet,
                frame_width=player.frame_width,
                frame_height=player.frame_height,
                column=column,
                row=row,
                scale_factor=player.scale,
            )
            for row in range(4)
        ]
        for direction, column in columns.items()
    }


class OverworldScene(scb.Scene):
    def __init__(self, state, room_id):
        super().__init__()
        self.state = state
        self.room_id = room_id

        room = ROOMS[room_id]
        if state.current_room != room_id:
            state.player_position = room["spawn"]
        state.current_room = room_id

        aud.play_looping_track(filename="sounds/sample_music_2.mp3")

        self.player = crs.Player()
        self.player.set_sprite_sheet(sprite_sheet=state.player_sprite_sheet)
        self.player.set_frame_width(frame_width=stt.PLAYER_FRAME_WIDTH)
        self.player.set_frame_height(frame_height=stt.PLAYER_FRAME_HEIGHT)
        self.player.set_scale(scale=stt.PLAYER_SCALE)
        self.player.set_position(position=state.player_position)
        self.player.direction = state.player_direction

        self.tile_map = tmp.TileMap(
            width=dms.SCREEN_WIDTH, height=dms.SCREEN_HEIGHT, tile_size=dms.TILE_SIZE,
            wall_color=room["wall_color"], floor_color=room["floor_color"],
        )

        self.animations = _build_animations(self.player)
        self.frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.moving = False

        self.doors = self._build_doors()

    def _build_doors(self):
        if self.room_id == "main":
            return [
                drs.Door.from_icon_files(
                    door_id="letter_matching", label="Letter Matching", position=(200, 200),
                    icon_unselected="sprites/minigame_icons/letter_matching.png",
                    icon_selected="sprites/minigame_icons/letter_matching_selected.png",
                    on_enter=self._enter_letter_matching,
                ),
                drs.Door.from_icon_files(
                    door_id="find_pooh", label="    Find Pooh", position=(880, 200),
                    icon_unselected="sprites/minigame_icons/find_pooh.png",
                    icon_selected="sprites/minigame_icons/find_pooh_selected.png",
                    on_enter=self._enter_find_pooh,
                ),
                drs.Door.plain(
                    door_id="to_outside", label="Outside", position=(580, 560),
                    on_enter=lambda: self._enter_room("outside"),
                ),
            ]
        elif self.room_id == "outside":
            return [
                drs.Door.plain(
                    door_id="to_main", label="Luna's Room", position=(580, 560),
                    on_enter=lambda: self._enter_room("main"),
                ),
                drs.Door.plain(
                    door_id="catch_stars", label="Catch the Stars", position=(880, 200), size=(160, 200),
                    on_enter=self._enter_catch_stars,
                ),
            ]
        raise ValueError(f"Unknown room_id: {self.room_id}")

    def _enter_room(self, room_id):
        self.next_scene = OverworldScene(state=self.state, room_id=room_id)

    def _enter_letter_matching(self):
        self.next_scene = screens.game_letter_matching.LetterMatchingScene(state=self.state)

    def _enter_find_pooh(self):
        self.next_scene = screens.game_find_pooh.FindPoohScene(state=self.state)

    def _enter_catch_stars(self):
        self.next_scene = screens.game_catch_stars.CatchStarsScene(state=self.state)

    def handle_event(self, event, screen):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.next_scene = screens.menu_pause.PauseMenuScene(resume_scene=self, state=self.state)
            elif event.key == pygame.K_SPACE:
                for door in self.doors:
                    if door.selected:
                        door.on_enter()

    def update(self, dt):
        keys = pygame.key.get_pressed()
        player_x, player_y = self.player.get_position()
        new_x, new_y = player_x, player_y
        self.moving = False

        if keys[pygame.K_UP]:
            self.player.direction = "up"
            new_y -= 5
            self.moving = True
        elif keys[pygame.K_DOWN]:
            self.player.direction = "down"
            new_y += 5
            self.moving = True
        elif keys[pygame.K_LEFT]:
            self.player.direction = "left"
            new_x -= 5
            self.moving = True
        elif keys[pygame.K_RIGHT]:
            self.player.direction = "right"
            new_x += 5
            self.moving = True

        width = self.player.frame_width * self.player.scale
        height = self.player.frame_height * self.player.scale
        if self.tile_map.can_move(new_x, player_y, width, height):
            player_x = new_x
        if self.tile_map.can_move(player_x, new_y, width, height):
            player_y = new_y

        self.player.set_position((player_x, player_y))
        self.state.player_position = (player_x, player_y)
        self.state.player_direction = self.player.direction

        for door in self.doors:
            door.update_selection((player_x, player_y))

        current_time = pygame.time.get_ticks()
        if self.moving and current_time - self.last_update_time > ANIMATION_SPEED:
            self.last_update_time = current_time
            self.frame_index = (self.frame_index + 1) % len(self.animations[self.player.direction])
        elif not self.moving:
            self.frame_index = 0

    def draw(self, screen):
        self.tile_map.draw(screen)
        for door in self.doors:
            door.draw(screen, self.player.get_position(), fnt.small_font)
        current_frame = self.animations[self.player.direction][self.frame_index]
        screen.blit(current_frame, self.player.get_position())

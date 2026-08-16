import numpy as np
import pygame

import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import constants.settings as stt
import functions.audio as aud
import functions.visual as viz
import objects.tilemap as tmp
import screens.menu_end_minigame
import screens.menu_pause
import screens.scene_base as scb

BASKET_Y = 600
BASKET_SPEED = 8  # px/frame

GOOD_ITEM_CHANCE = 0.7
WIN_SCORE = 10
STARTING_LIVES = 3

SPAWN_INTERVAL_START_MS = 1100
SPAWN_INTERVAL_MIN_MS = 500
SPAWN_INTERVAL_DECAY_PER_POINT = 40

FALL_SPEED_START = 4  # px/frame
FALL_SPEED_MAX = 10
FALL_SPEED_RAMP_PER_POINT = 0.4

STAR_SIZE = (50, 50)
HUD_MARGIN = 50  # clear of the two-tile-thick wall border
HUD_PADDING = 8


class CatchStarsScene(scb.Scene):
    """Catch the falling star, dodge the red X. The basket is the player's
    own sprite; the star is drawn rather than loaded, since there's no
    dedicated art for a third minigame yet. First minigame with an actual
    lose condition, for a bit of replay variety."""

    def __init__(self, state):
        super().__init__()
        self.state = state
        aud.play_looping_track(filename="sounds/sample_music_3.mp3")

        self.tile_map = tmp.TileMap(
            width=dms.SCREEN_WIDTH, height=dms.SCREEN_HEIGHT, tile_size=dms.TILE_SIZE,
            wall_color=clr.NAVY, floor_color=clr.LIGHT_BLUE,
        )

        self.good_item_template = {
            "frame": viz.render_star(STAR_SIZE, clr.YELLOW, outline_color=clr.BLACK),
            "width": STAR_SIZE[0], "height": STAR_SIZE[1],
        }
        self.bad_item_template = {
            "frame": viz.load_static_frame("sprites/shapes/x_mark_red.png", 90, 90, 0.5),
            "width": int(90 * 0.5), "height": int(90 * 0.5),
        }

        self.basket_frame = viz.load_static_frame(
            state.player_sprite_sheet, stt.PLAYER_FRAME_WIDTH, stt.PLAYER_FRAME_HEIGHT, stt.PLAYER_SCALE
        )
        self.basket_width = stt.PLAYER_FRAME_WIDTH * stt.PLAYER_SCALE
        self.basket_height = stt.PLAYER_FRAME_HEIGHT * stt.PLAYER_SCALE
        self.basket_position = (dms.SCREEN_WIDTH / 2 - self.basket_width / 2, BASKET_Y)

        self.items = []
        self.spawn_timer_ms = SPAWN_INTERVAL_START_MS
        self.score = 0
        self.lives = STARTING_LIVES
        self.won = False
        self.lost = False

    def _spawn_item(self):
        kind = "good" if np.random.random() < GOOD_ITEM_CHANCE else "bad"
        template = self.good_item_template if kind == "good" else self.bad_item_template
        wall = dms.TILE_SIZE * 2
        x = np.random.uniform(wall, dms.SCREEN_WIDTH - wall - template["width"])
        self.items.append({
            "kind": kind, "x": x, "y": wall,
            "frame": template["frame"], "width": template["width"], "height": template["height"],
        })

    def handle_event(self, event, screen):
        if self.won or self.lost:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_scene = screens.menu_pause.PauseMenuScene(resume_scene=self, state=self.state)

    def update(self, dt):
        if self.won or self.lost:
            return

        keys = pygame.key.get_pressed()
        basket_x, basket_y = self.basket_position
        new_x = basket_x
        if keys[pygame.K_LEFT]:
            new_x -= BASKET_SPEED
        elif keys[pygame.K_RIGHT]:
            new_x += BASKET_SPEED
        if self.tile_map.can_move(new_x, basket_y, self.basket_width, self.basket_height):
            basket_x = new_x
        self.basket_position = (basket_x, basket_y)

        self.spawn_timer_ms -= dt
        if self.spawn_timer_ms <= 0:
            self._spawn_item()
            self.spawn_timer_ms = max(
                SPAWN_INTERVAL_MIN_MS, SPAWN_INTERVAL_START_MS - self.score * SPAWN_INTERVAL_DECAY_PER_POINT
            )

        fall_speed = min(FALL_SPEED_MAX, FALL_SPEED_START + self.score * FALL_SPEED_RAMP_PER_POINT)
        basket_rect = pygame.Rect(basket_x, basket_y, self.basket_width, self.basket_height)
        remaining = []
        for item in self.items:
            item["y"] += fall_speed
            item_rect = pygame.Rect(item["x"], item["y"], item["width"], item["height"])
            if item_rect.colliderect(basket_rect):
                if item["kind"] == "good":
                    self.score += 1
                else:
                    self.lives -= 1
                continue
            if item["y"] > dms.SCREEN_HEIGHT:
                continue
            remaining.append(item)
        self.items = remaining

        if self.lives <= 0:
            self.lost = True
        elif self.score >= WIN_SCORE:
            self.won = True

    def draw(self, screen):
        self.tile_map.draw(screen)
        for item in self.items:
            screen.blit(item["frame"], (item["x"], item["y"]))
        screen.blit(self.basket_frame, self.basket_position)

        self._draw_hud(screen)

        if self.won or self.lost:
            self._finish(screen, won=self.won)

    def _draw_hud(self, screen):
        # White-on-translucent-black reads over any floor/wall color the
        # room might use, and sitting past HUD_MARGIN keeps it off the
        # wall border instead of getting drawn half inside it.
        hud_text = fnt.small_font.render(f"Score: {self.score}   Lives: {self.lives}", True, clr.WHITE)
        backing = pygame.Surface(
            (hud_text.get_width() + 2 * HUD_PADDING, hud_text.get_height() + 2 * HUD_PADDING), pygame.SRCALPHA
        )
        backing.fill((0, 0, 0, 150))
        screen.blit(backing, (HUD_MARGIN, HUD_MARGIN))
        screen.blit(hud_text, (HUD_MARGIN + HUD_PADDING, HUD_MARGIN + HUD_PADDING))

    def _finish(self, screen, won):
        message = "GREAT JOB!" if won else "Nice Try!"
        color = clr.DARK_GREEN if won else clr.NAVY
        text = fnt.font.render(message, True, color)
        screen.blit(text, (dms.SCREEN_WIDTH / 2 - text.get_width() / 2, dms.SCREEN_HEIGHT / 2 - 50))
        pygame.display.flip()
        pygame.time.wait(2500)
        aud.stop_music()
        self.state.record_high_score("catch_stars", self.score, higher_is_better=True)
        self.state.save()
        self.next_scene = screens.menu_end_minigame.EndMinigameScene(
            minigame_factory=lambda: CatchStarsScene(state=self.state), state=self.state,
        )

import numpy as np
import pygame

import constants.colors as clr
import constants.dimensions as dms
import constants.fonts as fnt
import functions.audio as aud
import functions.visual as viz
import objects.tilemap as tmp
import screens.menu_end_minigame
import screens.menu_pause
import screens.scene_base as scb

POOH_WIDTH, POOH_HEIGHT, POOH_SCALE = 60, 100, 1.5
GREEN_CIRCLE_WIDTH, GREEN_CIRCLE_HEIGHT = 90, 90
RED_X_WIDTH, RED_X_HEIGHT = 90, 90
BLACK_ARROW_WIDTH, BLACK_ARROW_HEIGHT = 90, 150
N_BOXES = 3
BOX_WIDTH, BOX_HEIGHT, BOX_SPACING = 90, 150, 200
WIN_TARGET_CORRECT_GUESSES = 3


def boxes_left_to_right(boxes):
    """boxes: {box_id: {'position_x': float, ...}} -> box ids ordered by
    their current x position. Pure logic (no pygame) so it's unit-testable;
    the original had this exact sort-and-lookup copy-pasted three times."""
    return [
        box_id for box_id, _ in
        sorted(((box_id, box["position_x"]) for box_id, box in boxes.items()), key=lambda item: item[1])
    ]


class FindPoohScene(scb.Scene):
    def __init__(self, state):
        super().__init__()
        self.state = state
        aud.play_looping_track(filename="sounds/sample_music_3.mp3")

        self.tile_map = tmp.TileMap(
            width=dms.SCREEN_WIDTH, height=dms.SCREEN_HEIGHT, tile_size=dms.TILE_SIZE,
            wall_color=clr.DARK_GREEN, floor_color=clr.LIGHT_GREY,
        )
        self.clock = pygame.time.Clock()  # paces the blocking animation helpers below

        self.pooh_frame = viz.load_static_frame("sprites/characters/pooh.png", POOH_WIDTH, POOH_HEIGHT, POOH_SCALE)
        self.green_circle_frame = viz.load_static_frame(
            "sprites/shapes/circle_green.png", GREEN_CIRCLE_WIDTH, GREEN_CIRCLE_HEIGHT, 1
        )
        self.red_x_frame = viz.load_static_frame("sprites/shapes/x_mark_red.png", RED_X_WIDTH, RED_X_HEIGHT, 1)
        self.black_arrow_frame = viz.load_static_frame(
            "sprites/shapes/up_arrow_black.png", BLACK_ARROW_WIDTH, BLACK_ARROW_HEIGHT, 1
        )

        self.pooh_position = self._pooh_home_position()
        self.pooh_visible = True
        self.pooh_box = -1
        self.green_circle_visible = False
        self.red_x_visible = False
        self.black_arrow_visible = False
        self.black_arrow_box = 0

        self.boxes = {
            i: {
                "position_x": dms.SCREEN_WIDTH / 2 - POOH_WIDTH / 2 * POOH_SCALE + BOX_SPACING * (i - (N_BOXES - 1) / 2),
                "position_y": 325,
            }
            for i in range(N_BOXES)
        }

        self.show_instructions = True
        self.correct_guesses = 0
        self.rounds_played = 0
        self.won = False

    def _pooh_home_position(self):
        return dms.SCREEN_WIDTH / 2 - POOH_WIDTH / 2 * POOH_SCALE, 80

    # --- discrete input -------------------------------------------------

    def handle_event(self, event, screen):
        if event.type != pygame.KEYDOWN or self.won:
            return
        if event.key == pygame.K_ESCAPE:
            self.next_scene = screens.menu_pause.PauseMenuScene(resume_scene=self, state=self.state)
        elif event.key == pygame.K_SPACE:
            self.show_instructions = False
            if self.pooh_visible:
                self._move_pooh_into_box(screen)
                self._shuffle_boxes(screen)
            else:
                correct = self._move_pooh_outside_box(screen)
                self.rounds_played += 1
                if correct:
                    self.correct_guesses += 1
                if self.correct_guesses >= WIN_TARGET_CORRECT_GUESSES:
                    self.won = True
        elif event.key == pygame.K_LEFT:
            self._move_black_arrow("left")
        elif event.key == pygame.K_RIGHT:
            self._move_black_arrow("right")

    def _move_black_arrow(self, direction):
        if not self.black_arrow_visible:
            return
        order = boxes_left_to_right(self.boxes)
        current = order.index(self.black_arrow_box)
        if direction == "left":
            self.black_arrow_box = order[(current - 1) % len(order)]
        elif direction == "right":
            self.black_arrow_box = order[(current + 1) % len(order)]

    # --- blocking animations (self-contained, don't call other scenes) --

    def _draw_transit_frame(self, screen, show_indicators):
        screen.fill(clr.WHITE)
        self.tile_map.draw(screen)
        screen.blit(self.pooh_frame, self.pooh_position)
        self._draw_boxes(screen)
        if show_indicators:
            self._draw_green_circle(screen)
            self._draw_red_x(screen)
            self._draw_black_arrow(screen)
        pygame.display.flip()

    def _move_pooh_into_box(self, screen):
        box = np.random.choice(a=list(self.boxes), size=1, replace=False).tolist()[0]
        self.pooh_box = box
        box_x = self.boxes[box]["position_x"]
        box_y = self.boxes[box]["position_y"]
        pooh_x, pooh_y = self.pooh_position

        while abs(pooh_x - box_x) > 2:
            pooh_x += (box_x - pooh_x) / 10
            self.pooh_position = (pooh_x, pooh_y)
            self._draw_transit_frame(screen, show_indicators=False)
            self.clock.tick(30)
        while abs(pooh_y - box_y) > 5:
            pooh_y += (box_y - pooh_y) / 10
            self.pooh_position = (pooh_x, pooh_y)
            self._draw_transit_frame(screen, show_indicators=False)
            self.clock.tick(30)

        self.pooh_visible = False
        self.black_arrow_visible = True

    def _move_pooh_outside_box(self, screen):
        box = self.pooh_box
        self.pooh_visible = True
        self.black_arrow_visible = False
        correct = self.black_arrow_box == box
        if correct:
            self.green_circle_visible = True
        else:
            self.red_x_visible = True

        final_x, final_y = self._pooh_home_position()
        pooh_x = self.boxes[box]["position_x"]
        pooh_y = self.boxes[box]["position_y"]
        self.pooh_position = (pooh_x, pooh_y)

        while abs(pooh_y - final_y) > 5:
            pooh_y += (final_y - pooh_y) / 10
            self.pooh_position = (pooh_x, pooh_y)
            self._draw_transit_frame(screen, show_indicators=True)
            self.clock.tick(30)
        while abs(pooh_x - final_x) > 2:
            pooh_x += (final_x - pooh_x) / 10
            self.pooh_position = (pooh_x, pooh_y)
            self._draw_transit_frame(screen, show_indicators=True)
            self.clock.tick(30)

        self.green_circle_visible = False
        self.red_x_visible = False
        self.black_arrow_visible = False
        return correct

    def _shuffle_boxes(self, screen):
        n_shuffles = np.random.choice(a=[5, 10, 15], size=1, replace=False).tolist()[0]
        for _ in range(n_shuffles):
            box_a, box_b = np.random.choice(a=list(self.boxes), size=2, replace=False).tolist()
            x_a, y_a = self.boxes[box_a]["position_x"], self.boxes[box_a]["position_y"]
            x_b, y_b = self.boxes[box_b]["position_x"], self.boxes[box_b]["position_y"]
            box_a_moves_up_first = np.random.choice(a=["up", "down"], size=1, replace=False).tolist()[0] == "up"
            speed = np.random.choice(a=[30, 60, 90], size=1, replace=False).tolist()[0]

            thetas_up_ccw = np.linspace(start=0, stop=np.pi, num=speed)
            thetas_down_ccw = np.linspace(start=np.pi, stop=2 * np.pi, num=speed)
            thetas_up_cw = np.linspace(start=np.pi, stop=0, num=speed)
            thetas_down_cw = np.linspace(start=2 * np.pi, stop=np.pi, num=speed)

            center_x = 0.5 * (x_a + x_b)
            center_y = 0.5 * (y_a + y_b)
            radius = 0.5 * abs(x_a - x_b)

            if x_a < x_b:
                thetas_a, thetas_b = (thetas_up_cw, thetas_down_cw) if box_a_moves_up_first else (thetas_down_ccw, thetas_up_ccw)
            else:
                thetas_a, thetas_b = (thetas_up_ccw, thetas_down_ccw) if box_a_moves_up_first else (thetas_down_cw, thetas_up_cw)

            for theta_a, theta_b in zip(thetas_a, thetas_b):
                self.boxes[box_a]["position_x"] = radius * np.cos(theta_a) + center_x
                self.boxes[box_a]["position_y"] = radius * np.sin(theta_a) + center_y
                self.boxes[box_b]["position_x"] = radius * np.cos(theta_b) + center_x
                self.boxes[box_b]["position_y"] = radius * np.sin(theta_b) + center_y
                screen.fill(clr.WHITE)
                self.tile_map.draw(screen)
                self._draw_boxes(screen)
                pygame.display.flip()
                self.clock.tick(60)

        order = boxes_left_to_right(self.boxes)
        self.black_arrow_box = order[0]

    # --- drawing ----------------------------------------------------------

    def _draw_boxes(self, screen):
        for box in self.boxes.values():
            viz.draw_rectangle(
                screen=screen, x=box["position_x"], y=box["position_y"],
                color=clr.NAVY, width=BOX_WIDTH, height=BOX_HEIGHT,
            )
            viz.draw_rectangle(
                screen=screen, x=box["position_x"] - 5, y=box["position_y"],
                color=clr.BLACK, width=BOX_WIDTH + 10, height=10,
            )

    def _draw_green_circle(self, screen):
        if self.green_circle_visible and self.pooh_box > -1:
            box_x = self.boxes[self.black_arrow_box]["position_x"]
            screen.blit(self.green_circle_frame, (box_x, 500))

    def _draw_red_x(self, screen):
        if self.red_x_visible and self.pooh_box > -1:
            box_x = self.boxes[self.black_arrow_box]["position_x"]
            screen.blit(self.red_x_frame, (box_x, 500))

    def _draw_black_arrow(self, screen):
        if self.black_arrow_visible:
            box_x = self.boxes[self.black_arrow_box]["position_x"]
            screen.blit(self.black_arrow_frame, (box_x, 500))

    def _draw_instructions(self, screen):
        if self.show_instructions:
            instructions = fnt.font.render("Press Space to Begin", True, clr.BLACK)
            screen.blit(instructions, (dms.SCREEN_WIDTH / 2 - len("Press Space to Begin") * 13, 600))

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(clr.WHITE)
        self.tile_map.draw(screen)
        if self.pooh_visible:
            screen.blit(self.pooh_frame, self.pooh_position)
        self._draw_boxes(screen)
        self._draw_green_circle(screen)
        self._draw_red_x(screen)
        self._draw_black_arrow(screen)
        self._draw_instructions(screen)

        if self.won:
            self._celebrate_and_finish(screen)

    def _celebrate_and_finish(self, screen):
        screen.fill(clr.WHITE)
        self.tile_map.draw(screen)
        congratulations_text = fnt.font.render("GREAT JOB!", True, clr.DARK_GREEN)
        screen.blit(congratulations_text, (dms.SCREEN_WIDTH / 2 - 150, dms.SCREEN_HEIGHT / 2 - 50))
        pygame.display.flip()
        pygame.time.wait(3000)
        aud.stop_music()
        self.state.record_high_score("find_pooh", self.rounds_played, higher_is_better=False)
        self.state.save()
        self.next_scene = screens.menu_end_minigame.EndMinigameScene(
            minigame_factory=lambda: FindPoohScene(state=self.state), state=self.state,
        )

import pygame

import constants.colors as clr
import functions.visual as viz


def render_door_icon(size, body_color, frame_color):
    """Draw a simple stylized door (no art asset needed) for doors that
    don't have hand-made icon art, e.g. room-to-room exits."""
    width, height = size
    surface = pygame.Surface(size, pygame.SRCALPHA)
    pygame.draw.rect(surface, frame_color, (0, 0, width, height), border_radius=10)
    inset = 8
    pygame.draw.rect(
        surface, body_color,
        (inset, inset, width - 2 * inset, height - 2 * inset),
        border_radius=8,
    )
    knob_center = (int(width * 0.75), int(height * 0.55))
    pygame.draw.circle(surface, frame_color, knob_center, max(4, width // 20))
    return surface


class Door:
    """Something in a room the player can walk up to and activate with
    Space: a minigame entrance or a passage to another room. Handles its own
    proximity-based highlighting so every room draws doors the same way."""

    def __init__(self, door_id, label, position, frame_unselected, frame_selected,
                 on_enter, activation_radius=250):
        self.id = door_id
        self.label = label
        self.position = position
        self.on_enter = on_enter
        self.activation_radius = activation_radius
        self.selected = False
        self._frame_unselected = frame_unselected
        self._frame_selected = frame_selected

    @classmethod
    def from_icon_files(cls, door_id, label, position, icon_unselected, icon_selected,
                         on_enter, size=(200, 200), activation_radius=250):
        frame_unselected = viz.get_frame(
            sheet=pygame.image.load(icon_unselected).convert_alpha(),
            frame_width=size[0], frame_height=size[1], column=0, row=0, scale_factor=1,
        )
        frame_selected = viz.get_frame(
            sheet=pygame.image.load(icon_selected).convert_alpha(),
            frame_width=size[0], frame_height=size[1], column=0, row=0, scale_factor=1,
        )
        return cls(door_id, label, position, frame_unselected, frame_selected, on_enter, activation_radius)

    @classmethod
    def plain(cls, door_id, label, position, on_enter, size=(120, 160), activation_radius=200,
              body_color=clr.NAVY, selected_body_color=clr.LIGHT_BLUE, frame_color=clr.BLACK):
        frame_unselected = render_door_icon(size, body_color, frame_color)
        frame_selected = render_door_icon(size, selected_body_color, frame_color)
        return cls(door_id, label, position, frame_unselected, frame_selected, on_enter, activation_radius)

    def update_selection(self, player_position):
        px, py = player_position
        cx, cy = self.position
        self.selected = abs(px - cx) < self.activation_radius and abs(py - cy) < self.activation_radius
        return self.selected

    def draw(self, screen, player_position, font, text_color=clr.BLACK, selected_text_color=clr.BLUE):
        frame = self._frame_selected if self.selected else self._frame_unselected
        screen.blit(frame, self.position)

        title_position = (self.position[0] + 10, self.position[1] - 30)
        px, py = player_position
        near_label = abs(px - title_position[0]) < 50 and abs(py - title_position[1]) < 50
        if not near_label:
            color = selected_text_color if self.selected else text_color
            label_surface = font.render(self.label, True, color)
            screen.blit(label_surface, title_position)

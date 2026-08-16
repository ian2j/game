import pygame


def draw_circle(screen, x_center, y_center, radius, color):
    pygame.draw.circle(surface=screen, color=color, center=(x_center, y_center), radius=radius)
    return None


def draw_rectangle(screen, x, y, color, width, height):
    pygame.draw.rect(surface=screen, color=color, rect=(x, y, width, height))
    return None


def draw_button(screen, text, x, y, button_color, text_color, width, height, font):
    pygame.draw.rect(surface=screen, color=button_color, rect=(x, y, width, height))
    button_text = font.render(text, True, text_color)
    text_rect = button_text.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(button_text, text_rect)
    return None


def get_frame(sheet, frame_width, frame_height, column, row, scale_factor=1):
    frame_rect = pygame.Rect(column * frame_width, row * frame_height, frame_width, frame_height)
    frame = sheet.subsurface(frame_rect)
    new_width = int(frame_width * scale_factor)
    new_height = int(frame_height * scale_factor)
    return pygame.transform.scale(frame, size=(new_width, new_height))


def load_static_frame(path, width, height, scale=1):
    """Load an image file and pull out its single (column 0, row 0) frame,
    scaled. A shorthand for the many places that need one fixed sprite
    rather than a full animated sheet."""
    sheet = pygame.image.load(path).convert_alpha()
    return get_frame(sheet=sheet, frame_width=width, frame_height=height, column=0, row=0, scale_factor=scale)

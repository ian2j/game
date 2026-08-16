import sys

import pygame

import functions.audio as aud


class _Quit:
    """Sentinel next_scene value meaning 'exit the game'."""

    def __repr__(self):
        return "QUIT"


QUIT = _Quit()


class Scene:
    """Base class for every game screen.

    A scene owns one screenful of behavior (a menu, the overworld, a
    minigame). It never calls into another scene directly - instead it sets
    self.next_scene, and the run() loop below performs the actual switch.
    This keeps the call stack flat no matter how long a play session runs
    or how many screens it visits.

    next_scene meanings:
        None        - keep running this scene
        Scene       - switch to this scene next frame
        QUIT        - stop the game
    """

    def __init__(self):
        self.next_scene = None

    def handle_event(self, event, screen):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def draw(self, screen):
        raise NotImplementedError


def run(screen, initial_scene, fps=60):
    """The one real game loop. Pumps events into the current scene, updates
    and draws it, and swaps scenes when it asks to."""
    clock = pygame.time.Clock()
    scene = initial_scene

    while True:
        dt = clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                scene.next_scene = QUIT
            else:
                scene.handle_event(event, screen)

        scene.update(dt)
        scene.draw(screen)
        pygame.display.flip()

        if scene.next_scene is QUIT:
            state = getattr(scene, "state", None)
            if state is not None:
                state.save()
            aud.stop_music()
            pygame.quit()
            sys.exit()
        elif scene.next_scene is not None:
            scene = scene.next_scene

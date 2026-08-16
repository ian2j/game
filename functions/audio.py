import constants.settings as stt
import pygame

_mixer_ready = False


def start_mixer():
    global _mixer_ready
    pygame.mixer.init(buffer=stt.AUDIO_BUFFER)
    _mixer_ready = True
    return None


def load_music(filename):
    pygame.mixer.music.load(filename=filename)
    return None


def play_music():
    pygame.mixer.music.play()
    return None


def play_music_on_loop():
    pygame.mixer.music.play(-1)
    return None


def stop_music():
    pygame.mixer.music.stop()
    return None


def play_looping_track(filename):
    """Make sure the mixer is initialized (only once - previously every
    screen re-checked a flag that was never actually set), then load and
    loop a track. This is what every scene used to do by hand."""
    if not _mixer_ready:
        start_mixer()
    load_music(filename=filename)
    play_music_on_loop()
    return None

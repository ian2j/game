import constants.settings as stt
import pygame


def start_mixer():
    pygame.mixer.init(buffer=stt.AUDIO_BUFFER)
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



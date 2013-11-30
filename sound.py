import pygame
import time

pygame.mixer.init()
def music():
    pygame.mixer.music.load("assets/test.wav")
    pygame.mixer.music.play()

def sound():
    sound = pygame.mixer.Sound("assets/test.wav")
    sound.play()
time.sleep(200)
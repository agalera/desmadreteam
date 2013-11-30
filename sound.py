import pygame
import time

pygame.mixer.init()
def music():
    pygame.mixer.music.load("test.wav")
    pygame.mixer.music.play()

def sound():
    sound = pygame.mixer.Sound("test.wav")
    sound.play()
time.sleep(200)
from PPlay.window import Window
from PPlay.scenemanager import SceneManager
from classes.cenas import Menu, Jogo
from player import Volpina
from PPlay.input_manager import InputManager
import pygame, ctypes

pygame.init()
icone = pygame.image.load("recursos/volpina/obj.png")
pygame.display.set_icon(icone)

janela = Window(800, 444, "Batalha Miraculous All-Stars")

SW_MAXIMIZE = 3
ctypes.windll.user32.ShowWindow(pygame.display.get_wm_info()["window"], SW_MAXIMIZE)

controls = InputManager()
SceneManager.change_scene(Menu(255, controls))

while True:
    SceneManager.run()
    janela.update()


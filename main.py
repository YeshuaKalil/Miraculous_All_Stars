from PPlay.window import Window
from PPlay.scenemanager import SceneManager
from classes.cenas import Menu, Jogo
from player import Volpina
from PPlay.input_manager import InputManager



janela = Window(800, 444, "Batalha Miraculous All-Stars")

controls = InputManager()
SceneManager.change_scene(Menu(255, controls))

while True:
    SceneManager.run()
    janela.update()


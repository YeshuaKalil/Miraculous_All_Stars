from PPlay.window import Window
from PPlay.scenemanager import SceneManager
from classes.cenas import Menu, Jogo
from player import Volpina



janela = Window(800, 444, "Batalha Miraculous All-Stars")
SceneManager.change_scene(Menu(255))

while True:
    SceneManager.run()
    janela.update()


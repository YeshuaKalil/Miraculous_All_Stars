from PPlay.scenemanager import SceneManager, Scene
from PPlay.sprite import Sprite
from classes.button import Button
from classes.mover import Mover
from classes.jogador import Jogador
from PPlay.physics import Physics
from player import Volpina
import time

class Menu(Scene):
    button = []
    
    def __init__(self, transp):
        self.fundo = Sprite("recursos/fundo.png")
        super().__init__()
        a = 75
        self.logo = Sprite("recursos/logo.png")
        self.logo.set_position(30, 50)
        self.transp = transp
        self.preto = Sprite("recursos/prato.png")
        self.button.append(Button(Jogo(), "recursos/button0.png", 120, 160))
        self.button.append(Button(Opcao(), "recursos/button1.png", 120, 160+a))
        self.button.append(Button(Sair(), "recursos/button2.png", 120, 160+2*a))

    def loop(self):
        if self.transp > 0:
            self.transp -=2
        for b in self.button:
            if b.update():
                SceneManager.change_scene(b.get_scene())

    def draw(self):
        self.fundo.draw()
        self.preto.image.set_alpha(self.transp)
        self.preto.draw()
        self.logo.draw()
        for b in self.button:
            b.draw()
        self.janela.set_background_color((0,0,0))
        
class InputBuffer():
    def __init__(self):
        self.inputs = []
    
    def add(self, input):
        self.inputs.append({"input": input, "time": time.time()})
        
    def get_inputs(self):
        return self.inputs
    
    def clear(self):
        self.inputs = []
        

class Jogo(Scene):
    def __init__(self):
                super().__init__()

                self.jogador = Volpina(300, 300)
                self.chao = Sprite("recursos/prato.png")
                self.chao.set_position(0, 400)
                self.chao.image.set_alpha(255)
                #self.fisica = Physics(gravidade=5500)
                #self.jogador.setup_physics(self.fisica, controlavel=False)
                self.fundoB = Sprite("recursos/fundoB.png")
                self.fundoB.set_position(0, 100)
                self.key=""
                self.keyCounter = 0
                self.keyCurrent = ""
                self.buffer = InputBuffer()
                
    def readInput(self):
        #if (self.teclado.key_down("LEFT")): self.buffer.add("LEFT")
        #if (self.teclado.key_down("RIGHT")): self.buffer.add("RIGHT")
        if (self.teclado.key_down("UP")): self.buffer.add("UP")
        if (self.teclado.key_down("DOWN")): self.buffer.add("DOWN")
        if (self.teclado.key_down("w")): self.buffer.add("w")
        if (self.teclado.key_down("e")): self.buffer.add("e")
        if (self.teclado.key_down("s")): self.buffer.add("s")
        if (self.teclado.key_down("d")): self.buffer.add("d")
        if (self.teclado.key_down("t")): self.buffer.add("t")
        
    
    def loop(self):
        #self.keyCurrent = self.readInput(self.keyCurrent)
        #self.jogador.move(self.keyCurrent, self.janela.delta_time())
        #Eself.keyCounter+=self.janela.delta_time()
        #if self.keyCounter > 0.05:
         #   self.key += self.keyCurrent
          #  self.keyCounter = 0
           # self.keyCurrent = ""
                
        #self.key = self.jogador.update(self.janela, self.key, self.chao)
        self.readInput()
        self.jogador.update(self.janela, self.buffer, self.chao)
        if len(self.buffer.get_inputs())>20:
            self.buffer.clear()
        
        if self.teclado.key_pressed("ESC"):
            SceneManager.change_scene(Menu(0))

    def draw(self):
        self.janela.set_background_color((0,0,0))
        self.fundoB.draw()
        self.chao.image.set_alpha(255)
        self.chao.draw()
        self.jogador.draw()
        

class Opcao(Scene):
    transp = 0
    mover = []
    def __init__(self):
            self.fundo = Sprite("recursos/fundo.png")
            super().__init__()
            self.preto = Sprite("recursos/prato.png")
            self.logo = Sprite("recursos/logo.png")
            self.logo.set_position(30, 50)
            self.config = Sprite("recursos/config2.png")
            self.config.set_position(self.janela.width/2-self.config.width/2, 100)
            self.button = Button(None, "recursos/button3.png", self.janela.width/2+50, 270)
            self.mover.append(Mover("recursos/mover.png", 361, 131))
            self.mover.append(Mover("recursos/mover.png", 361, 175))
            self.mover.append(Mover("recursos/mover.png", 361, 206))
    
    def loop(self):
        if self.teclado.key_pressed("ESC"):
                    SceneManager.change_scene(Menu(self.transp))
        if self.transp < 155:
            self.transp +=2
        if self.button.update():
             SceneManager.change_scene(Menu(self.transp))
        for m in self.mover:
            m.update()

    def draw(self):
        self.fundo.draw()
        self.preto.image.set_alpha(self.transp)
        self.preto.draw()
        #self.logo.draw()
        self.config.draw()
        self.button.draw()
        for m in self.mover:
             m.draw()

class Sair(Scene):
    def loop(self):
        self.janela.close()

    def draw(self):
        self.janela.set_background_color((222,222,0))
from PPlay.scenemanager import SceneManager, Scene
from PPlay.sprite import Sprite
from classes.button import Button
from classes.mover import Mover
from classes.jogador import Jogador
from PPlay.physics import Physics
from PPlay.input_manager import InputManager
from PPlay.uikit import ProgressBar
from player import Volpina, Mimico
from object import Object
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
        self.button.append(Button(Select(), "recursos/button0.png", 120, 160))
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
        
class Select(Scene):
    def __init__(self):
        self.fundo = Sprite("recursos/character_select.png")
        self.p1 = None
        self.p2 = None
        super().__init__()
    
    def loop(self):
        if self.teclado.key_pressed("SPACE"):
            self.p1 = Volpina
            self.p2 = Mimico
            SceneManager.change_scene(Jogo(self.p1, self.p2))
            
    def draw(self):
        self.fundo.draw()
            
        
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
    def __init__(self, p1, p2):
                super().__init__()

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
                self.buffers = [InputBuffer(), InputBuffer()]
                self.inputs = InputManager()
                self.inputs.define_action("cima1", "w")
                self.inputs.define_action("baixo1", "s")
                self.inputs.define_action("esquerda1", "a")
                self.inputs.define_action("direita1", "d")
                self.inputs.define_action("wp1", "u")
                self.inputs.define_action("mp1", "i")
                self.inputs.define_action("wk1", "j")
                self.inputs.define_action("mk1", "k")
                self.inputs.define_action("pw1", "p")
                
                self.inputs.define_action("cima2", "UP")
                self.inputs.define_action("baixo2", "DOWN")
                self.inputs.define_action("esquerda2", "LEFT")
                self.inputs.define_action("direita2", "RIGHT")
                self.inputs.define_action("wp2", "7")
                self.inputs.define_action("mp2", "8")
                self.inputs.define_action("wk2", "9")
                self.inputs.define_action("mk2", "0")
                self.inputs.define_action("pw2", "=")
                
                # Colocar para qualquer personagem
                self.objetos = [Object(0, 0, f"recursos/{p1.name}/obj.png", None), Object(0, 0, f"recursos/{p2.name}/obj.png", None)]
                
                self.p1 = p1(200, 400, ["w", "s", "a", "d"], self.objetos[0])
                self.p2 = p2(472, 400, ["UP", "DOWN", "LEFT", "RIGHT"], self.objetos[1])
                
                self.objetos[0].pai = self.p1
                self.objetos[0].portador = self.p1
                
                self.objetos[1].pai = self.p2
                self.objetos[1].portador = self.p2
                
                self.vida1 = ProgressBar(300, 20, "green", "black")
                self.vida1.set_position(50,40)
                self.vida1.valor_max = 100
                
                self.vida2 = ProgressBar(300, 20, "green", "black")
                self.vida2.set_position(450,40)
                self.vida2.valor_max = 100
                
                self.espelhado1 = False
                self.espelhado2 = True
                
    def readInput(self, jogador):
        #if (self.teclado.key_down("LEFT")): self.buffer.add("LEFT")
        #if (self.teclado.key_down("RIGHT")): self.buffer.add("RIGHT")
        if (self.inputs.action_pressed("cima"+str(jogador+1))): self.buffers[jogador].add("cima")
        if (self.inputs.action_pressed("baixo"+str(jogador+1))): self.buffers[jogador].add("baixo")
        if (self.inputs.action_pressed("wp"+str(jogador+1))): self.buffers[jogador].add("wp")
        if (self.inputs.action_pressed("mp"+str(jogador+1))): self.buffers[jogador].add("mp")
        if (self.inputs.action_pressed("wk"+str(jogador+1))): self.buffers[jogador].add("wk")
        if (self.inputs.action_pressed("mk"+str(jogador+1))): self.buffers[jogador].add("mk")
        if (self.inputs.action_pressed("pw"+str(jogador+1))): self.buffers[jogador].add("pw")
      
    def checkCollision(self, Oattack, hit, espelhado):
        if len(Oattack)<3 or Oattack[2] is None:
            return None
        
        attack = list(Oattack)
        attack[2] = list(Oattack[2])
        if espelhado:
            attack[2][2] = 128 - attack[2][2] - attack[2][0] #depois trocar 128 pela largura do sprite
        
        minXH = hit[0][0] + hit[1]["high"][2]
        minYH = hit[0][1] + hit[1]["high"][3]
        minXL = hit[0][0] + hit[1]["low"][2]
        minYL = hit[0][1] + hit[1]["low"][3]
        
        maxXH = hit[0][0] + hit[1]["high"][2] + hit[1]["high"][0]
        maxYH = hit[0][1] + hit[1]["high"][3] + hit[1]["high"][1]
        maxXL = hit[0][0] + hit[1]["low"][2] + hit[1]["low"][0]
        maxYL = hit[0][1] + hit[1]["low"][3] + hit[1]["low"][1]
        
        if attack[0][0] + attack[2][2] + attack[2][0] > minXH and attack[0][0] + attack[2][2] < maxXH and attack[0][1] + attack[2][3] + attack[2][1] > minYH and attack[0][1] + attack[2][3] < maxYH:
            return ["high", attack[2][4]]
        elif attack[0][0] + attack[2][2] + attack[2][0] > minXL and attack[0][0] + attack[2][2] < maxXL and attack[0][1] + attack[2][3] + attack[2][1] > minYL and attack[0][1] + attack[2][3] < maxYL:
            return ["low", attack[2][4]]
        else:
            return None
    
    def loop(self):
        #self.keyCurrent = self.readInput(self.keyCurrent)
        #self.jogador.move(self.keyCurrent, self.janela.delta_time())
        #Eself.keyCounter+=self.janela.delta_time()
        #if self.keyCounter > 0.05:
         #   self.key += self.keyCurrent
          #  self.keyCounter = 0
           # self.keyCurrent = ""
                
        #self.key = self.jogador.update(self.janela, self.key, self.chao)
        self.readInput(0)
        self.readInput(1)
        
        defending1 = False
        defending2 = False
        if not self.p1.occupied():
            if self.p1.x > self.p2.x:
                self.espelhado1 = True
                if self.inputs.is_active("direita1"):
                    defending1 = True
            else:
                self.espelhado1 = False
                if self.inputs.is_active("esquerda1"):
                    defending1 = True
        
        if not self.p2.occupied():
            if self.p2.x > self.p1.x:
                self.espelhado2 = True
                if self.inputs.is_active("direita2"):
                    defending2 = True
            else:
                self.espelhado2 = False
                if self.inputs.is_active("esquerda2"):
                    defending2 = True
        
            
        
        
        col1 = self.p1.update(self.janela, self.buffers[0], self.chao, self.objetos)
        col2 = self.p2.update(self.janela, self.buffers[1], self.chao, self.objetos)
        
        if col1 == "FIM":
            print("P1 GANHOU!")
            SceneManager.change_scene(Menu(0))
            return
        
        if col2 == "FIM":
            print("P2 GANHOU!")
            SceneManager.change_scene(Menu(0))
            return
        
        for object in self.objetos:
            object.update(self.janela, self.chao)
        
        self.p2.hit(self.checkCollision(col1, col2, self.espelhado1), defending2)
        self.p1.hit(self.checkCollision(col2, col1, self.espelhado2), defending1)
        
        self.vida1.set_value(self.p1.get_vida())
        self.vida2.set_value(self.p2.get_vida())
        
        if self.vida1.valor_atual <= 0 or self.vida2.valor_atual <= 0:
            if self.vida1.valor_atual == 0 and self.vida2.valor_atual == 0:
                print("EMPATE!")
            elif self.vida1.valor_atual == 0:
                print("P2 GANHOU!")
            else:
                print("P1 GANHOU!")
                
            SceneManager.change_scene(Menu(0))
                
        
        if self.teclado.key_pressed("ESC"):
            SceneManager.change_scene(Menu(0))

    def draw(self):
        self.janela.set_background_color((0,0,0))
        self.fundoB.draw()
        self.chao.image.set_alpha(255)
        self.chao.draw()
        self.p1.draw(self.espelhado1, self.objetos)
        self.p2.draw(self.espelhado2, self.objetos)
        for object in self.objetos:
            object.draw()
        self.vida1.draw()
        self.vida2.draw()
        

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
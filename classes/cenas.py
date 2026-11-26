from PPlay.scenemanager import SceneManager, Scene
from PPlay.sprite import Sprite
from classes.button import Button
from classes.mover import Mover
from classes.jogador import Jogador
from PPlay.physics import Physics
from PPlay.input_manager import InputManager
from PPlay.uikit import ProgressBar
from player import Volpina, Mimico
from PPlay.gameimage import GameImage
from object import Object
import time
from PPlay.camera import Camera
from PPlay.fontes import Fontes
Fontes.registrar("Pixel", "recursos/pixel.ttf")

class Menu(Scene):
    button = []
    
    def __init__(self, transp, controls):
        self.fundo = GameImage("recursos/fundo.png")
        super().__init__()
        a = 75
        self.logo = GameImage("recursos/logo.png")
        self.logo.set_position(30, 50)
        self.transp = transp
        self.controls = controls
        self.preto = GameImage("recursos/prato.png")
        self.button.append(Button(Select(self.controls), "recursos/button0.png", 120, 160))
        self.button.append(Button(Opcao(self.controls), "recursos/button1.png", 120, 160+a))
        self.button.append(Button(Sair(), "recursos/button2.png", 120, 160+2*a))
        
        controls.define_action("cima1", "w")
        controls.define_action("baixo1", "s")
        controls.define_action("esquerda1", "a")
        controls.define_action("direita1", "d")
        controls.define_action("wp1", "u")
        controls.define_action("mp1", "i")
        controls.define_action("wk1", "j")
        controls.define_action("mk1", "k")
        controls.define_action("pw1", "p")
                                
        controls.define_action("cima2", "UP")
        controls.define_action("baixo2", "DOWN")
        controls.define_action("esquerda2", "LEFT")
        controls.define_action("direita2", "RIGHT")
        controls.define_action("wp2", "7")
        controls.define_action("mp2", "8")
        controls.define_action("wk2", "9")
        controls.define_action("mk2", "0")
        controls.define_action("pw2", "6")
        

    def loop(self):
        #SceneManager.change_scene(Jogo(self.controls, Volpina, Volpina))
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
    def __init__(self, controls):
        self.fundo = GameImage("recursos/prato.png")
        self.controls = controls
        self.p1 = Volpina
        self.p2 = Mimico
        
        self.j1 = GameImage("recursos/j1.png")
        self.j2 = GameImage("recursos/j2.png")
        self.display1 = {
            (-91, 91): GameImage("recursos/displayVolpina.png"),
            (91, 91): GameImage("recursos/displayMimico.png")
        }
        self.display2 = {
            (-91, 91): GameImage("recursos/displayVolpina.png"),
            (91, 91): GameImage("recursos/displayMimico.png")
        }
        for i in self.display1:
            self.display1[i].set_position(-50,30)
        for i in self.display2:
            self.display2[i].set_position(392, 30)
            self.display2[i].set_espelhado(True)
            
        self.aval1 = False
        self.aval2 = False
        
        self.j1.set_position(-91, 91)
        self.j2.set_position(91, 91)
        self.j1.image.set_alpha(80)
        self.j2.image.set_alpha(80)
        self.coord = {
            (-91, 91): Volpina,
            (91, 91): Mimico
        }
        self.select = GameImage("recursos/select.png")
        super().__init__()
    
    def loop(self):
        self.display1[(self.j1.x, self.j1.y)].x += 500*self.janela.delta_time()
        self.display2[(self.j2.x, self.j2.y)].x -= 500*self.janela.delta_time()
        if self.display1[(self.j1.x, self.j1.y)].x > -50:
            self.display1[(self.j1.x, self.j1.y)].x = -50
        if self.display2[(self.j2.x, self.j2.y)].x < 392:
            self.display2[(self.j2.x, self.j2.y)].x = 392
        if (not self.aval1) and (self.controls.action_pressed("esquerda1") or self.controls.action_pressed("direita1")):
            self.j1.x *= -1
            self.display1[(self.j1.x, self.j1.y)].x = -150
        if (not self.aval2) and (self.controls.action_pressed("esquerda2") or self.controls.action_pressed("direita2")):
            self.j2.x *= -1
            self.display2[(self.j2.x, self.j2.y)].x = 492
        
        if self.controls.action_pressed("wp1") or self.controls.action_pressed("mp1") or self.controls.action_pressed("wk1") or self.controls.action_pressed("mk1"):
            self.aval1 = True
        if self.controls.action_pressed("wp2") or self.controls.action_pressed("mp2") or self.controls.action_pressed("wk2") or self.controls.action_pressed("mk2"):
            self.aval2 = True
        
        if self.aval1 and self.aval2:
            self.p1 = self.coord[(self.j1.x, self.j1.y)]
            self.p2 = self.coord[(self.j2.x, self.j2.y)]
            SceneManager.change_scene(Jogo(self.controls, self.p1, self.p2))
        
            
    def draw(self):
        #self.fundo.draw()
        self.janela.set_background_color((0,30,0))
        self.display1[(self.j1.x, self.j1.y)].draw()
        self.display2[(self.j2.x, self.j2.y)].draw()
        self.select.draw()
        if not self.aval1:
            self.j1.draw()
        if not self.aval2:
            self.j2.draw()
            
        
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
    def __init__(self, controls, p1, p2):
                super().__init__()

                self.chao = Sprite("recursos/chao.png")
                self.chao.set_position(-400, 400)
                self.chao.image.set_alpha(255)
                #self.fisica = Physics(gravidade=5500)
                #self.jogador.setup_physics(self.fisica, controlavel=False)
                self.fundoB = GameImage("recursos/fundoB.png")
                self.fundoB.set_position(0, 100)
                self.key=""
                self.keyCounter = 0
                self.keyCurrent = ""
                self.buffers = [InputBuffer(), InputBuffer()]
                
                self.controls = controls
                
                # Colocar para qualquer personagem
                self.objetos = [Object(0, 0, f"recursos/{p1.name}/obj.png", None), Object(0, 0, f"recursos/{p2.name}/obj.png", None)]
                
                # Corrigir para controle configuravel
                self.p1 = p1(200, self.chao.y, ["w", "s", "a", "d"], self.objetos[0])
                self.p2 = p2(472, self.chao.y, ["UP", "DOWN", "LEFT", "RIGHT"], self.objetos[1])
                
                self.objetos[0].pai = self.p1
                self.objetos[0].portador = self.p1
                
                self.objetos[1].pai = self.p2
                self.objetos[1].portador = self.p2
                
                self.vida1 = ProgressBar(300, 30, "green", "black")
                self.vida1.set_position(50,40)
                self.vida1.valor_max = 100
                
                self.vida2 = ProgressBar(300, 30, "green", "black")
                self.vida2.set_position(450,40)
                self.vida2.valor_max = 100
                
                self.espelhado1 = False
                self.espelhado2 = True
                
                self.sameHit1 = 0
                self.hitCounter1 = 0
                self.sameHit2 = 0
                self.hitCounter2 = 0
                
                self.beggining = 0
                self.ending = 0
                self.vencedor = 0
                
                self.camera = Camera(800, 444) # mesmo tamanho da janela
                #self.camera.set_world_bounds(3200, 1200)
                self.astro = Sprite("recursos/volpina/idle.png")
                self.astro.set_position((self.p1.x+self.p2.x)/2, min(self.p1.y, self.p2.y))
                
    def readInput(self, jogador):
        #if (self.teclado.key_down("LEFT")): self.buffer.add("LEFT")
        #if (self.teclado.key_down("RIGHT")): self.buffer.add("RIGHT")
        if (self.controls.action_pressed("cima"+str(jogador+1))): self.buffers[jogador].add("cima")
        if (self.controls.action_pressed("baixo"+str(jogador+1))): self.buffers[jogador].add("baixo")
        if (self.controls.action_pressed("wp"+str(jogador+1))): self.buffers[jogador].add("wp")
        if (self.controls.action_pressed("mp"+str(jogador+1))): self.buffers[jogador].add("mp")
        if (self.controls.action_pressed("wk"+str(jogador+1))): self.buffers[jogador].add("wk")
        if (self.controls.action_pressed("mk"+str(jogador+1))): self.buffers[jogador].add("mk")
        if (self.controls.action_pressed("pw"+str(jogador+1))): self.buffers[jogador].add("pw")
      
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
        self.astro.set_position((self.p1.x+self.p2.x)/2, min(self.p1.y, self.p2.y)-50)
        self.camera.follow(self.astro)
        
        if self.beggining < 4:
            self.beggining += self.janela.delta_time()
            return
        if self.ending > 0:
            self.ending += self.janela.delta_time()
            if self.ending > 3:
                SceneManager.change_scene(Menu(0, self.controls))
            return
        
        
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
                if self.controls.is_active("direita1"):
                    defending1 = True
            else:
                self.espelhado1 = False
                if self.controls.is_active("esquerda1"):
                    defending1 = True
        
        if not self.p2.occupied():
            if self.p2.x > self.p1.x:
                self.espelhado2 = True
                if self.controls.is_active("direita2"):
                    defending2 = True
            else:
                self.espelhado2 = False
                if self.controls.is_active("esquerda2"):
                    defending2 = True
        
            
        
        
        col1 = self.p1.update(self.janela, self.buffers[0], self.chao, self.objetos, self.camera)
        col2 = self.p2.update(self.janela, self.buffers[1], self.chao, self.objetos, self.camera)
        
        if col1 == "ENDER":
            self.p1.winningState()
            self.p2.losingState()
            return
        
        if col2 == "ENDER":
            self.p2.winningState()
            self.p1.losingState()
            return
        
        if col1 == "FIM" and col2 == "FIM":
            print("EMPATE!")
            self.ending = 1
            return
        
        if col1 == "FIM":
            print("P2 GANHOU!")
            self.ending = 1
            self.vencedor = 2
            return
        
        if col2 == "FIM":
            print("P1 GANHOU!")
            self.ending = 1
            self.vencedor = 1
            return
        
        colI1 = []
        for i in self.p1.illusions:
            colI1.append(i.update(self.janela, None, self.chao, None, self.camera))
                        
                
        for i in range(len(self.p1.illusions)):
            if not self.p1.illusions[i].hit(self.checkCollision(col2, colI1[i], self.espelhado2), False):
                self.p1.deleteI(i)
                break
                    #if not (self.p1.illusions[i].x+self.p1.illusions[i].collision["low"][2]<self.chao.x+self.chao.width and self.p1.illusions[i].x+self.p1.illusions[i].collision["low"][2]+self.p1.illusions[i].collision["low"][0]>self.chao.x):
                       # self.p1.deleteI(i)
                       # break
            
        colI2 = []
        for i in self.p2.illusions:
            colI2.append(i.update(self.janela, None, self.chao, None, self.camera))
                        
        for i in range(len(self.p2.illusions)):
            if not self.p2.illusions[i].hit(self.checkCollision(col1, colI2[i], self.espelhado2), False):
                self.p2.deleteI(i)
                break
                            #if not (self.p1.illusions[i].x+self.p1.illusions[i].collision["low"][2]<self.chao.x+self.chao.width and self.p1.illusions[i].x+self.p1.illusions[i].collision["low"][2]+self.p1.illusions[i].collision["low"][0]>self.chao.x):
                             #   self.p1.deleteI(i)
                              #  break
                
        
        for object in self.objetos:
            object.update(self.janela, self.chao)
        
        
        hit2 = self.checkCollision(col1, col2, self.espelhado1)
        hit1 = self.checkCollision(col2, col1, self.espelhado2)
        
        if hit2 and hit2[0] == "high":
            self.sameHit2 += 1
        if self.sameHit2 > 0:
            self.hitCounter2 += self.janela.delta_time()
            if self.hitCounter2 > 2:
                self.hitCounter2 = 0
                self.sameHit2 = 0
        if hit1 and hit1[0] == "high":
            self.sameHit1 += 1
        if self.sameHit1 > 0:
            self.hitCounter1 += self.janela.delta_time()
            if self.hitCounter1 > 2:
                self.hitCounter1 = 0
                self.sameHit1 = 0
        print(self.sameHit1>1)
        objectable1 = False
        objectable2 = False
        if self.p1.name == "mimico":
            objectable1 = self.p2.y+self.p2.collision["low"][3]+self.p2.collision["low"][1] < self.p1.y+self.p1.collision["low"][3]
        else:
            objectable1 = self.sameHit1 > 40
            self.sameHit = 0
        
        if self.p2.name == "mimico":
            objectable2 = self.p1.y+self.p1.collision["low"][3]+self.p1.collision["low"][1] < self.p2.y+self.p2.collision["low"][3]
        else:
            objectable2 = self.sameHit2 > 40
            self.sameHit = 0
            
        bat1 = self.p1.currentState == 4 and self.p1.name == "mimico"
        bat2 = self.p2.currentState == 4 and self.p2.name == "mimico"
        #if len(col1)>2 and len(col1[2])>4:
         #   bat1 = True
        #if len(col2)>2 and len(col2[2])>4:
         #   bat2 = True

        self.p2.hit(hit2, defending2, objectable2, bat1)
        self.p1.hit(hit1, defending1, objectable1, bat2)
        
        self.vida1.set_value(self.p1.get_vida())
        self.vida2.set_value(self.p2.get_vida())
        
        if self.vida1.valor_atual <= 0 or self.vida2.valor_atual <= 0:
            if self.vida1.valor_atual == 0 and self.vida2.valor_atual == 0:
                self.p1.losingState()
                self.p2.losingState()
            elif self.vida1.valor_atual == 0:
                self.p2.winningState()
                self.p1.losingState()
                return
            else:
                self.p1.winningState()
                self.p2.losingState()
                return
            
        if not (self.p1.x+self.p1.collision["low"][2]<self.chao.x+self.chao.width and self.p1.x+self.p1.collision["low"][2]+self.p1.collision["low"][0]>self.chao.x):
            if self.p1.y+self.p1.collision["low"][3]+self.p1.collision["low"][1]>self.chao.y:
                self.p2.winningState()
                self.p1.losingState()
                return 
        if not (self.p2.x+self.p2.collision["low"][2]<self.chao.x+self.chao.width and self.p2.x+self.p2.collision["low"][2]+self.p2.collision["low"][0]>self.chao.x):
                    if self.p2.y+self.p2.collision["low"][3]+self.p2.collision["low"][1]>self.chao.y:
                        self.p1.winningState()
                        self.p2.losingState()
                        return 
                
        
        if self.teclado.key_pressed("ESC"):
            SceneManager.change_scene(Menu(0, self.controls))

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
        
        if self.ending > 0:
            if self.vencedor > 0:
                self.janela.draw_text(f"Jogador {self.vencedor} venceu!", 200, 120, tamanho=60, cor="red", fonte = "Pixel")
            else:
                self.janela.draw_text(f"Empate!", 180, 120, tamanho=60, cor="red", fonte = "Pixel")
        #self.astro.draw()
        if self.beggining < 4:
            if self.beggining < 3:
                self.janela.draw_text("Preparar...", 310, 120, tamanho=60, cor="green", fonte = "Pixel")
            else:
                self.janela.draw_text("Vai!!!", 350, 120, tamanho=60, cor="green", fonte = "Pixel")
        

class Opcao(Scene):
    transp = 0
    mover = []
    def __init__(self, controls):
            self.controls = controls
            self.fundo = GameImage("recursos/fundo.png")
            super().__init__()
            self.preto = GameImage("recursos/prato.png")
            self.logo = GameImage("recursos/logo.png")
            self.logo.set_position(30, 50)
            self.config = GameImage("recursos/config2.png")
            self.config.set_position(self.janela.width/2-self.config.width/2, 100)
            self.button = Button(None, "recursos/button3.png", self.janela.width/2+50, 270)
            self.mover.append(Mover("recursos/mover.png", 361, 131))
            self.mover.append(Mover("recursos/mover.png", 361, 175))
            self.mover.append(Mover("recursos/mover.png", 361, 206))
    
    def loop(self):
        if self.teclado.key_pressed("ESC"):
            SceneManager.change_scene(Menu(self.transp, self.controls))
        if self.transp < 155:
            self.transp +=2
        if self.button.update():
             SceneManager.change_scene(Menu(self.transp, self.controls))
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
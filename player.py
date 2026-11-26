from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import time, random
from object import Object
from PPlay.particles import ParticleEmitter

IDLE = 0
WALK = 1
CROUCH = 2
JUMP = 3
POWER = 4
CWALK = 5
WP = 6
WWP = 7
UWP = 8
DWP = 9
MP = 10
WK = 11
MK = 12
CATCH = 13
HA = 14
HB = 15
DF = 16
DESTROYING = 17
WIN = 18
LOSE = 19

class Player(Sprite):
    
    def __init__(self, x, y, controle, caminho_imagem, total_frames, linhas, type):
        super().__init__(caminho_imagem, total_frames, linhas=linhas)
        self.set_position(x,y)
        self.frame_atual = 0
        self.controle = {}
        if controle:
            self.controle = {
            "cima": controle[0],
            "baixo": controle[1],
            "esquerda": controle[2],
            "direita": controle[3]
        }
        
        self.states = {
            IDLE: (None,0, None),
            WALK: (None,0, None),
            #CROUCH: {None,0},
            JUMP: (None,0, None),
            POWER: (None,0, None),
            #CWALK: {None,0},
            WP:(None,0, None),
            WWP:(None,0, None),
            UWP:(None,0, None),
            DWP:(None,0, None),
            MP:(None,0, None),
            WK:(None,0, None),
            MK:(None,0, None),
            CATCH:(None,0, None),   
            DESTROYING:(None,0, None),   
            HA:(None,0, None),
            HB:(None,0, None),
            DF:(None, 0, None),
            WIN:(None, 0, None),
            LOSE: (None, 0, None)
        }
        self.collision = {
            "high": None,
            "low": None
        }
        
        self.vida = 100
        self.vx = 0
        self.vy = 0
        self.teclado = Keyboard()
        self.g = 1200
        self.jump = -400
        self.ground = False
        self.currentState = IDLE
        self.fila = []
        self.impact_start = None
        self.impact_duration = 0.3
        self.frameLimit = 0.1
        self.frameCount = 0
        #self.set_loop()
        self.hit_dur = 0.4
        self.power_dur = 4
        self.hit_count = 0
        
        self.gatilhoCounter = 0
        self.gatilhoDisparo = 0.2
        self.type = type
        self.illusions = []
        self.puff = ParticleEmitter(0,0)
        self.puff.cor = (255, 255, 255)
        self.puff.vida_base = 4
        self.puff.intensidade = 10
        self.puff.spread_x = 60
        self.puff.spread_y = 60
        
        self.pulando = False
        self.andandoEsq = True
        self.andandoDir = False
        
        self.objects = []
        self.available = True
        
        self.var = 0
        
        self.cr = {
            WP: ["cima+wp", "baixo+wp", "wp", "mp"],
            WWP: [],
            UWP: [],
            DWP: [],
            MP: ["mk"],
            WK: ["wp", "mp", "mk"],
            MK: [],
            CATCH: [],
            POWER: []
        }
    
    def get_vida(self):
        return self.vida
    
    def getLastInputTime(self, inputs, target):

        for item in reversed(inputs):
            if item["input"] == target:
                return item["time"]

        return None
    
    def getCommand(self, buffer, maxGap=0.12):

        if not buffer:
            return None
        
        inputs = buffer.get_inputs()
        

        if not inputs:
            return None

        latest = inputs[-1]

        combinations = {
            "wp": ["cima", "baixo"],
            "mp": ["cima"]
        }

        # Check combinations
        if latest["input"] in combinations:

            for item in reversed(inputs[:-1]):

                if item["input"] in combinations[latest["input"]]:

                    gap = latest["time"] - item["time"]

                    if 0 <= gap <= maxGap:
                        command = f'{item["input"].lower()}+{latest["input"]}'
                        buffer.clear()
                        return command

                    break

        # Check individual buttons
        if latest["input"] in ["wp", "mp", "wk", "mk", "pw"]:
            buffer.clear()
            return latest["input"]

        return None
     
    def hit(self, mode, defense=False):
        if mode:
            print("ioiho")
            if self.type == "player":
                for i in range(len(self.illusions)):
                    self.deleteI(0)
            else:
                return False
            if defense or self.currentState == DF:
                self.currentState = DF 
            else:
                if self.currentState != HA and self.currentState != HB:
                    self.vida -= mode[1]
                    print(self.objects)
                    if self.objects and self.objects[0].portador == self:
                        self.objects[0].descolar(self.x, self.y)
                        self.objects.pop(0)
                if mode[0] == "high":
                    self.currentState = HA
                else:
                    self.currentState = HB   
            self.states[self.currentState][self.var].set_position(self.x, self.y)
        return True
            
    def occupied(self):
        if self.currentState in [WALK, JUMP, IDLE]:
            return False
        return True
    
    def activate(self):
        pass
    
    def deleteI(self, i):
        self.puff.set_pos(self.illusions[i].x + self.illusions[i].width/2, self.illusions[i].y + self.illusions[i].height/2)
        self.puff.emitir()
        self.illusions.pop(i)
    
    def winningState(self):
        self.currentState = WIN
        self.states[self.currentState][self.var].set_position(self.x, self.y)
    
    def losingState(self):
        self.currentState = LOSE
        self.states[self.currentState][self.var].set_position(self.x, self.y)
        
    def update(self, janela, buffer, chao, objetos, cam):
        super().update()
        
        self.puff.update()
        
        buffer_duration = 0.4
        current_time = time.perf_counter()

        self.fila = [
            item for item in self.fila
            if current_time - item["time"] <= buffer_duration
        ]
        
        colInfo = [(self.x, self.y), self.collision]
        
        self.var = 3
        if self.objects:
            for object in self.objects:
                if object.pai == self:
                    self.var = 0
                    break
        
        if self.type == "player":
            self.pulando = self.teclado.key_pressed(self.controle["cima"])
            self.andandoEsq = self.teclado.key_pressed(self.controle["esquerda"])
            self.andandoDir = self.teclado.key_pressed(self.controle["direita"])
        else:
            self.pulando = True    
            self.gatilhoCounter += janela.delta_time()
            if self.gatilhoCounter > random.randint(2,4):
                self.gatilhoCounter = 0
                if self.andandoEsq:
                    self.andandoEsq = False
                    self.andandoDir = True
                else:
                    self.andandoEsq = True
                    self.andandoDir = False
            if cam.transform_x(self.x)<0:
                self.x = 0
                self.andandoEsq = False
                self.andandoDir = True
            elif cam.transform_x(self.x)>cam.largura-self.states[self.currentState][0].width:
                self.x = janela.width-self.states[self.currentState][0].width
                self.andandoEsq = True
                self.andandoDir = False 
        
        if self.currentState in [HA, HB, DF, POWER]:
            dur = self.hit_dur
            if self.currentState == POWER: 
                dur = self.power_dur
                if self.hit_count >= self.power_dur / 2:
                    self.gatilhoCounter += janela.delta_time()
                    if self.gatilhoCounter >= self.gatilhoDisparo:
                        self.activate()
                        self.gatilhoCounter = 0
                else:
                    self.gatilhoCounter = 0
            if self.hit_count < dur:
                self.states[self.currentState][self.var].set_position(self.x, self.y)
                self.states[self.currentState][self.var].set_curr_frame(0)
                colInfo.append(None)
                self.hit_count+=janela.delta_time()
                return colInfo
            else:
                self.currentState = IDLE
                self.states[self.currentState][self.var].set_curr_frame(0)
                if buffer: buffer.clear()
                self.hit_count = 0
        
        if self.currentState == IDLE or self.currentState == WALK or self.currentState == JUMP:
            if self.andandoEsq or self.andandoDir:
                if self.andandoDir:
                    self.vx = 400
                if self.andandoEsq: 
                    self.vx = -400
                if self.currentState != JUMP:
                    self.currentState = WALK
            elif self.ground == True:
                self.vx = 0
                self.currentState = IDLE
            if self.pulando and self.ground == True:
                self.vy = self.jump
                self.currentState = JUMP
        elif self.ground == True:
            self.vx = 0
        
        self.x += self.vx * janela.delta_time()
        telaX = cam.transform_x(self.x)
        if telaX < 0:
            self.x = cam.x
        elif telaX + self.states[self.currentState][0].width  > cam.largura:
            self.x = cam.x + cam.largura - self.states[self.currentState][0].width   
             
        self.y += self.vy * janela.delta_time()  
        if self.y+self.collision["low"][3]+self.collision["low"][1]>chao.y and self.x+self.collision["low"][2]<chao.x+chao.width and self.x+self.collision["low"][2]+self.collision["low"][0]>chao.x:
            self.y = chao.y-self.collision["low"][1]-self.collision["low"][3]
            self.vy = 0
            self.ground = True
            if self.currentState == JUMP and not self.pulando:
                self.currentState = IDLE
        else:
            self.vy += self.g * janela.delta_time()
            self.ground = False
        
        command = self.getCommand(buffer)
        
        if command and len(self.fila) < 3:
            self.fila.append({
                "command": command,
                "time": time.perf_counter()
            })
        
        sprite, impact_frame, collision, other = self.states[self.currentState]

        frame = self.states[self.currentState][self.var].get_curr_frame()
        last_frame = self.states[self.currentState][self.var].total_frames-1

        if impact_frame is not None and frame == impact_frame:
                        
            if self.currentState == DESTROYING:
                return "ENDER"
            
            if self.currentState == LOSE:
                return "FIM"
            
            colInfo.append(collision)

            if self.impact_start is None:
                self.impact_start = time.perf_counter()
                
            if self.currentState == CATCH and self.available == True:
                for objeto in objetos:
                    referee = objeto.acoplar(self.states[self.currentState][self.var], self)
                    if referee:
                        self.objects.insert(0, referee)
                        self.available = False
                        break

            if time.perf_counter() - self.impact_start >= self.impact_duration:
                self.impact_start = None
                self.available = True
                self.states[self.currentState][self.var].set_curr_frame(frame+1)
                #print("Before/after:", frame, sprite.get_curr_frame())
                
                if self.fila and self.fila[0]["command"] in self.cr[self.currentState]:
                    command = self.fila.pop(0)["command"]
                    
                    if self.currentState == WP:
                        if command == "wp":
                            self.currentState = WWP
                        elif command == "cima+wp":
                            self.currentState = UWP
                        elif command == "baixo+wp":
                            self.currentState = DWP
                        else:
                            self.currentState = MP
                    
                    elif self.currentState == MP:
                        self.currentState = MK
                    
                    elif self.currentState == WK:
                        if command == "wp":
                            self.currentState = WP
                        elif command == "mp":
                            self.currentState = MP
                        elif command == "mk":
                            self.currentState = MK
                    self.states[self.currentState][self.var].set_curr_frame(0)
                    
                    
        elif frame == last_frame or self.currentState in [WALK, JUMP, IDLE]:
            if self.fila:
                command = self.fila.pop(0)["command"]

                if command == "wp":
                    self.currentState = WP
                elif command == "mp":
                    self.currentState = MP
                elif command == "wk":
                    self.currentState = WK
                elif command == "mk":
                    self.currentState = MK
                elif command == "baixo+wp":
                    self.currentState = CATCH
                elif command == "cima+mp":
                    can_destroy = False
                    for object in self.objects:
                        if object.pai != object.portador:
                            can_destroy = True
                    if can_destroy: self.currentState = DESTROYING
                elif command == "pw" and (not self.illusions) and self.currentState!=POWER:
                    self.currentState = POWER
                    print("Ativo")
                
                self.states[self.currentState][self.var].set_curr_frame(0)
                
            elif self.currentState == WALK or self.currentState == JUMP:
                self.frameCount += janela.delta_time()
                if self.frameCount >= self.frameLimit:
                    self.frameCount -= self.frameLimit
                    self.states[self.currentState][self.var].set_curr_frame((frame + 1) % self.states[self.currentState][self.var].total_frames)
            else:
                self.currentState = IDLE
                self.states[self.currentState][0].set_curr_frame(0)
                                
        else:
            self.frameCount += janela.delta_time()
            if self.frameCount >= self.frameLimit:
                self.frameCount -= self.frameLimit
                self.states[self.currentState][self.var].set_curr_frame((frame + 1) % self.states[self.currentState][self.var].total_frames)
        
        
        self.states[self.currentState][self.var].set_position(self.x, self.y)
        #if not input in self.combos and len(input)>3:
         #   input = input[-2:]
        #janela.draw_text(command, 0, 0, tamanho=20, color=(255, 0, 0))
        
        
        return colInfo
    
    
    def draw(self, espelhado, objetos):
        #self.states[self.currentState][0].set_position(self.x, self.y)
        self.states[self.currentState][self.var].espelhado = espelhado
        self.states[self.currentState][self.var].draw()
        
        if self.illusions:
            for i in self.illusions:
                i.draw(espelhado, None)
        
        self.puff.draw()
    

class Volpina(Player):
    
    name = "volpina"
    
    def __init__(self, x, y, controle, objeto, type="player", caminho_imagem="recursos/volpina/idle.png", total_frames=16, linhas=1):
        super().__init__(x, y, controle, caminho_imagem, total_frames, linhas, type)
        if objeto:
            objeto.set_position(x,y)
            self.objects = [objeto]
        self.cr = {
                    WP: ["cima+wp", "baixo+wp", "wp", "mp"],
                    WWP: [],
                    UWP: [],
                    DWP: [],
                    MP: ["mk"],
                    WK: ["wp", "mp", "mk"],
                    MK: [],
                    CATCH: [],
                    POWER: []
                }
        self.states = {
                    WIN: (Sprite("recursos/volpina/idle.png", 1), None, None, Sprite("recursos/volpina/idle (2).png", 1)),
                    IDLE: (Sprite("recursos/volpina/idle.png", 1), None, None, Sprite("recursos/volpina/idle (2).png", 1)),
                    WALK: (Sprite("recursos/volpina/walk.png", 12), None, None, Sprite("recursos/volpina/walk (2).png", 12)),
                    #CROUCH: {Sprite("recursos/jogador/volpina_crouch.png", 4), 0},
                    JUMP: (Sprite("recursos/volpina/jump.png", 1), None, None, Sprite("recursos/volpina/jump (2).png", 1)),
                    POWER: (Sprite("recursos/volpina/pw.png", 1), 0, None, Sprite("recursos/volpina/pw (2).png", 1)),
                    #CWALK: {Sprite("recursos/jogador/volpina_crouchWalk.png", 10), 0},
                    #WP: (Sprite("recursos/jogador/wp.png", 5, False), 2, (12, 12, 116, 94, 20)),
                    #WWP: (Sprite("recursos/jogador/wwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #UWP: (Sprite("recursos/jogador/uwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #DWP: (Sprite("recursos/jogador/dwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #MP: (Sprite("recursos/jogador/mp.png", 3, False), 1, (0,0,0,0, 20)),
                    #WK: (Sprite("recursos/jogador/wk.png", 5, False), 2, (0,0,0,0, 20)),
                    #MK: (Sprite("recursos/jogador/mk.png", 5, False), 2, (0,0,0,0, 20)),
                    WP:  (Sprite("recursos/volpina/wp.png", 6, False),
     2, (32, 18, 90, 94, 2), Sprite("recursos/volpina/wp (2).png", 6, False)),

WWP: (Sprite("recursos/volpina/wwp.png", 4, False),
     0, (44, 16, 84, 80, 2), Sprite("recursos/volpina/wwp (2).png", 4, False)),

UWP: (Sprite("recursos/volpina/uwp.png", 4, False),
     0, (40, 28, 88, 50, 2), Sprite("recursos/volpina/uwp (2).png", 4, False)),

DWP: (Sprite("recursos/volpina/dwp.png", 4, False),
     0, (30, 28, 94, 92, 2), Sprite("recursos/volpina/dwp (2).png", 4, False)),

MP:  (Sprite("recursos/volpina/mp.png", 4, False),
     1, (32, 42, 92, 52, 4), Sprite("recursos/volpina/mp (2).png", 4, False)),

WK:  (Sprite("recursos/volpina/wk.png", 6, False),
     2, (52, 28, 76, 84, 2), Sprite("recursos/volpina/wk (2).png", 6, False)),

MK:  (Sprite("recursos/volpina/mk.png", 7, False),
     3, (36, 40, 80, 48, 4), Sprite("recursos/volpina/mk (2).png", 7, False)),
                    CATCH: (Sprite("recursos/volpina/catch.png", 6, False), 2, None, Sprite("recursos/volpina/catch (2).png", 6, False)),
                    DESTROYING: (Sprite("recursos/volpina/destroy.png", 10, False), 9, None, Sprite("recursos/volpina/destroy (2).png", 10, False)),
                    HA: (Sprite("recursos/volpina/ha.png", 1, False), 0, None, Sprite("recursos/volpina/ha (2).png", 1, False)),
                    HB: (Sprite("recursos/volpina/hb.png", 1, False), 0, None, Sprite("recursos/volpina/hb (2).png", 1, False)),
                    DF: (Sprite("recursos/volpina/df.png", 1, False), 0, None, Sprite("recursos/volpina/df (2).png", 1, False)),
                    LOSE: (Sprite("recursos/volpina/fall.png", 9), 8, None, Sprite("recursos/volpina/fall (2).png", 9)),
                }
        
        self.collision = {
            "high": (68, 35, 29, 39),
            "low":  (68, 35, 29, 74)
        }
        
        self.set_position(self.x, self.y-self.collision["low"][3]-self.collision["low"][1])
        self.states[self.currentState][0].set_position(self.x, self.y)
    
    def activate(self):
            self.illusions.append(Volpina(self.x, self.y, None, None, "cpu"))



class Mimico(Player):
    
    name = "mimico"
    
    def __init__(self, x, y, controle, objeto, type="player", caminho_imagem="recursos/mimico/idle.png", total_frames=16, linhas=1):
        super().__init__(x, y, controle, caminho_imagem, total_frames, linhas, type)
        objeto.set_position(x,y)
        self.objects = [objeto]
        self.cr = {
                    WP: ["mp"],
                    WWP: [],
                    UWP: [],
                    DWP: [],
                    MP: [],
                    WK: [],
                    MK: [],
                    CATCH: [],
                    POWER: []
                }
        self.states = {
                    WIN: (Sprite("recursos/mimico/idle.png", 1), None, None, Sprite("recursos/mimico/idle (2).png", 1)),
                    IDLE: (Sprite("recursos/mimico/idle.png", 1), None, None, Sprite("recursos/mimico/idle (2).png", 1)),
                    WALK: (Sprite("recursos/mimico/walk.png", 12), None, None, Sprite("recursos/mimico/walk (2).png", 12)),
                    #CROUCH: {Sprite("recursos/jogador/volpina_crouch.png", 4), 0},
                    JUMP: (Sprite("recursos/mimico/jump.png", 1), None, None, Sprite("recursos/mimico/jump (2).png", 1)),
                    POWER: (Sprite("recursos/mimico/idleP.png", 1), None, None, Sprite("recursos/mimico/idleP (2).png", 1)),
                    #CWALK: {Sprite("recursos/jogador/volpina_crouchWalk.png", 10), 0},
                    #WP: (Sprite("recursos/jogador/wp.png", 5, False), 2, (12, 12, 116, 94, 20)),
                    #WWP: (Sprite("recursos/jogador/wwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #UWP: (Sprite("recursos/jogador/uwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #DWP: (Sprite("recursos/jogador/dwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #MP: (Sprite("recursos/jogador/mp.png", 3, False), 1, (0,0,0,0, 20)),
                    #WK: (Sprite("recursos/jogador/wk.png", 5, False), 2, (0,0,0,0, 20)),
                    #MK: (Sprite("recursos/jogador/mk.png", 5, False), 2, (0,0,0,0, 20)),
                    WP:  (Sprite("recursos/mimico/wp.png", 6, False),
     2, (88, 52, 40, 48, 2), Sprite("recursos/mimico/wp (2).png", 6, False)),

MP:  (Sprite("recursos/mimico/mp.png", 4, False),
     1, (92, 48, 36, 44, 4), Sprite("recursos/mimico/mp (2).png", 4, False)),

WK:  (Sprite("recursos/mimico/wk.png", 4, False),
     1, (88, 48, 40, 68, 2), Sprite("recursos/mimico/wk (2).png", 4, False)),

MK:  (Sprite("recursos/mimico/mk.png", 4, False),
     1, (48, 40, 72, 68, 40), Sprite("recursos/mimico/mk (2).png", 4, False)),
                    CATCH: (Sprite("recursos/mimico/catch.png", 6, False), 2, None, Sprite("recursos/mimico/catch (2).png", 6, False)),
                    DESTROYING: (Sprite("recursos/mimico/destroy.png", 10, False), 9, None, Sprite("recursos/mimico/destroy (2).png", 10, False)),
                    HA: (Sprite("recursos/mimico/ha.png", 1, False), 0, None, Sprite("recursos/mimico/ha (2).png", 1, False)),
                    HB: (Sprite("recursos/mimico/hb.png", 1, False), 0, None, Sprite("recursos/mimico/hb (2).png", 1, False)),
                    DF: (Sprite("recursos/mimico/df.png", 1, False), 0, None, Sprite("recursos/mimico/df (2).png", 1, False)),
                    LOSE: (Sprite("recursos/mimico/fall.png", 6), 5, None, Sprite("recursos/mimico/fall (2).png", 6))
                }
        
        self.collision = {
            "high": (68, 35, 29, 39),
            "low":  (68, 35, 29, 74)
        }
        
        self.set_position(self.x, self.y-self.collision["low"][3]-self.collision["low"][1])
        self.states[self.currentState][0].set_position(self.x, self.y)
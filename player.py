from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import time
from object import Object

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

class Player(Sprite):
    
    def __init__(self, x, y, controle, caminho_imagem, total_frames, linhas):
        super().__init__(caminho_imagem, total_frames, linhas=linhas)
        self.set_position(x,y)
        self.frame_atual = 0
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
            DF:(None, 0, None)
        }
        self.collision = {
            "high": None,
            "low": None
        }
        
        self.vida = 100
        self.vx = 0
        self.vy = 0
        self.teclado = Keyboard()
        self.g = 20
        self.jump = -400
        self.ground = False
        self.currentState = IDLE
        self.fila = []
        self.impact_start = None
        self.impact_duration = 0.3
        self.frameLimit = 0.08
        self.frameCount = 0
        #self.set_loop()
        self.hit_dur = 0.4
        self.hit_count = 0
        
        self.objects = []
        
        
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
            self.states[self.currentState][0].set_position(self.x, self.y)
            
    def occupied(self):
        if self.currentState in [WALK, JUMP, IDLE]:
            return False
        return True
        
    def update(self, janela, buffer, chao, objetos):
        super().update()    
        
        buffer_duration = 0.4
        current_time = time.perf_counter()

        self.fila = [
            item for item in self.fila
            if current_time - item["time"] <= buffer_duration
        ]
        
        colInfo = [(self.x, self.y), self.collision]
        
        if self.currentState in [HA, HB, DF]:
            
            if self.hit_count < self.hit_dur:
                self.states[self.currentState][0].set_position(self.x, self.y)
                self.states[self.currentState][0].set_curr_frame(0)
                colInfo.append(None)
                self.hit_count+=janela.delta_time()
                return colInfo
            else:
                self.currentState = IDLE
                self.states[self.currentState][0].set_curr_frame(0)
                buffer.clear()
                self.hit_count = 0
        
        if self.currentState == IDLE or self.currentState == WALK or self.currentState == JUMP:
            if self.teclado.key_pressed(self.controle["esquerda"]) or self.teclado.key_pressed(self.controle["direita"]):
                if self.teclado.key_pressed(self.controle["direita"]):
                    self.vx = 400
                if self.teclado.key_pressed(self.controle["esquerda"]): 
                    self.vx = -400
                if self.currentState != JUMP:
                    self.currentState = WALK
            elif self.ground == True:
                self.vx = 0
                self.currentState = IDLE
            if self.teclado.key_pressed(self.controle["cima"]) and self.ground == True:
                self.vy = self.jump
                self.currentState = JUMP
        elif self.ground == True:
            self.vx = 0
        
        self.x += self.vx * janela.delta_time()  
        self.y += self.vy * janela.delta_time()  
        if self.y > chao.y-116:
            self.y = chao.y-116
            self.vy = 0
            self.ground = True
            if self.currentState == JUMP and not self.teclado.key_pressed("UP"):
                self.currentState = IDLE
        else:
            self.vy += self.g
            self.ground = False
        
        command = self.getCommand(buffer)
        
        if command and len(self.fila) < 3:
            self.fila.append({
                "command": command,
                "time": time.perf_counter()
            })
        
        sprite, impact_frame, collision = self.states[self.currentState]

        frame = sprite.get_curr_frame()
        last_frame = sprite.total_frames-1

        if impact_frame is not None and frame == impact_frame:
            
            if self.currentState == CATCH:
                for objeto in objetos:
                    referee = objeto.acoplar(sprite, self)
                    if referee:
                        self.objects.insert(0, referee)
                        
            if self.currentState == DESTROYING:
                return "FIM"
            
            colInfo.append(collision)

            if self.impact_start is None:
                self.impact_start = time.perf_counter()

            if time.perf_counter() - self.impact_start >= self.impact_duration:
                self.impact_start = None
                sprite.set_curr_frame(frame+1)
                print("Before/after:", frame, sprite.get_curr_frame())
                
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
                    self.states[self.currentState][0].set_curr_frame(0)
                    
                    
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
                elif command == "pw":
                    self.currentState = POWER
                
                self.states[self.currentState][0].set_curr_frame(0)
                
            elif self.currentState == WALK or self.currentState == JUMP:
                self.frameCount += janela.delta_time()
                if self.frameCount >= self.frameLimit:
                    self.frameCount -= self.frameLimit
                    sprite.set_curr_frame((frame + 1) % sprite.total_frames)
            else:
                self.currentState = IDLE
                self.states[self.currentState][0].set_curr_frame(0)
                                
        else:
            self.frameCount += janela.delta_time()
            if self.frameCount >= self.frameLimit:
                self.frameCount -= self.frameLimit
                sprite.set_curr_frame((frame + 1) % sprite.total_frames)
        
        
        self.states[self.currentState][0].set_position(self.x, self.y)
        #if not input in self.combos and len(input)>3:
         #   input = input[-2:]
        #janela.draw_text(command, 0, 0, tamanho=20, color=(255, 0, 0))
        
        
        return colInfo
    
    
    def draw(self, espelhado, objetos):
        #self.states[self.currentState][0].set_position(self.x, self.y)
        self.states[self.currentState][0].espelhado = espelhado
        self.states[self.currentState][0].draw()
    

class Volpina(Player):
    
    def __init__(self, x, y, controle, objeto, caminho_imagem="recursos/ryu_anim/seq (27).png", total_frames=16, linhas=1):
        super().__init__(x, y, controle, caminho_imagem, total_frames, linhas)
        objeto.set_position(x,y)
        self.objects = [objeto]
        self.states = {
                    IDLE: (Sprite("recursos/jogador/idle.png", 1), None, None),
                    WALK: (Sprite("recursos/jogador/volpina_walk.png", 12), None, None),
                    #CROUCH: {Sprite("recursos/jogador/volpina_crouch.png", 4), 0},
                    JUMP: (Sprite("recursos/jogador/volpina_jump.png", 1), None, None),
                    POWER: (Sprite("recursos/jogador/volpina_power.png", 1), None, None),
                    #CWALK: {Sprite("recursos/jogador/volpina_crouchWalk.png", 10), 0},
                    #WP: (Sprite("recursos/jogador/wp.png", 5, False), 2, (12, 12, 116, 94, 20)),
                    #WWP: (Sprite("recursos/jogador/wwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #UWP: (Sprite("recursos/jogador/uwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #DWP: (Sprite("recursos/jogador/dwp.png", 4, False), 0, (0,0,0,0, 20)),
                    #MP: (Sprite("recursos/jogador/mp.png", 3, False), 1, (0,0,0,0, 20)),
                    #WK: (Sprite("recursos/jogador/wk.png", 5, False), 2, (0,0,0,0, 20)),
                    #MK: (Sprite("recursos/jogador/mk.png", 5, False), 2, (0,0,0,0, 20)),
                    WP:  (Sprite("recursos/jogador/wp.png", 5, False),
     2, (32, 18, 90, 94, 2)),

WWP: (Sprite("recursos/jogador/wwp.png", 4, False),
     0, (44, 16, 84, 80, 2)),

UWP: (Sprite("recursos/jogador/uwp.png", 4, False),
     0, (40, 28, 88, 50, 2)),

DWP: (Sprite("recursos/jogador/dwp.png", 4, False),
     0, (30, 28, 94, 92, 2)),

MP:  (Sprite("recursos/jogador/mp.png", 3, False),
     1, (32, 42, 92, 52, 4)),

WK:  (Sprite("recursos/jogador/wk.png", 5, False),
     2, (52, 28, 76, 84, 2)),

MK:  (Sprite("recursos/jogador/mk.png", 5, False),
     2, (36, 40, 80, 48, 4)),
                    CATCH: (Sprite("recursos/jogador/catch.png", 5, False), 2, None),
                    DESTROYING: (Sprite("recursos/jogador/destroy.png", 8, False), 7, None),
                    HA: (Sprite("recursos/jogador/ha.png", 1, False), 0, None),
                    HB: (Sprite("recursos/jogador/hb.png", 1, False), 0, None),
                    DF: (Sprite("recursos/jogador/button1.png", 1, False), 0, None)
                }
        
        self.collision = {
            "high": (68, 35, 29, 39),
            "low":  (68, 35, 29, 74)
        }
        self.states[self.currentState][0].set_position(self.x, self.y)
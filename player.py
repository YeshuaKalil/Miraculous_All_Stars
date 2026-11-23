from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard
import time

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

class Player(Sprite):
    
    def __init__(self, x, y, caminho_imagem, total_frames, linhas):
        super().__init__(caminho_imagem, total_frames, linhas=linhas)
        self.set_position(x,y)
        self.frame_atual = 0
        
        self.states = {
            IDLE: (None,0),
            WALK: (None,0),
            #CROUCH: {None,0},
            JUMP: (None,0),
            POWER: (None,0),
            #CWALK: {None,0},
            WP:(None,0),
            WWP:(None,0),
            UWP:(None,0),
            DWP:(None,0),
            MP:(None,0),
            WK:(None,0),
            MK:(None,0),
            CATCH:(None,0),   
        }
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
        self.frameLimit = 0.05
        self.frameCount = 0
        #self.set_loop()
        
        self.cr = {
            WP: ["up+w", "down+w", "w", "e"],
            WWP: [],
            UWP: [],
            DWP: [],
            MP: ["d"],
            WK: ["w", "e", "d"],
            MK: [],
            CATCH: [],
            POWER: []
        }
    
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
            "w": ["UP", "DOWN"],
            "e": ["UP"]
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
        if latest["input"] in ["w", "e", "s", "d", "t"]:
            buffer.clear()
            return latest["input"]

        return None
        
        
    def update(self, janela, buffer, chao):
        super().update()
        
        buffer_duration = 0.4
        current_time = time.perf_counter()

        self.fila = [
            item for item in self.fila
            if current_time - item["time"] <= buffer_duration
        ]
        
        if self.currentState == IDLE or self.currentState == WALK or self.currentState == JUMP:
            if self.teclado.key_pressed("LEFT") or self.teclado.key_pressed("RIGHT"):
                if self.teclado.key_pressed("RIGHT"):
                    self.vx = 400
                if self.teclado.key_pressed("LEFT"): 
                    self.vx = -400
                    print("i")
                if self.currentState != JUMP:
                    self.currentState = WALK
            elif self.ground == True:
                self.vx = 0
                self.currentState = IDLE
            if self.teclado.key_pressed("UP") and self.ground == True:
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

        
        sprite, impact_frame = self.states[self.currentState]

        frame = sprite.get_curr_frame()
        last_frame = sprite.total_frames-1

        if impact_frame is not None and frame == impact_frame:

            if self.impact_start is None:
                self.impact_start = time.perf_counter()

            if time.perf_counter() - self.impact_start >= self.impact_duration:
                self.impact_start = None
                sprite.set_curr_frame(frame+1)
                print("Before/after:", frame, sprite.get_curr_frame())
                
                if self.fila and self.fila[0]["command"] in self.cr[self.currentState]:
                    command = self.fila.pop(0)["command"]
                    
                    if self.currentState == WP:
                        if command == "w":
                            self.currentState = WWP
                        elif command == "up+w":
                            self.currentState = UWP
                        elif command == "down+w":
                            self.currentState = DWP
                        else:
                            self.currentState = MP
                    
                    elif self.currentState == MP:
                        self.currentState = MK
                    
                    elif self.currentState == WK:
                        if command == "w":
                            self.currentState = WP
                        elif command == "e":
                            self.currentState = MP
                        elif command == "d":
                            self.currentState = MK
                    self.states[self.currentState][0].set_curr_frame(0)
                    
                    
        elif frame == last_frame or self.currentState in [WALK, JUMP, IDLE]:
            if self.fila:
                command = self.fila.pop(0)["command"]

                if command == "w":
                    self.currentState = WP
                elif command == "e":
                    self.currentState = MP
                elif command == "s":
                    self.currentState = WK
                elif command == "d":
                    self.currentState = MK
                elif command == "t":
                    self.currentState = POWER
                
                self.states[self.currentState][0].set_curr_frame(0)
                
            elif self.currentState == WALK or self.currentState == JUMP:
                print(self.currentState==WALK)
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
        return command
    
    
    def draw(self):
        self.states[self.currentState][0].draw()
    

class Volpina(Player):
    
    def __init__(self, x, y, caminho_imagem="recursos/ryu_anim/seq (27).png", total_frames=16, linhas=1):
        super().__init__(x, y, caminho_imagem, total_frames, linhas)
        self.states = {
                    IDLE: (Sprite("recursos/jogador/idle.png", 1), None),
                    WALK: (Sprite("recursos/jogador/volpina_walk.png", 12), None),
                    #CROUCH: {Sprite("recursos/jogador/volpina_crouch.png", 4), 0},
                    JUMP: (Sprite("recursos/jogador/volpina_jump.png", 1), None),
                    POWER: (Sprite("recursos/jogador/volpina_power.png", 1), None),
                    #CWALK: {Sprite("recursos/jogador/volpina_crouchWalk.png", 10), 0},
                    WP: (Sprite("recursos/jogador/wp.png", 5, False), 2),
                    WWP: (Sprite("recursos/jogador/wwp.png", 4, False), 0),
                    UWP: (Sprite("recursos/jogador/uwp.png", 4, False), 0),
                    DWP: (Sprite("recursos/jogador/dwp.png", 4, False), 0),
                    MP: (Sprite("recursos/jogador/mp.png", 3, False), 1),
                    WK: (Sprite("recursos/jogador/wk.png", 5, False), 2),
                    MK: (Sprite("recursos/jogador/mk.png", 5, False), 2),
                    CATCH: (Sprite("recursos/jogador/catch.png", 5, False), 2)
                }
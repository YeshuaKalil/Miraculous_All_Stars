from PPlay.sprite import Sprite
from PPlay.keyboard import Keyboard


class Jogador(Sprite):

    def __init__(self, x, y, caminho_imagem="recursos/jogador/volpina_walk.png", total_frames=1):
        super().__init__(caminho_imagem, total_frames)
        self.set_position(x,y)
        self.animacoes = {
            "walk": Sprite("recursos/jogador/volpina_walk.png", 12),
            "crouch": Sprite("recursos/jogador/volpina_crouch.png", 4),
            "jump": Sprite("recursos/jogador/volpina_jump.png", 1),
            "power": Sprite("recursos/jogador/volpina_power.png", 1),
            "crouchWalk": Sprite("recursos/jogador/volpina_crouchWalk.png", 10)
        }
        self.sprite = self.animacoes["walk"]
        self.estado = "walk"
        self.vx = 200
        self.vy = 100
        self.JUMP = 800
        self.a = 30
        self.teclado = Keyboard()
        self.chao = False
        self.powerUse = False
        self.counter = 0
        self.key = ""


    def trocar_animacao(self, estado):
        if estado == self.estado:
            return
        self.estado = estado
        self.sprite = self.animacoes[estado]

    def update(self, janela, chao):

        if self.teclado.key_pressed("U"):
            self.powerUse = True
            self.trocar_animacao("power")
        self.y += self.vy*janela.delta_time()
        if not self.powerUse:
            if self.chao and self.teclado.key_pressed("UP"):
                    self.vy -= self.JUMP
                    self.chao = False
            if self.teclado.key_pressed("DOWN"):
                if self.teclado.key_pressed("LEFT") or self.teclado.key_pressed("RIGHT"):
                    self.trocar_animacao("crouchWalk")
                    self.sprite.set_total_duration(800)
                    self.sprite.play()
                    if self.teclado.key_pressed("LEFT"):
                        self.x -= self.vx*janela.delta_time()  
                    else: self.x += self.vx*janela.delta_time()
                else:
                    if self.estado != "crouch":
                        self.trocar_animacao("crouch")
                        self.sprite.stop()
                    self.trocar_animacao("crouch")
                    self.sprite.set_total_duration(200)
                    self.sprite.play()
                    if(self.sprite.get_curr_frame()==3):
                        self.sprite.pause()
            else:
                if self.teclado.key_pressed("LEFT") or self.teclado.key_pressed("RIGHT"):
                    self.trocar_animacao("walk")
                    self.sprite.set_total_duration(800)
                    self.sprite.play()
                    if self.teclado.key_pressed("LEFT"):
                        self.x -= self.vx*janela.delta_time()  
                    else: self.x += self.vx*janela.delta_time()
                else:
                    self.trocar_animacao("walk")
                    self.sprite.stop()
            if not self.chao:
                self.trocar_animacao("jump")
        else:
            self.trocar_animacao("power")
            self.counter+=1*janela.delta_time()
            if(self.counter>2):
                self.powerUse = False
                self.counter = 0

        self.sprite.update()
        self.sprite.set_position(self.x, self.y)
        if not self.chao and self.collided(chao):
            self.vy = 0
            while self.collided(chao):
                self.y -=1
                self.chao = True
        if not self.chao: self.vy += self.a
        
    def draw(self):
        self.sprite.draw()
        self.sprite.draw_collision_box((255,0,0))

        


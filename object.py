from PPlay.sprite import Sprite
from PPlay.collision import Collision

ACOPLADO = 0
CAINDO = 1
NOCHAO = 2
ROUBADO = 3
DESTRUIDO = 4

class Object(Sprite):
    def __init__(self, x, y, caminho_imagem, pai):
        super().__init__(caminho_imagem)
        self.set_position(x, y)
        self.pai = pai
        self.portador = pai
        self.state = ACOPLADO
        self.vy = 0
        self.g = 20
        
    def descolar(self, x, y):
        self.portador = None
        self.state = CAINDO
        self.set_position(x, y)
        
    def acoplar(self, mendigo, men):
        if self.state == NOCHAO and Collision.collided(self, mendigo):
            print("i")
            self.portador = men
            if self.pai == self.portador:
                self.state = ACOPLADO
            else:
                self.state = ROUBADO
            return self
        return None
            
    
    def update(self, janela, chao):
        
        if self.state == CAINDO:
            self.y += self.vy * janela.delta_time()
            self.vy += self.g
            if self.y + self.height > chao.y:
                self.y = chao.y - self.height
                self.state = NOCHAO
    
    def draw(self):
        if self.state in [CAINDO, NOCHAO]:
            super().draw()
        
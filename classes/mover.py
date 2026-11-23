from PPlay.sprite import Sprite
from PPlay.mouse import Mouse

class Mover(Sprite):

    def __init__(self, caminho_imagem, x, y):
        super().__init__(caminho_imagem)
        self.set_position(x,y)
        self.ini = x
        self.fim = x+147
        self.moving = False

    def get_scene(self):
        return self.scene
    
    def update(self):
        m = Mouse().get_position()
        mx = m[0]
        print(m)
        if self.moving:
            self.x = mx-self.width/2
            if mx-self.width/2 < self.ini:
                self.x = self.ini

            elif mx+self.width/2 > self.fim:
                self.x = self.fim - self.width
               
            if not Mouse().button_pressed(1):
                self.moving = False
        else:
            if Mouse().button_down(1) and Mouse().is_over_object(self):
                self.moving = True
                



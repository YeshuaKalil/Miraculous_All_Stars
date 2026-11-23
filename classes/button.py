from PPlay.sprite import Sprite
from PPlay.mouse import Mouse

class Button(Sprite):

    def __init__(self, scene,  caminho_imagem, x, y):
        super().__init__(caminho_imagem)
        self.scene = scene
        self.set_position(x,y)

    def get_scene(self):
        return self.scene
    
    def update(self):
        if Mouse().button_down(1) and Mouse().is_over_object(self):
            return True


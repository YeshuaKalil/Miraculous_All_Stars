from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

class Button(GameImage):

    def __init__(self, scene,  caminho_imagem, x, y, sound):
        super().__init__(caminho_imagem)
        self.scene = scene
        self.set_position(x,y)
        self.sound = sound

    def get_scene(self):
        return self.scene
    
    def update(self):
        if Mouse().button_down(1) and Mouse().is_over_object(self):
            self.sound.play()
            return True


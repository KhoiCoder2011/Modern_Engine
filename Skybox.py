from Model import Quad
from Texture import Texture


class Skybox:
    def __init__(self, scene):
        self.app = scene.app
        self.location = 'assets/skybox/'
        self.format = '.png'
        self.faces = ['top', 'bottom', 'front', 'back', 'left', 'right']

        texture = [self.location + texture +
                   self.format for texture in self.faces]

        self.quad = [
            Quad(self.app, position=[0.0, 100.0, 0.0], scale=(100, 0, 100), rotation=[
                 0, 90, 0], texture=Texture(self.app, texture[0])),
            Quad(self.app, position=[0.0, -100.0, 0.0], scale=(100, 0, 100),
                 rotation=[0, -90, 0], texture=Texture(self.app, texture[1])),
            Quad(self.app, position=[0.0, 0.0, 100.0], scale=(100, 0, 100), rotation=[
                 90, 0, 90], texture=Texture(self.app, texture[2])),
            Quad(self.app, position=[0.0, 0.0, -100.0], scale=(100, 0, 100),
                 rotation=[-90, 0, 90], texture=Texture(self.app, texture[3])),
        ]

        scene.objects.extend(self.quad)

    def render(self):

        for quad in self.quad:
            quad.render()

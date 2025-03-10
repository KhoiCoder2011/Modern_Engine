from Model import *
from Settings import *


class Scene:
    def __init__(self, app):
        self.app = app

        self.objects = []
        self.add(BasicChunk(self.app, self, 100))
        self.num_obj = len(self.objects)

    def add(self, model):
        self.objects.append(model)

    def remove(self, model):
        self.objects.remove(model)

    def render(self, camera):
        for obj in self.objects:
            if camera.is_point_in_frustum(self.app, obj.position):
                obj.render()

    def update(self): ...

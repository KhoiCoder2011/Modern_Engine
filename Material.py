from Texture import Texture
import glm

class Material:
    def __init__(self, color : tuple[float, float, float] = (1, 1, 1), texture : Texture = None):
        self.color = glm.vec3(color)
        self.texture = texture
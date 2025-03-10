import numpy as np
from Settings import *


class Mesh:
    def __init__(self, object):
        self.object = object
        self.app = object.app
        self.ctx = self.app.ctx
        self.program = self.app.prog
        self.camera = self.app.camera
        self.texture = object.texture
        # self.texture = None

        self.vbo_vert = self.ctx.buffer(np.array(object.vertices, dtype='f4'))
        self.vbo_color = self.ctx.buffer(np.array(object.color, dtype='f4'))
        self.index_buffer = self.ctx.buffer(
            np.array(object.indices, dtype='u4'))
        self.text_buffer = self.ctx.buffer(
            np.array(object.text_coord, dtype='f4'))
        # self.vbo_normal = self.ctx.buffer(np.array(object.normal, dtype = 'f4'))

        # print("Shader Attributes:", self.program._attribute_locations)

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo_vert, '3f', 'in_vert'),
                (self.vbo_color, '3f', 'in_color'),
                (self.text_buffer, '2f', 'in_uv'),
                # (self.vbo_normal, '3f', 'in_normal'),
            ],
            index_buffer=self.index_buffer,
            # skip_errors = True
        )

        self.get_model_matrix()

    def get_model_matrix(self):
        self.model = glm.translate(glm.mat4(), self.object.position)
        self.model = glm.rotate(self.model, glm.radians(
            self.object.rotation.x), glm.vec3(1, 0, 0))
        self.model = glm.rotate(self.model, glm.radians(
            self.object.rotation.y), glm.vec3(0, 1, 0))
        self.model = glm.rotate(self.model, glm.radians(
            self.object.rotation.z), glm.vec3(0, 0, 1))
        self.model = glm.scale(self.model, self.object.scale)
        return self.model

    def render(self):
        self.get_model_matrix()
        self.program['m_model'].write(self.model)
        self.program['m_view'].write(self.camera.m_view)
        self.program['m_proj'].write(self.camera.m_proj)
        self.program['tex_0'] = 0
        self.texture.use(location=0)
        self.vao.render(RENDER_MODE)

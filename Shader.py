class ShaderProgram:
    def __init__(self, app, shader_name='shader'):
        self.ctx = app.ctx
        with open(f'shaders/{shader_name}.vert') as file:
            self.vertex_shader = file.read()

        with open(f'shaders/{shader_name}.frag') as file:
            self.fragment_shader = file.read()

    def get_program(self):
        program = self.ctx.program(
            vertex_shader=self.vertex_shader,
            fragment_shader=self.fragment_shader
        )
        return program

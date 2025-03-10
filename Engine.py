from UI.Text import Text
from Camera import Camera
from Scene import Scene
from Shader import ShaderProgram
import sys
import pygame as pg
import moderngl as mgl
from Settings import *
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

class Engine:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        self.window = pg.display.set_mode(RESOLUTION, flags=pg.OPENGL | pg.DOUBLEBUF)
        pg.display.set_icon(pg.image.load('assets/icon.png'))
        pg.display.set_caption('ModernGL Engine')

        self.ctx = mgl.create_context()
        self.ctx.multisample = True
        self.ctx.enable(mgl.DEPTH_TEST | mgl.BLEND)

        # ctx_size = (WIN_WIDTH / 2 * 1.1, WIN_HEIGHT  - 280)
        # self.ctx.viewport = ((WIN_WIDTH - ctx_size[0]) / 2, WIN_HEIGHT - ctx_size[1], *ctx_size)

        self.ctx.gc_mode = 'auto'
        self.delta_time = 0
        self.clock = pg.time.Clock()
        self.on_init()

    def on_init(self):
        self.camera = Camera()
        self.shader = ShaderProgram(self)
        self.prog = self.shader.get_program()
        self.scene = Scene(self)
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        self.fps = Text(self)
        self.num_obj = Text(self)

    def render(self):
        self.ctx.clear(color = BG_COLOR)
        if IS_FPS_TEXT:
            fps = self.clock.get_fps()
            self.fps.render(f'FPS : {fps :.2f}')
        if IS_NUM_OBJ_TEXT:
            self.num_obj.render(f'Num OBJ : {self.scene.num_obj}', y=50)
        self.scene.render(self.camera)

    def update(self):
        self.delta_time = self.clock.tick() * 0.001
        self.camera.update_view_matrix()
        self.scene.update()

    def destroy(self):
        self.ctx.release()
        self.prog.release()

    def handle_events(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.camera.process_keyboard('FORWARD', self.delta_time)
        if keys[pg.K_s]:
            self.camera.process_keyboard('BACKWARD', self.delta_time)
        if keys[pg.K_a]:
            self.camera.process_keyboard('LEFT', self.delta_time)
        if keys[pg.K_d]:
            self.camera.process_keyboard('RIGHT', self.delta_time)
        if keys[pg.K_e]:
            self.camera.process_keyboard('UP', self.delta_time)
        if keys[pg.K_q]:
            self.camera.process_keyboard('DOWN', self.delta_time)

        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                self.destroy()
                sys.exit()

        xoffset, yoffset = pg.mouse.get_rel()
        self.camera.process_mouse_movement(xoffset, yoffset)
    
    def run(self):
        while True:
            self.handle_events()
            self.render()
            self.update()
            pg.display.flip()


if __name__ == "__main__":
    engine = Engine()
    engine.run()

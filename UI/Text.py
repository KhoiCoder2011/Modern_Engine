import moderngl as mgl
import pygame as pg
import freetype
import glm
import numpy as np

pg.init()


class CharacterSlot:
    def __init__(self, texture, glyph):
        self.texture = texture
        self.texture_size = (glyph.bitmap.width, glyph.bitmap.rows)
        self.bearing = (glyph.bitmap_left, glyph.bitmap_top)
        self.advance = glyph.advance.x


class TextRenderer:
    def __init__(self, app):
        self.ctx = app.ctx
        self.font_file = app.font_file
        self.characters = {}
        self.width, self.height = app.window.get_size()
        self._init_gl()

    def _init_gl(self):
        vertex_shader = """
            
            in vec4 vertex; // <vec2 pos, vec2 tex>
            out vec2 TexCoords;
            uniform mat4 projection;
            void main() {
                gl_Position = projection * vec4(vertex.xy, 0.0, 1.0);
                TexCoords = vertex.zw;
            }
        """

        fragment_shader = """
            
            in vec2 TexCoords;
            out vec4 color;
            uniform sampler2D text;
            uniform vec3 textColor;
            void main() {
                vec4 sampled = vec4(1.0, 1.0, 1.0, texture(text, TexCoords).r);
                color = vec4(textColor, 1.0) * sampled;
            }
        """

        self.prog = self.ctx.program(
            vertex_shader=vertex_shader,
            fragment_shader=fragment_shader
        )

        self.prog['projection'].write(
            glm.ortho(0, self.width, self.height, 0, -1, 1))

        self.vbo = self.ctx.buffer(reserve=6 * 4 * 4)

        self.vao = self.ctx.vertex_array(
            self.prog,

            [(self.vbo, '4f', 'vertex')]
        )

        self._load_characters()

    def _load_characters(self):
        face = freetype.Face(self.font_file)
        face.set_char_size(48 * 64)

        for i in range(128):
            face.load_char(chr(i))
            glyph = face.glyph
            bitmap = glyph.bitmap

            texture = self.ctx.texture(
                (bitmap.width, bitmap.rows), 1, bytes(bitmap.buffer)
            )
            texture.repeat_x = False
            texture.repeat_y = False
            texture.filter = (mgl.LINEAR, mgl.LINEAR)

            self.characters[chr(i)] = CharacterSlot(texture, glyph)

    def render_text(self, text, x, y, scale, color):
        self.prog['textColor'].value = tuple(c / 255.0 for c in color)

        for c in text:
            ch = self.characters[c]

            xpos = x + ch.bearing[0] * scale
            ypos = y - (ch.texture_size[1] - ch.bearing[1]) * scale

            w = ch.texture_size[0] * scale
            h = ch.texture_size[1] * scale

            vertices = np.array([
                xpos,     ypos - h, 0.0, 0.0,
                xpos,     ypos,     0.0, 1.0,
                xpos + w, ypos,     1.0, 1.0,
                xpos,     ypos - h, 0.0, 0.0,
                xpos + w, ypos,     1.0, 1.0,
                xpos + w, ypos - h, 1.0, 0.0,
            ], dtype='f4')

            self.vbo.write(vertices.tobytes())
            ch.texture.use(location=0)
            self.vao.render(mgl.TRIANGLES)

            x += (ch.advance >> 6) * scale


class Text:
    def __init__(self, app, font_file='Font/JetBrainsMonoNL-Regular.ttf'):
        self.app = app
        self.window = app.window
        self.font_file = font_file
        self.ctx = app.ctx
        self.text_renderer = TextRenderer(self)

    def render(self, content, x=10, y=30, scale=0.4, color=(255, 255, 255)):
        self.text_renderer.render_text(content, x, y, scale, color)

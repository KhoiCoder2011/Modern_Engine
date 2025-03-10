import glm
import configparser
import moderngl as mgl

config_path = 'Config\config.ini'

config = configparser.ConfigParser()
config.read(config_path)

WIN_RES = glm.vec2(config.getint('Window', 'win_res_x'),
                   config.getint('Window', 'win_res_y'))

RENDER_MODE = mgl.TRIANGLES

WIN_WIDTH, WIN_HEIGHT = WIN_RES.x, WIN_RES.y
RESOLUTION = (WIN_WIDTH, WIN_HEIGHT)

SENSITIVITY = config.getfloat('Camera', 'sensitivity')
SPEED = config.getfloat('Camera', 'speed')

FOV = config.getfloat('Camera', 'fov')
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
NEAR = config.getfloat('Camera', 'near')
FAR = config.getfloat('Camera', 'far')

BG_COLOR = glm.vec3(
    config.getfloat('Window', 'r'),
    config.getfloat('Window', 'g'),
    config.getfloat('Window', 'b')
)

IS_FPS_TEXT = config.getboolean('Graphics', 'is_fps_text')
IS_NUM_OBJ_TEXT = config.getboolean('Graphics', 'is_num_obj_text')

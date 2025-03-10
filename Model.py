from Mesh import *
from Settings import *
from ObjLoader import *
from Terrain import *
import glm
import random
from numba import prange
from Material import Material
from Texture import Texture
from Noise import SimplexNoise

'''
f = Any character but != None
faces = [f] * 6  # Render All Faces and number 6 is 6 faces
faces[0] -> faces[len(faces) - 1] = [Back, Front, Bottom, Top, Left, Right]
faces[0:5] = [Back, Front, Bottom, Top, Left, Right]

cube_indices = [
    0, 1, 2, 0, 2, 3,  # Front face
    4, 5, 6, 4, 6, 7,  # Back face
    8, 9, 10, 8, 10, 11,  # Top face
    12, 13, 14, 12, 14, 15,  # Bottom face
    16, 17, 18, 16, 18, 19,  # Right face
    20, 21, 22, 20, 22, 23   # Left face
]

self.vertices = np.array([
    # Front face
    -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  # Bottom-left
    0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  # Bottom-right
    0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  # Top-right
    -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  # Top-left

    # Back face
    -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  # Bottom-left
    0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  # Bottom-right
    0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  # Top-right
    -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  # Top-left

    # Top face
    -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  # Front-left
    0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  # Front-right
    0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  # Back-right
    -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  # Back-left

    # Bottom face
    -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  # Front-left
    0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  # Front-right
    0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  # Back-right
    -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  # Back-left

    # Right face
    0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  # Front-bottom
    0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  # Front-top
    0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  # Back-top
    0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  # Back-bottom

    # Left face
    -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  # Front-bottom
    -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  # Front-top
    -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  # Back-top
    -0.5, -0.5, -0.5, -1.0,  0.0,  0.0   # Back-bottom
], dtype='f4')
'''


class OBJTM(Mesh):
    def __init__(self, app, objects, texture):
        self.app = app
        self.objects = objects
        self.position = glm.vec3(0, 0, 0)
        self.rotation = glm.vec3(0, 0, 0)
        self.scale = glm.vec3(1, 1, 1)
        self.texture = texture
        self.text_coord = [objects[0].text_coord] * len(objects)

        self.vertices, self.indices, self.color = self.create_vertices()


        super().__init__(self)

    def create_indices(self, faces):
        face_indices = [
            [4, 5, 6, 6, 7, 4],  # Back face
            [0, 1, 2, 2, 3, 0],  # Front face
            [0, 1, 5, 5, 4, 0],  # Bottom face
            [3, 2, 6, 6, 7, 3],  # Top face
            [0, 3, 7, 7, 4, 0],  # Left face
            [1, 2, 6, 6, 5, 1]   # Right face
        ]

        indices = [idx for face, idx in zip(
            faces, face_indices) if face is not None]
        return [index for sublist in indices for index in sublist]

    def create_vertices(self, size=1):
        vertices = []
        indices = []
        color = []
        offset = 0

        s = size / 2  # Kích thước từng cạnh chia đôi
        for object in self.objects:
            x, y, z = object.position.x, object.position.y, object.position.z

            cube_vertices = [
                x - s, y - s, z + s,
                x + s, y - s, z + s,
                x + s, y + s, z + s,
                x - s, y + s, z + s,
                x - s, y - s, z - s,
                x + s, y - s, z - s,
                x + s, y + s, z - s,
                x - s, y + s, z - s
            ]

            vertices.extend(cube_vertices)

            cube_indices = self.create_indices(object.faces)

            indices.extend([i + offset for i in cube_indices])
            color.extend(object.color)
            offset += 8

        return vertices, indices, color


class Cube(Mesh):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1),
                 faces: list = [0] * 6, color=(1, 1, 1), texture: Texture = None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.texture = texture
        # self.get_parameter()
        self.faces = faces

        # 24 vertices = 6 faces * 4 vertices / face
        self.vertices = np.array([

            # Back face
            -0.5, -0.5, -0.5,  # Bottom-left
            0.5, -0.5, -0.5,  # Bottom-right
            0.5,  0.5, -0.5,  # Top-right
            -0.5,  0.5, -0.5,  # Top-left

            # Front face
            -0.5, -0.5,  0.5,  # Bottom-left
            0.5, -0.5,  0.5,  # Bottom-right
            0.5,  0.5,  0.5,  # Top-right
            -0.5,  0.5,  0.5,  # Top-left

            # Bottom face
            -0.5, -0.5,  0.5,  # Front-left
            0.5, -0.5,  0.5,  # Front-right
            0.5, -0.5, -0.5,  # Back-right
            -0.5, -0.5, -0.5,  # Back-left

            # Top face
            -0.5,  0.5,  0.5,  # Front-left
            0.5,  0.5,  0.5,  # Front-right
            0.5,  0.5, -0.5,  # Back-right
            -0.5,  0.5, -0.5,  # Back-left

            # Left face
            -0.5, -0.5,  0.5,  # Front-bottom
            -0.5,  0.5,  0.5,  # Front-top
            -0.5,  0.5, -0.5,  # Back-top
            -0.5, -0.5, -0.5,   # Back-bottom

            # Right face
            0.5, -0.5,  0.5,  # Front-bottom
            0.5,  0.5,  0.5,  # Front-top
            0.5,  0.5, -0.5,  # Back-top
            0.5, -0.5, -0.5  # Back-bottom
        ], dtype='f4')

        self.text_coord = np.array([
            # Back face (grass on top, dirt below)
            0.0, 0.0,
            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,

            # Front face (grass on top, dirt below)
            0.0, 0.0,   # Bottom-left
            0.5, 0.0,   # Bottom-right
            0.5, 1.0,   # Top-right
            0.0, 1.0,   # Top-left

            # Bottom face (full dirt texture)
            0.5, 0.0,   # Bottom-left
            1.0, 0.0,   # Bottom-right
            1.0, 1.0,   # Top-right
            0.5, 1.0,   # Top-left

            # Top face (full grass texture)
            0.5, 0.0,   # Bottom-left
            1.0, 0.0,   # Bottom-right
            1.0, 1.0,   # Top-right
            0.5, 1.0,   # Top-left

            # Left face (grass on top, dirt below)
            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,
            0.0, 0.0,

            # Right face (grass on top, dirt below)
            0.5, 0.0,
            0.5, 1.0,
            0.0, 1.0,
            0.0, 0.0,
        ], dtype='f4')

        '''self.normal = np.array([
            *[ 0.0,  0.0,  1.0] * 4,
            *[ 0.0,  0.0, -1.0] * 4,
            *[ 0.0,  1.0,  1.0] * 4,
            *[ 0.0, -1.0,  0.0] * 4,
            *[ 1.0,  0.0,  0.0] * 4,
            *[-1.0,  0.0,  0.0] * 4,
        ], dtype = 'f4')'''

        self.indices = self.create_indices()
        self.color = [*color] * (len(self.vertices.tolist()) // 3)
        super().__init__(self)

    def get_parameter(self):
        if self.material != None:
            self.color = self.material.color
            self.texture = self.material.texture
            if self.texture != None:
                self.text_coord = np.array([
                    0.0, 0.0,
                    1.0, 0.0,
                    1.0, 1.0,
                    0.0, 1.0,
                ] * 6, dtype='f4')
        else:
            # Set default
            self.color = glm.vec3(1, 1, 1)
            self.texture = None
            self.text_coord = np.array([
                0.0
            ] * 48, dtype='f4')

            # self.texture = Texture(self.app, 'assets/grass.png')
            '''self.text_coord = np.array([
                0.0, 0.0,
                1.0, 0.0,
                1.0, 1.0,
                0.0, 1.0,
            ] * 6, dtype='f4')
            '''

    def create_indices(self):
        face_indices = [
            [0, 1, 2, 0, 2, 3],  # Front face
            [4, 5, 6, 4, 6, 7],  # Back face
            [8, 9, 10, 8, 10, 11],  # Top face
            [12, 13, 14, 12, 14, 15],  # Bottom face
            [16, 17, 18, 16, 18, 19],  # Right face
            [20, 21, 22, 20, 22, 23]   # Left face
        ]

        indices = [idx for face, idx in zip(
            self.faces, face_indices) if face is not None]
        return np.array([index for sublist in indices for index in sublist], dtype='u4')


class Quad(Mesh):
    def __init__(self, app, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), color=(1, 1, 1), faces: list = [0] * 6, texture=None):
        self.app = app
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.color = color
        self.texture = texture
        self.faces = faces

        # 4 vertices = 1 faces * 4 vertices / face
        self.vertices = np.array([
            -0.5, 0.0,  0.5,
            0.5, 0.0,  0.5,
            0.5, 0.0, -0.5,
            -0.5, 0.0, -0.5
        ], dtype='f4')

        self.text_coord = np.array([
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,
        ], dtype='f4')

        self.indices = np.array([
            0, 1, 2,
            2, 3, 0
        ], dtype='u4')
        self.color = [*color] * (len(self.vertices.tolist()) // 3)
        super().__init__(self)


class ObjModel(Mesh):
    def __init__(self, app, path, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), color=(1, 1, 1), texture=None):
        self.app = app
        self.path = path
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.scale = glm.vec3(scale)
        self.obj_loader = ObjLoader(self.path)
        self.texture = texture

        self.vertices = self.obj_loader.get_vertices()
        self.indices = self.obj_loader.get_indices()
        self.normals = self.obj_loader.get_normals()
        self.text_coord = self.obj_loader.get_texture_coords()
        self.color = [color] * len(self.vertices)

        super().__init__(self)


class Chunk:
    def __init__(self, app, chunk_size: int = 16, cave_depth: int = 10):
        self.app = app
        self.chunk_size = chunk_size
        self.cave_depth = cave_depth
        self.gen_chunk()
        self.chunk = OBJTM(self.app, self.voxels, texture=Texture(self.app, 'assets/mix.png'))

    def gen_voxel(self):
        arr = prange(self.chunk_size + 1)
        voxels = []

        for x in arr:
            for z in arr:
                pos = glm.vec3(x, int(sin_cos(x, z) * 3.5), z)
                voxels.append(pos)
        return voxels

    def hash31(self, num: int):
        p3 = glm.fract(glm.vec3(num) * glm.vec3(0.1031, 0.1030, 0.0973))
        p3 += glm.dot(p3, p3.yzx + 33.33)
        return glm.fract((p3.xxy + p3.yzz) * p3.zyx)

    def gen_chunk(self):
        self.voxels = []
        voxels = self.gen_voxel()

        directions = [
            glm.vec3(0,  0, -1),
            glm.vec3(0,  0,  1),
            glm.vec3(0, -1,  0),
            glm.vec3(0,  1,  0),
            glm.vec3(-1,  0,  0),
            glm.vec3(1,  0,  0)
        ]

        voxel_set = set(tuple(v) for v in voxels)

        for position in voxels:
            faces = [None] * 6

            for i, direction in enumerate(directions):
                if tuple(position + direction) not in voxel_set:
                    faces[i] = 0

            if faces != [None] * 6:
                color = self.hash31(position.x + position.y + position.z)
                cube = Cube(self.app, position, faces=faces)
                self.voxels.append(cube)

    def render(self):
        self.chunk.render()


class BigChunk:
    def __init__(self, app, chunk_size: int = 16):
        self.app = app
        self.chunk_size = chunk_size
        self.gen_chunk()
        self.chunk = OBJTM(self.app, self.voxels)

    def gen_voxel(self):
        arr = prange(self.chunk_size + 1)
        for x in arr:
            for y in arr:
                for z in arr:
                    yield glm.vec3(x, y, z)

    def hash31(self, num: int):
        p3 = glm.fract(glm.vec3(num) * glm.vec3(0.1031, 0.1030, 0.0973))
        p3 += glm.dot(p3, p3.yzx + 33.33)
        return glm.fract((p3.xxy + p3.yzz) * p3.zyx)

    def gen_chunk(self):
        self.voxels = []
        voxels = self.gen_voxel()

        directions = np.array([
            glm.vec3(0,  0, -1),
            glm.vec3(0,  0,  1),
            glm.vec3(0, -1,  0),
            glm.vec3(0,  1,  0),
            glm.vec3(-1,  0,  0),
            glm.vec3(1,  0,  0)
        ])

        for position in voxels:
            faces = [None] * 6

            for i, direction in enumerate(directions):
                if position + direction not in voxels:
                    faces[i] = 0

            if faces != [None] * 6:
                color = self.hash31(position.x + position.y + position.z)
                self.voxels.append(
                    Cube(self.app, position, faces=faces, color=color))

    def render(self):
        self.chunk.render()


class BasicChunk:
    def __init__(self, app, scene, chunk_size: int = 16):
        self.app = app
        self.scene = scene
        self.chunk_size = chunk_size
        self.initalize()
        self.position = glm.vec3(0)
        self.scene.objects.extend(self.voxels)

    def gen_voxel(self):
        v = []
        arr = prange(self.chunk_size + 1)
        for x in arr:
            for z in arr:
                v.append(glm.vec3(x, int(sin_cos(x, z) * 2.5), z))
        return v

    def initalize(self):
        self.voxels = []
        voxels = self.gen_voxel()

        directions = np.array([
            glm.vec3(0,  0, -1),
            glm.vec3(0,  0,  1),
            glm.vec3(0, -1,  0),
            glm.vec3(0,  1,  0),
            glm.vec3(-1,  0,  0),
            glm.vec3(1,  0,  0)
        ])

        for position in voxels:
            faces = [None] * 6

            for i, direction in enumerate(directions):
                if position + direction not in voxels:
                    faces[i] = 0

            if faces != [None] * 6:
                self.voxels.append(
                    Cube(self.app, position, faces=faces, texture=Texture(self.app, 'assets/mix.png')))

    def render(self):
        pass

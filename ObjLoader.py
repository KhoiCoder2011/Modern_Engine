import numpy as np


class ObjLoader:
    def __init__(self, path):
        self.path = path

    def get_vertices(self):
        vertices = []
        with open(self.path, 'r') as file:
            for line in file:
                if line.startswith('v '):
                    vertices.append(np.array(line[2:].split(), dtype='f4'))
        return vertices

    def get_indices(self):
        indices = []
        with open(self.path, 'r') as file:
            for line in file:
                if line.startswith('f '):
                    indices.extend(
                        int(index.split('/')[0]) - 1 for index in line[2:].split())
        return indices

    def get_normals(self):
        normals = []
        with open(self.path, 'r') as file:
            for line in file:
                line = line.strip()
                if line.startswith('vn '):
                    normals.append(list(map(float, line.split()[1:])))
        return normals

    def get_texture_coords(self):
        texture_coords = []

        with open(self.path, 'r') as file:
            for line in file:
                if line.startswith('vt'):
                    parts = line.split()
                    texture_coords.append([float(parts[1]), float(parts[2])])

        return texture_coords

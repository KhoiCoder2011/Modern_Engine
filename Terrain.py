import numpy as np
from opensimplex import OpenSimplex
from numba import prange

width = 256
height = 256
scale = 100.0
octaves = 8
persistence = 0.6
lacunarity = 2.0
seed = 42

tmp = OpenSimplex(seed)


def _terrain(width, height, scale, octaves, persistence, lacunarity, tmp):
    terrain = np.zeros((height, width))
    for z in prange(height):
        for x in prange(width):
            nx = x / scale
            ny = z / scale
            amplitude = 1.0
            frequency = 1.0
            noise_value = 0.0

            for _ in range(octaves):
                noise_value += tmp.noise2(nx * frequency,
                                          ny * frequency) * amplitude
                frequency *= lacunarity
                amplitude *= persistence

            terrain[z][x] = noise_value

    return terrain


terrain = _terrain(width, height, scale, octaves, persistence, lacunarity, tmp)


def basic_noise2d(x, z):
    return tmp.noise2(x, z)


def noise2d(x, z):
    return terrain[x][z] / (width * height)


def sin_cos(x, z):
    return np.sin(x * 0.4) + np.cos(z * 0.5)

import glm
import random
from opensimplex import OpenSimplex

class Noise:
    def __init__(self, seed = 1):
        self.seed = seed
        self.noise = OpenSimplex(self.seed)

    def _noise_2d(self, x : glm.vec2) -> float:
        return self.noise.noise2(x.x, x.y)

    def _noise_3d(self, x : glm.vec3) -> float:
        return self.noise.noise3(x.x, x.y, x.z)

class Math:
    def sqrt(x : float) -> float:
        return x ** 0.5
    
    def abs(x : float) -> float:
        return abs(x)

    def normalize_3d(vector : glm.vec3):
        normalize_vec = glm.normalize(vector)
        return Vector3(normalize_vec.x, normalize_vec.y, normalize_vec.z)

    def calculate_normal_3d(x : glm.vec3, y : glm.vec3, z : glm.vec3) -> glm.vec3:
        normal_vec = glm.normalize(glm.cross(x - y, z - y))
        return Vector3(normal_vec.x, normal_vec.y, normal_vec.z)

    def clamp(number : float, min_val : float, max_val : float) -> float:
        return max(min(number, max_val), min_val)
    
    def sin(a : float) -> float:
        return glm.sin(a)
    
    def cos(a : float) -> float:
        return glm.cos(a)
    
    def tan(a : float) -> float:
        return glm.tan(a)
    
    def atan(y : float, x : float) -> float:
        return glm.atan(y, x)
    
    def acos(a : float) -> float:
        return glm.acos(a)
    
    def asin(a : float) -> float:
        return glm.asin(a)
    
    def floor(x : float) -> float:
        return glm.floor(x)
    
    def ceil(x : float) -> float:
        return glm.ceil(x)
    
    def fract(x : float) -> float:
        return x - glm.floor(x)
    
    def mix(a : float, b : float, t : float) -> float:
        return a * (1 - t) + b * t
    
    def step(edge : float, x : float) -> float:
        return 1.0 if x >= edge else 0.0
    
    def smoothstep(edge0 : float, edge1 : float, x : float) -> float:
        t = Math.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t ** 2 * (3 - 2 * t)
    
    def lerp(a : float, b : float, t : float) -> float:
        return a * (1 - t) + b * t
    
    def distance(veca, vecb) -> float:
        """Tính khoảng cách giữa hai vector (Vector2 hoặc Vector3)"""
        if isinstance(veca, Vector2) and isinstance(vecb, Vector2):
            return glm.distance(veca.to_glm_vec2(), vecb.to_glm_vec2())
        
        elif isinstance(veca, Vector3) and isinstance(vecb, Vector3):
            return glm.distance(veca.to_glm_vec3(), vecb.to_glm_vec3())
        
        else:
            raise ValueError("Cả hai vector phải có cùng kiểu (Vector2 hoặc Vector3)")

class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def to_glm_vec2(self):
        """Chuyển đổi Vector2 sang glm.vec2"""
        return glm.vec2(self.x, self.y)
    
    def __add__(self, other):
        """Cộng hai vector với nhau"""
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return NotImplemented
    
    def __sub__(self, other):
        """Trừ hai vector với nhau"""
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        return NotImplemented
    
    def __mul__(self, scalar: float):
        """Nhân vector với một số (scalar)"""
        return Vector2(self.x * scalar, self.y * scalar)
    
    def length(self) -> float:
        """Tính độ dài của vector"""
        return glm.length(self.to_glm_vec2())
    
    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    
    def normalize(self):
        """Chuẩn hóa vector"""
        length = self.length()
        if length != 0:
            return self * (1 / length)
        return Vector2(0, 0)
    
class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z
    
    def to_glm_vec3(self):
        """Chuyển đổi Vector2 sang glm.vec2"""
        return glm.vec3(self.x, self.y, self.z)
    
    def __add__(self, other):
        """Cộng hai vector với nhau"""
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented
    
    def __sub__(self, other):
        """Trừ hai vector với nhau"""
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented
    
    def __mul__(self, scalar: float):
        """Nhân vector với một số (scalar)"""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def length(self) -> float:
        """Tính độ dài của vector"""
        return glm.length(self.to_glm_vec3())
    
    def __repr__(self) -> str:
        return f"Vector3({self.x}, {self.y}, {self.z})"
    
    def normalize(self):
        """Chuẩn hóa vector"""
        length = self.length()
        if length != 0:
            return self * (1 / length)
        return Vector3(0, 0, 0)

class PerlinWorm:
    def __init__(self, distance : int):
        self.distance = distance

    def get_perin_worm(self, origin : Vector3):
        worm = []
        last_value = origin
        for _ in range(self.distance):
            x = random.random() * random.random() * 3
            y = random.random() * random.random() * 3
            z = random.random() * random.random() * 3

            worm.append(last_value + Vector3(x ** 3, y ** 3, z ** 3))
   
            last_value = worm[-1]

        return worm

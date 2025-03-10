from Settings import *

speed = SPEED
sensitivity = SENSITIVITY
FOV = glm.radians(FOV)


class Camera:
    def __init__(self, position=(0, 0, -5), front=(0, 0, 1), up=(0, 1, 0), rotation=(0, 90, 0)):
        self.position = glm.vec3(position)
        self.rotation = glm.vec3(rotation)
        self.forward = glm.vec3(front)
        self.up = glm.vec3(up)

        self.pitch = self.rotation.x
        self.yaw = self.rotation.y
        self.roll = self.rotation.z

        self.update_projection_matrix()
        self.update_view_matrix()

    def update_view_matrix(self):
        # * glm.rotate(glm.mat4(1.0), glm.radians(self.roll), glm.vec3(0, 0, 1))
        self.m_view = glm.lookAt(
            self.position, self.position + self.forward, self.up)

    def update_projection_matrix(self):
        self.m_proj = glm.perspective(FOV, ASPECT_RATIO, NEAR, FAR)

    def process_keyboard(self, direction, delta_time=1):
        velocity = speed * delta_time
        if direction == "FORWARD":
            self.position += self.forward * velocity
        elif direction == "BACKWARD":
            self.position -= self.forward * velocity
        elif direction == "UP":
            self.position += self.up * velocity
        elif direction == "DOWN":
            self.position -= self.up * velocity
        elif direction == "LEFT":
            self.position -= glm.normalize(glm.cross(self.forward,
                                           self.up)) * velocity
        elif direction == "RIGHT":
            self.position += glm.normalize(glm.cross(self.forward,
                                           self.up)) * velocity

    def process_mouse_movement(self, x_offset, y_offset):
        x_offset *= sensitivity
        y_offset *= sensitivity

        self.yaw += x_offset
        self.pitch -= y_offset
        self.pitch = glm.clamp(self.pitch, -89.9, 89.9)
        self.update_front()

    def update_front(self):
        self.forward = glm.normalize(
            glm.vec3(
                glm.cos(glm.radians(self.yaw)) *
                glm.cos(glm.radians(self.pitch)),
                glm.sin(glm.radians(self.pitch)),
                glm.sin(glm.radians(self.yaw)) *
                glm.cos(glm.radians(self.pitch))
            )
        )

    def is_point_in_frustum(self, app, point):
        point_view = glm.vec4(*point, 1.0)
        point_camera = app.camera.m_view * point_view
        point_clip = app.camera.m_proj * point_camera

        if point_clip.w == 0:
            return False

        x = point_clip.x / point_clip.w
        y = point_clip.y / point_clip.w
        z = point_clip.z / point_clip.w

        if -1.5 <= x <= 1.5 and -1.5 <= y <= 1.5 and -1.5 <= z <= 1.5:
            return True

        if glm.length2(app.camera.position - point) <= 16:
            return True

        return False

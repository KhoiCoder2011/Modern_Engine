'''
a (m/s^2)
v (m/s)
t (s)
g (m/s^2)

GRAVITY = 9.81
acceleration = 0
velocity = 0
time = 0

'''

GRAVITY = 9.81


class Rigidbody:
    def __init__(self, app, object):
        self.t = 0
        self.object = object
        self.is_gravity = True
        if self.is_gravity:
            self.gravity = GRAVITY
        else:
            self.gravity = 0

    def update(self, time):
        self.t += time
        self.object.position.y -= 0.5 * self.gravity * self.t ** 2

from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Box2D import *
import math
import clases.audio
from disparos import disparos
size_tile=0.16
class armas:
    def __init__ (self,damage, delay, type_id, bullet, body, world):
        self.damage = damage
        self.delay = delay
        self.type_id = type_id
        self.bullet = bullet
        self.block_fire = delay
        self.body = body
        self.world = world
    def set_body(self, body):
        self.body = body
    def get_id(self):
        return self.type_id
    def get_value(self):
        pass
    def update(self, t_delta):
        if (self.block_fire >= 0):
                self.block_fire -= t_delta
    def fire(self):
        if (self.block_fire < 0.0):
            self.block_fire = self.delay
            clases.audio.efectSound(26)
            body_tmp = self.body.get_body()
            self.bullet.append(disparos(self.world.CreateDynamicBody(
                position=(body_tmp.position[0]+(math.cos(body_tmp.angle)*0.22),body_tmp.position[1]+(math.sin(body_tmp.angle)*0.22)),
                bullet=True,angle = body_tmp.angle,  angularDamping=0.0, linearDamping= 5.0,
                fixtures=b2FixtureDef(shape=b2CircleShape(radius=(size_tile/8.0)), density=60),
                linearVelocity=(50*math.cos(body_tmp.angle), 50*math.sin(body_tmp.angle))), 0)
            )

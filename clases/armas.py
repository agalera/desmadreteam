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
    def __init__ (self, type_id , bullet, body, world, global_DL):
        #
        if (type_id == 1):
            self.delay = 400
            self.damage = 500
        if (type_id == 2):
            self.delay = 200
            self.damage = 100
        if (type_id == 3):
            self.delay = 700
            self.damage = 900
        self.global_DL = global_DL
        self.type_id = type_id
        self.bullet = bullet
        self.block_fire = self.delay
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
    def use(self):

        if (self.block_fire < 0.0):
            self.block_fire = self.delay
            body_tmp = self.body.get_body()
            if (self.type_id == 1 or self.type_id == 2 or self.type_id == 3):
                clases.audio.efectSound(26)
                self.bullet.append(disparos(self.world.CreateDynamicBody(
                    position=(body_tmp.position[0]+(math.cos(body_tmp.angle)*0.22),body_tmp.position[1]+(math.sin(body_tmp.angle)*0.22)),
                    bullet=True, angle = body_tmp.angle,  angularDamping=0.0, linearDamping= 5.0,
                    fixtures=b2FixtureDef(shape=b2CircleShape(radius=(size_tile/8.0)),isSensor= False, density=self.damage),
                    linearVelocity=(50*math.cos(body_tmp.angle), 50*math.sin(body_tmp.angle))), 0,self.global_DL)
                )
            if (self.type_id == 3):
                body_tmp.angle += 0.2
                self.bullet.append(disparos(self.world.CreateDynamicBody(
                    position=(body_tmp.position[0]+(math.cos(body_tmp.angle)*0.22),body_tmp.position[1]+(math.sin(body_tmp.angle)*0.22)),
                    bullet=True, angle = body_tmp.angle,  angularDamping=0.0, linearDamping= 5.0,
                    fixtures=b2FixtureDef(shape=b2CircleShape(radius=(size_tile/8.0)),isSensor= False, density=self.damage),
                    linearVelocity=(50*math.cos(body_tmp.angle), 50*math.sin(body_tmp.angle))), 0,self.global_DL)
                )
                body_tmp.angle -= 0.4
                self.bullet.append(disparos(self.world.CreateDynamicBody(
                    position=(body_tmp.position[0]+(math.cos(body_tmp.angle)*0.22),body_tmp.position[1]+(math.sin(body_tmp.angle)*0.22)),
                    bullet=True, angle = body_tmp.angle,  angularDamping=0.0, linearDamping= 5.0,
                    fixtures=b2FixtureDef(shape=b2CircleShape(radius=(size_tile/8.0)),isSensor= False, density=self.damage),
                    linearVelocity=(50*math.cos(body_tmp.angle), 50*math.sin(body_tmp.angle))), 0,self.global_DL)
                )
                body_tmp.angle += 0.2
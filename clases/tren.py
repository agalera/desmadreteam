from __future__ import division

import math
from Box2D import *
import copy
from disparos import disparos
from components import components
from clases.asteroids import asteroids
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import clases.audio
from random import randint

size_tile = 0.16

class tren:
    def __init__ (self, pos_init, world, bullet):
        #self.world = world
        self.bullet = bullet
        self.pos_init = pos_init
        #self.create_player()
        self.touch = False
        self.mode_normal = True
        self.world = world
        self.create_player()
        self.damage = 0.0
        self.block_fire = 1200
        self.timelap = 0.0

    def add_damage(self, damages):
        print "yo"
        pass
        #self.damage += damages
        #print "damage: " + str(damages)
        #if (self.damage > 1 and self.mode_normal == True):
        #    self.change_mode()

    def change_touch(self, val=False):
        self.touch = val

    def create_player(self):
        self.body = self.create_box()
        #self.body.userData

    def create_box(self):
        tmp = asteroids(self.world.CreateDynamicBody(position=(self.pos_init[0]*size_tile,self.pos_init[1]*size_tile), angularDamping=10.0, linearDamping= 5.0), 2, 50000, [6.0,3.0])
        #print tmp.get_body()
        return tmp
        #tmp = self.world.CreateDynamicBody(position=(pos),angularDamping=30.0, linearDamping= 20.0, angle= 0)
        #return tmp.CreateCircleFixture(radius=(size_tile/1.2),density=100000, friction= 0)
    def get_normal(self):
        return self.mode_normal
    def get_position(self):
        return self.body.get_position()

    def draw_sangre(self):
        self.body.draw(self.id_sangre, self.sangre_angle)
    def open_fire(self, body_tmp):
        if(self.block_fire < 0.0):
            self.block_fire = 600.0
            self.bullet.append(disparos(self.world.CreateDynamicBody(
                position=(body_tmp.position[0]+(math.cos(body_tmp.angle)*0.3),body_tmp.position[1]+(math.sin(body_tmp.angle)*0.3)),
                bullet=True,angle = body_tmp.angle,  angularDamping=0.0, linearDamping= 5.0,
                fixtures=b2FixtureDef(shape=b2CircleShape(radius=(size_tile/8.0)), density=60),
                linearVelocity=(50*math.cos(body_tmp.angle), 50*math.sin(body_tmp.angle))), 0)
            )
    def draw(self, t_delta):

        if (self.mode_normal == False and self.body.get_vivo() == True):
            self.body.set_vivo()
            self.body.destruyeme()
        else:
            try:
                body_tmp = self.body.get_body()
                body_tmp.angle = -1.57
                if (self.block_fire >= 0):
                    self.block_fire -= t_delta

                if (self.timelap >= 0):
                    self.timelap -= t_delta

                
                if body_tmp.position[1] < 1.14:
                    self.body.get_body().position = [18.43, 90.0]

                if(self.timelap < 0.0):
                    clases.audio.efectSound(25)
                    self.timelap = 20000.0
                    self.body.get_body().position = [18.43, 9.0]

                if(self.body.get_body().position[1]< 6.0 and self.body.get_body().position[1] > 3.0):
                    speed = (1.0-self.damage)*100
                else:
                    speed = (1.0-self.damage)*400
                #print self.body.get_body().position
                #speed = (1.0-self.damage)*200
                body_tmp.ApplyLinearImpulse(b2Vec2(0.0,-speed*t_delta), b2Vec2(body_tmp.position[0],2+body_tmp.position[1]),1)
            except:
                pass

        if (self.mode_normal == True):
            self.body.draw(-1)
        
    def change_mode(self):
        self.mode_normal = not self.mode_normal
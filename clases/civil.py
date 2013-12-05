from __future__ import division

import math
from Box2D import *
import copy
from components import components
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import clases.audio
from random import randint
import clases.audio
from objetos import objetos
from armas import armas

size_tile = 0.16

class civil:
    def __init__ (self, pos_init, world, tileid, player, bullet, Lchunk):
        #self.world = world
        self.Lchunk = Lchunk
        self.bullet = bullet
        self.player = player
        self.sangre_angle = randint(0,360)
        self.id_sangre = randint(51,58)
        self.tileid = tileid
        self.pos_init = pos_init
        #self.create_player()
        self.touch = False
        self.mode_normal = True
        self.world = world
        self.create_player()
        self.damage = 0.0
        if self.tileid == 16:
            self.arma = armas(1, 1000, 1, self.bullet, self.body, self.world)
        else:
            self.arma = None
    def add_damage(self, damages):
        self.damage += damages
        #print "damage: " + str(damages)
        clases.audio.efectSound(randint(16,24))
        if (self.damage > 1 and self.mode_normal == True):
            pos = [0,0]
            pos[0] = int((self.body.get_body().position[0]+0.16) * 3.125)
            pos[1] = int((self.body.get_body().position[1]+0.16) * 3.125)
            if self.arma == None:
                if randint(0,30) == 30:
                    self.Lchunk[0].set_object(pos, consumibles(496,2.0))
            else:
                self.Lchunk[0].set_object(pos, self.arma)
            self.change_mode()

    def get_arma(self):
        return self.arma
    def set_arma(self, arma):
        self.arma = arma

    def change_touch(self, val=False):
        self.touch = val

    def create_player(self):
        pos = [self.pos_init[0],self.pos_init[1]]
        self.body = components(self.create_box(pos), self, 1, self.world)
        #self.body.userData

    def create_box(self, pos):
        tmp = self.world.CreateDynamicBody(position=(pos),angularDamping=30.0, linearDamping= 20.0, angle= 0)
        return tmp.CreateCircleFixture(radius=(size_tile/1.2),density=1, friction= 0)
    def get_normal(self):
        return self.mode_normal
    def get_position(self):
        return self.body.get_position()
    def get_tileid(self):
        return self.tileid
    def draw_sangre(self):
        self.body.draw(self.id_sangre, self.sangre_angle)
    def open_fire(self, body_tmp):
            self.arma.use()

    def draw(self, t_delta, animate):

        if (self.mode_normal == False and self.body.get_vivo() == True):
            self.body.set_vivo()
            self.body.destruyeme()
        if (self.mode_normal == False and self.body.get_vivo() == False):
            self.body.draw(self.tileid+15, 0.0)
        else:
            if self.arma != None:
                self.arma.update(t_delta)
            body_tmp = self.body.get_body()
            pasive_position = self.player.get_position()
            if (self.tileid == 16):
                speed = (1.0-self.damage)*0.0015
                body_tmp.angle = -(math.atan2(pasive_position[0][0]-body_tmp.position[0], pasive_position[0][1]-body_tmp.position[1]))+1.57

                body_tmp.ApplyLinearImpulse(b2Vec2(speed*t_delta*math.cos(body_tmp.angle), speed*t_delta*math.sin(body_tmp.angle)), b2Vec2(body_tmp.position[0],body_tmp.position[1]),1)
                self.open_fire(body_tmp)
            else:
                speed = (1.0-self.damage)*0.003
                #body_tmp.angle = -(math.atan2(pasive_position[0][0]-body_tmp.position[0], pasive_position[0][1]-body_tmp.position[1]))-1.57
                body_tmp.ApplyTorque(randint(-40,40)/10,1)
                body_tmp.ApplyLinearImpulse(b2Vec2(speed*t_delta*math.cos(body_tmp.angle), speed*t_delta*math.sin(body_tmp.angle)), b2Vec2(body_tmp.position[0],body_tmp.position[1]),1)
            self.body.draw(self.tileid+2+int(animate / 8))

    def change_mode(self):
        self.mode_normal = not self.mode_normal
from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Box2D import *
import math
import clases.basicas as basicas
size_tile = 0.16
class components:
    def __init__ (self,main, masterclass, id_t, world, global_DL, draw_optional = True):
        self.draw_optional = draw_optional
        self.global_DL = global_DL
        self.world = world
        self.main = main
        self.id_t = id_t
        self.main.body.userData = self
        self.masterclass = masterclass
        self.vivo = True
        self.position = [[0,0],0]
        #self.damage = 0.0
    def set_draw_optional(self, option):
        self.draw_optional = option
    def get_vivo(self):
        return self.vivo
    def set_vivo(self):
        self.vivo = False
    def destruyeme(self):
        #print self.main
        self.world.DestroyBody(self.main.body)
        self.main = None

    def touch(self, touch):
        self.masterclass.change_touch(touch)

    def get_main(self):
        return self.main

    def get_body(self):
        return self.main.body

    def add_damage(self, fl):
        self.masterclass.add_damage(fl)

    def get_position(self):
        return [self.main.body.position, self.main.body.angle]

    def get_worldcenter(self):
        return self.main.body.worldCenter

    def draw(self, posible = False, angle = False, zindex= 0.0):
        if (self.main != None):
            self.position[0][0] = self.main.body.position[0]
            self.position[0][1] = self.main.body.position[1]
            self.position[1] = self.main.body.angle

        if (posible != False):
            texture_info_temp = int(posible)
        else:
            texture_info_temp = int(self.id_t)
        if (angle != False):
            self.position[1] = angle
        #basicas.put_texture(True, texture_info_temp)
        if self.draw_optional:
            x2 = self.masterclass.get_masterclass().get_position()[0][0]
            if (x2+ 6 < self.position[0][0] or self.position[0][0] < x2- 6):
                return False

            #print self.position[0][0] , self.position[0][1], zindex
        glTranslatef( self.position[0][0] , self.position[0][1], zindex)
        glRotate(math.degrees(self.position[1]), 0, 0, 1)
        glCallList(self.global_DL+texture_info_temp)
        glRotate(math.degrees(self.position[1]), 0, 0, -1)
        glTranslatef( -self.position[0][0] , -self.position[0][1], -zindex)
        #basicas.put_texture(False)
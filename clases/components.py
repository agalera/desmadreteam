from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Box2D import *
import math

size_tile = 0.16
class components:
    def __init__ (self,main, masterclass, id_t, world):
        self.world = world
        self.main = main
        self.id_t = id_t
        self.main.body.userData = self
        self.masterclass = masterclass
        self.vivo = True
        self.position = [[0,0],0]
        #self.damage = 0.0
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

    def draw(self, posible = False, angle = False, zindex= 0.1):
        if (self.main != None):
            self.position[0][0] = self.main.body.position[0]
            self.position[0][1] = self.main.body.position[1]
            self.position[1] = self.main.body.angle

        if (posible != False):
            texture_info_temp = [int(posible), 0];
        else:
            texture_info_temp = [int(self.id_t), 0]
        if (angle != False):
            self.position[1] = angle
        textureXOffset = float(texture_info_temp[0]/16.0)+0.001
        textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
        textureHeight  = float(0.060)
        textureWidth   = float(0.060)

        glTranslatef( self.position[0][0] , self.position[0][1], zindex)
        glRotate(math.degrees(self.position[1]), 0, 0, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
        glVertex2f(-size_tile, -size_tile)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
        glVertex2f(size_tile, -size_tile)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
        glVertex2f( size_tile,  size_tile)

        glTexCoord2f(textureXOffset,textureYOffset)
        glVertex2f(-size_tile, size_tile)
        glEnd()
        glRotate(math.degrees(self.position[1]), 0, 0, -1)
        glTranslatef( -self.position[0][0] , -self.position[0][1], -zindex)
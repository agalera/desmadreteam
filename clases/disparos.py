from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

size_tile = 0.16
class disparos:
    def __init__ (self,body, hook):
        self.body = body
        self.hook = hook
        self.body.userData = self
        self.damage = 0.0
    def get_hook(self):
    	return self.hook
    def get_body(self):
        return self.body
    def add_damage(self, fl):
        if (self.damage != 0.0):
            "esto ya ha colisionado antes eh"
        self.damage += fl
    def awake(self):
        return self.body.awake
    def set_awake(self, boolean):
        self.body.awake = boolean
    def touch(self, touch):
        pass
    def get_position(self):
        return [self.body.position, self.body.angle]

    def draw(self):
        texture_info_temp = [int(1), 0];
        textureXOffset = float(texture_info_temp[0]/16.0)+0.001
        textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
        textureHeight  = float(0.060)
        textureWidth   = float(0.060)

        glTranslatef( self.body.position[0] , self.body.position[1], 0.00)
        glRotate(math.degrees(self.body.angle), 0, 0, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
        glVertex3f(-size_tile, -size_tile, 0)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
        glVertex3f(size_tile, -size_tile, 0)

        glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
        glVertex3f( size_tile,  size_tile, 0)

        glTexCoord2f(textureXOffset,textureYOffset)
        glVertex3f(-size_tile, size_tile, 0)
        glEnd()
        glRotate(math.degrees(self.body.angle), 0, 0, -1)
        glTranslatef( -self.body.position[0] , -self.body.position[1], 0.00)
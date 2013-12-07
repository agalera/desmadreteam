from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import clases.basicas as basicas

size_tile = 0.16
class disparos:
    def __init__ (self,body, hook, global_DL):
        self.global_DL = global_DL
        self.body = body
        self.hook = hook
        self.body.userData = self
    def get_hook(self):
    	return self.hook
    def get_body(self):
        return self.body
    def add_damage(self, fl):
        pass
#        if (self.damage != 0.0):
#            "esto ya ha colisionado antes eh"
#        self.damage += fl
    def awake(self):
        return self.body.awake
    def set_awake(self, boolean):
        self.body.awake = boolean
    def touch(self, touch):
        pass
    def get_position(self):
        return [self.body.position, self.body.angle]

    def draw(self):
        basicas.put_texture(True, 1)
        glTranslatef( self.body.position[0] , self.body.position[1], 0.00)
        glRotate(math.degrees(self.body.angle), 0, 0, 1)

        glCallList(self.global_DL[0])

        glRotate(math.degrees(self.body.angle), 0, 0, -1)
        glTranslatef( -self.body.position[0] , -self.body.position[1], 0.00)
        basicas.put_texture(False)
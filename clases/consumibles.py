from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Box2D import *
import math
import clases.audio

size_tile=0.16
class consumibles:
    def __init__ (self,type_id, value):
        self.value = value
        self.type_id = type_id
    def get_id(self):
        return self.type_id
    def get_value(self):
        pass
    def use(self):
            return self.value


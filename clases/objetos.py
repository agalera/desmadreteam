from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Box2D import *
import math

class objetos:
    def __init__ (self,type_id, value):
        self.type_id = type_id
        self.value = value
    def get_id(self):
        return self.type_id
    def get_value(self):
        return self.value
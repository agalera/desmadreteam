from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Box2D import *
from armas import armas

import math

class objetos:
    def __init__ (self,type_id, value):
        self.type_id = type_id
        #armas u otros
        self.value = value

    def get_id(self):
        return self.type_id

    def get_value(self):
        return self.value
    def use(self):
        self.value.use()
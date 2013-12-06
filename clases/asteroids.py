from __future__ import division
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

size_tile = 0.16
class asteroids:
    def __init__ (self,body, tile, densitys = 1, size_tmp = [0.90,0.90]):
        self.body = body
        self.body.userData = self
        self.damage = 0.0
        self.tile = tile
        self.body.CreatePolygonFixture(box=(size_tile*size_tmp[0],size_tile*size_tmp[1]),density=densitys, friction= 10)

    def get_body(self):
        return self.body
    def get_awake(self):
        return self.body.awake
    def touch(self, touch):
        pass
    def add_damage(self, fl):
        pass
    def get_position(self):
        return [self.body.position, self.body.angle]
    def get_worldcenter(self):
        return self.body.worldCenter
    def draw(self, xp):
        x = int(self.body.position[0]*3.10)+1
        if xp == -1:
            texture_info_temp = [int(self.tile), 0];
            textureXOffset = 1
            textureYOffset = 1
            textureHeight  = 1
            textureWidth   = 1

            glTranslatef( self.body.position[0] , self.body.position[1], 0.00)
            glRotate(0, 0, 0, 1)
            glBegin(GL_QUADS)
            glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
            glVertex3f(-0.48, -1.00, 0)

            glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
            glVertex3f(0.48, -1.00, 0)

            glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
            glVertex3f( 0.48,  1.00, 0)

            glTexCoord2f(textureXOffset,textureYOffset)
            glVertex3f(-0.48, 1.00, 0)
            glEnd()
            glRotate(0, 0, 0, -1)
            glTranslatef( -self.body.position[0] , -self.body.position[1], 0.00)
        else:

            if (x+ 19 < xp or xp < x- 19):
                pass

            else:
                texture_info_temp = [int(self.tile), 0];
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
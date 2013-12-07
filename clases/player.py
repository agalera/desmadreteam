from __future__ import division

import math
from Box2D import *
import copy
from armas import armas
from components import components
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import clases.audio
from clases.objetos import objetos
from clases.armas import armas

size_tile = 0.16

class player:
    def __init__ (self, bullet,joints, borrar, global_DL):
        #self.world = world
        self.pos_init = [20.0,1.0]
        #self.create_player()
        self.bullet = bullet
        self.borrar = borrar
        self.joints = joints
        self.hook_status = 0
        self.touch = False
        self.mode_normal = True
        self.rope = None
        self.other_body = None
        self.relative_pos = None
        self.damage = 12.0
        self.global_DL = global_DL

    def change_touch(self, val=False):
        self.touch = val
    def pick_object(self, objeto_arma):
        if objeto_arma != False:
            if isinstance(objeto_arma, objetos):
                self.add_hp(objeto_arma.get_value())
            elif isinstance(objeto_arma, armas):
                self.set_arma(objeto_arma)

    def set_world(self, world):
        self.world = world
        self.create_player()
    def add_damage(self, damage):
        self.damage -= damage
        print "hola"
    def add_hp(self, hp):
        self.damage += hp
    def get_arma(self):
        return self.arma
    def set_arma(self, arma):
        self.arma = arma
        self.arma.set_body(self.body)
    def get_damage(self):
        return self.damage

    def create_player(self):
        pos = [self.pos_init[0],self.pos_init[1]]
        self.body = components(self.create_box(pos), self, 1, self.world,self.global_DL, False)
        self.arma = armas(3, self.bullet, self.body, self.world, self.global_DL)
        #
    def set_other_body(self, var, var2):

        if (self.relative_pos == None and self.hook_status == 1 and var != self.body.get_body()):
            self.relative_pos = [var2.position[0], var2.position[1]]
            self.other_body = var
            return True
        else:
            return False

    def destroy_rope(self):
        if self.rope != None:
            self.relative_pos = None
            self.world.DestroyJoint(self.rope)
            self.rope = None

    def distance(self, p0, p1):
        return math.hypot(p1[0] - p0[0], p1[1] - p0[1])

    def create_rope(self, body_focus , relative_pos, distance = None):
        if distance == None:
            distance = self.distance(self.body.get_body().position, relative_pos)

        ropeJointDef = b2DistanceJointDef()
        ropeJointDef.bodyA = self.body.get_body()
        ropeJointDef.bodyB = body_focus
        ropeJointDef.localAnchorA = b2Vec2(0,0)
        ropeJointDef.localAnchorB = b2Vec2(relative_pos[0] - body_focus.position[0],relative_pos[1] - body_focus.position[1])
        ropeJointDef.length = distance
        ropeJointDef.collideConnected = True
        ropeJointDef.frequencyHz = 2
        ropeJointDef.dampingRatio = 0.5
        self.rope = self.world.CreateJoint(ropeJointDef)
        self.rope.userData = [relative_pos[0] - body_focus.position[0],relative_pos[1] - body_focus.position[1]]
        #self.rope.bodyB.position = self.absolute_pos

    def create_box(self, pos):
        tmp = self.world.CreateDynamicBody(position=(pos),angularDamping=30.0, linearDamping= 20.0, angle= 0)

        return tmp.CreateCircleFixture(radius=(size_tile/1.2),density=1, friction= 6)

    def create_join(self,types,a,b,c):
        if (types == 'Weld'):
            tmp = b2WeldJointDef()
        else:
            tmp = b2WeldJointDef()
        tmp.Initialize(a,b,c)
        self.joints.append(self.world.CreateJoint(tmp))

    def get_position(self):
        return self.body.get_position()

    def draw(self, radians, animate, wasd):
        if (self.mode_normal == True):

            if (wasd[0] == False and wasd[1] == False and wasd[2] == False and wasd[3] == False):
                self.body.draw(int(animate / 8))
            else:
                self.body.draw(int(animate / 8)+2)

        #self.other_body.draw()
        if self.rope != None:
            self.draw_line(self.rope.bodyA.position,[self.rope.bodyB.position[0] + self.rope.userData[0], self.rope.bodyB.position[1] + self.rope.userData[1]])

    def draw_line(self,obja,objb):
        texture_info_temp = [int(0), 0];
        textureXOffset = float(texture_info_temp[0]/16.0)+0.001
        textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
        textureHeight  = float(0.060)
        textureWidth   = float(0.060)

        glLineWidth(4)

        glBegin(GL_LINES)
        glTexCoord2f(0.0,1.0)
        glVertex3f(obja[0], obja[1], 0.0)
        glTexCoord2f(0.0, 1.0)
        glVertex3f(objb[0], objb[1], 0.0)
        glEnd()

    def change_mode(self):
        self.mode_normal = not self.mode_normal


    def move(self,wasd, t_delta, radians):
        body_tmp = self.body.get_body()
        body_tmp.angle = radians
        self.arma.update(t_delta)
        if(wasd[5][0] == 1):
            self.arma.use()

        if(wasd[0] == 1):
            body_tmp.ApplyLinearImpulse(b2Vec2(0.0,0.0015*t_delta), b2Vec2(body_tmp.position[0],2+body_tmp.position[1]),1)
        if(wasd[1] == 1):
            body_tmp.ApplyLinearImpulse(b2Vec2(-0.0015*t_delta,0.0000000), b2Vec2(2+body_tmp.position[0],body_tmp.position[1]),1)
        if(wasd[2] == 1):
            body_tmp.ApplyLinearImpulse(b2Vec2(0.0,-0.0015*t_delta), b2Vec2(body_tmp.position[0],2+body_tmp.position[1]),1)
        if(wasd[3] == 1):
            body_tmp.ApplyLinearImpulse(b2Vec2(0.0015*t_delta,0.0000000), b2Vec2(2+body_tmp.position[0],body_tmp.position[1]),1)
        #if(wasd[5][0] == 1):
        #    body_tmp.ApplyLinearImpulse(b2Vec2(0.004*t_delta*math.cos(radians), 0.004*t_delta*math.sin(radians)), b2Vec2(body_tmp.position[0],body_tmp.position[1]),1)

        #if(wasd[4] == 1 and self.hook_status == 0):
        #    self.hook_status = 1
        #    #self.create_rope(1)
        #    tmp = disparos(self.world.CreateDynamicBody(
        #                    position=(body_tmp.position[0]+(math.cos(radians)*0.4),body_tmp.position[1]+(math.sin(radians)*0.4)),
        #                    bullet=True,angle = body_tmp.angle,  angularDamping=5.0, linearDamping= 1.0,
        #                    fixtures=b2FixtureDef(shape=b2CircleShape(radius=(size_tile/1.4)), density=0.1),
        #                    linearVelocity=(30*math.cos(radians), 30*math.sin(radians))), 1)
        #    self.bullet.append(tmp)
        #    #print tmp.get_body()
        #    self.create_rope(tmp.get_body(), tmp.get_body().position, 1.0)

        #if(wasd[4] == 0 and self.hook_status == 1):
        #    self.hook_status = 0
        #    self.destroy_rope()
        #    for taa in list(self.bullet):
        #        if (taa.get_hook() == 1):
        #            self.world.DestroyBody(taa.get_body())
        #            self.bullet.remove(taa)


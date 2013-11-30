from __future__ import division
from Box2D import *
import math
class myContactListener(b2ContactListener):
    def __init__(self, borrar, player):
        super(myContactListener, self).__init__()
        self.borrar = borrar
        self.player = player

    def BeginContact(self, var):
        #print var.fixtureA.body.bullet

        #print var.fixtureB.contacts
        if var.fixtureB.body.userData != None:
            if (var.fixtureB.body.position[1] > var.fixtureA.body.position[1]):
                var.fixtureB.body.userData.touch(True)

            if var.fixtureB.body.bullet == True and var.fixtureB.body.userData.get_hook() == 1:
                if var.fixtureB.body not in self.borrar:
                    if (self.player.set_other_body(var.fixtureA.body, var.fixtureB.body)):
                        self.borrar.append(var.fixtureB.body)

        if var.fixtureA.body.userData != None:
            if (var.fixtureB.body.position[1] < var.fixtureA.body.position[1]):
                var.fixtureA.body.userData.touch(True)

        #print "fixtureb: " + str(var.fixtureB.body)

#        if (var.fixtureB.body.bullet == True):
#            borrar.append(var.fixtureB.body)
        #if (var.fixtureB.body.bullet == True):
    def EndContact(self, var):

        if var.fixtureB.body.userData != None:
            if (var.fixtureB.body.position[1] > var.fixtureA.body.position[1]):
                var.fixtureB.body.userData.touch(False)


        if var.fixtureA.body.userData != None:
            if (var.fixtureB.body.position[1] < var.fixtureA.body.position[1]):
                var.fixtureA.body.userData.touch(False)
        #if var.fixtureB.body.userData != None:
        #    var.fixtureB.body.userData

    def PostSolve(self, var, var2):
        #print "var"
        #print var.manifold
        #radians = math.degrees(math.atan2(var.manifold.localNormal[0], var.manifold.localNormal[1]))+ 90.0
        #print radians
        #print var.manifold.localNormal
        #for taa in var.manifold.points:
        #    print var.manifold.localPoint
        #radians = math.degrees(math.atan2(var.manifold.localPoint[0], var.manifold.localPoint[1]))+ 90.0

        if (var2.normalImpulses[0] > 20):
            if (var.fixtureA.body.userData != None):
                var.fixtureA.body.userData.add_damage(var2.normalImpulses[0] / 2)
            #pass # recv damage /  2
            if (var.fixtureB.body.userData != None):
                var.fixtureB.body.userData.add_damage(var2.normalImpulses[0])
            # recv damage total
        if var.fixtureB.body.bullet == True:
            if var.fixtureB.body not in self.borrar:
                self.borrar.append(var.fixtureB.body)

        #var.fixtureA.body #golpea
        #var.fixtureB.body #recibe

    def Add(self, point):
        """Called when a contact point is created"""
        print "Add:", point
    def Persist(self, point):
        """Called when a contact point persists for more than a time step"""
        print "Persist:", point
    def Remove(self, point):
        """Called when a contact point is removed"""
        print "Remove:",point
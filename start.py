from __future__ import division
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from clases.player import player
from clases.chunk import chunk
from clases.disparos import disparos
from clases.asteroids import asteroids
from clases.myContactListener import myContactListener
from clases.myDestructionListener import myDestructionListener
from PIL.Image import open
import sys
from Box2D import *
import pygame


resolution = [1600,800]
radians = 0
last_time = time.time()
t_delta = 0
fps = 0
lastFPS = 0
animate = 0.0
lastFrame = time.time()
test = 0.0
wasd = [0,0,0,0,0,[0,0,0]]
Lchunk = []
size_tile = 0.16
calculate_size = size_tile
v_object_select = [0,0]
borrar = []
textures = []
bullet = []
joints = []

zoom = 3.0


# Create a dynamic body at (0,4)


#body.fixedRotation = True


timeStep = 1.0 / 160
vel_iters, pos_iters = 6, 2

def enable_vsync():
    pass
    #glEnable(GL_VSYNC)
        # set v to 1 to enable vsync, 0 to disable vsync


def loadImage(imageName):
    im = open(imageName)
    try:
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
    except SystemError:
        ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)
    ID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, ID)
    glPixelStorei(GL_UNPACK_ALIGNMENT,4)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image
    )
    return ID

def create_camera():
    glRotate(0, 0, 0, 0)
    glRotate(0, 1, 0, 0)
    glRotate(0, 0, 0, 1)
    camera = player.get_position()[0]
    glTranslatef( -camera[0] , -camera[1], 0);

def ControlRatonPos(x,y):
    global radians
    radians = (math.atan2(-((resolution[1]/2)-y), (resolution[0]/2)-x)+ 3.14159266)

def ControlRaton(key,leave,x,y):
    global wasd
    global zoom
    if key <= 2 :
        ControlRatonPos(x,y)
        wasd[5][key] = not leave
    if (key == 3):
        zoom -= 0.08
        reshapeFun(resolution[0], resolution[1])
    if (key == 4):
        zoom += 0.08
        reshapeFun(resolution[0], resolution[1])

def ControlTeclado(key,x,y):
    global wasd
    global radians
    if (key == "w"):
        wasd[0] = 1
    if (key == "a"):
        wasd[1] = 1
    if (key == "s"):
        wasd[2] = 1
    if (key == "d"):
        wasd[3] = 1
    if (key == "q"):
        wasd[4] = 1

def object_select():
    v_object_select[0] = int((player.get_position()[0][0]+0.16) * 3.125)
    v_object_select[1] = int((player.get_position()[0][1]+0.16) * 3.125)
    tmp = math.degrees(radians)
    #print tmp
    #90 top
    if tmp > 0 and tmp < 45:
        v_object_select[1] += 1
        v_object_select[0] += 1
        #print "right top"
    if tmp > 45 and tmp < 90:
        v_object_select[1] += 1
        #print "top"
    if tmp > 90 and tmp < 135:
        v_object_select[1] += 1
        v_object_select[0] -= 1
        #print "left top"
    if tmp > 135 and tmp < 180:
        v_object_select[0] -= 1
        #print "left"
    if tmp > 180 and tmp < 225:
        v_object_select[1] -= 1
        v_object_select[0] -= 1
        #print "left bottom"
    if tmp > 225 and tmp < 270:
        v_object_select[1] -= 1
        #print "bottom"
    if tmp > 270 and tmp < 315:
        v_object_select[1] -= 1
        v_object_select[0] += 1
        #print "right bottom"
    if tmp > 315 and tmp < 360:
        v_object_select[0] += 1
        #print "right"



def ControlTecladoUp(key,x,y):
    global wasd
    if (key == "w"):
        wasd[0] = 0
    if (key == "a"):
        wasd[1] = 0
    if (key == "s"):
        wasd[2] = 0
    if (key == "d"):
        wasd[3] = 0
    if (key == "q"):
        wasd[4] = 0

def clear_objects(var):
    if (var == 2):
        for taa in borrar:
            borrar.remove(taa)
            world.DestroyBody(taa)
            bullet.remove(taa.userData)

    else:

        #clear fire idle
        for taa in list(bullet):
            if taa.awake() == False or taa.get_position()[0][1] < 0:
                print "awake: "+ str(taa.awake())
                print "pos" +str(taa.get_position()[0][1])
                world.DestroyBody(taa.get_body())
                bullet.remove(taa)
        glutTimerFunc(1000,clear_objects, 1)

def joint_check():
    for taa in joints:
        if (abs(taa.GetReactionForce(timeStep)[0])+abs(taa.GetReactionForce(timeStep)[1]) > 0.010):
            world.DestroyJoint(taa)
            joints.remove(taa)

def update():
    updateFPS()
    global timeStep
    global t_delta
    t_delta = getDelta()
    timeStep = t_delta*0.0004
    world.Step(timeStep, vel_iters, pos_iters)
    world.ClearForces()
    clear_objects(2)
    object_select()
    #joint_check()
    Lchunk[0].pick_object(player.get_position())

    player.move(wasd, t_delta, radians)

def initFun():
    print "initFun"
    glEnable(GL_AUTO_NORMAL)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)
    glClearColor(0.0,0.0,0.0,0.0)
    #reshapeFun(resolution[0],resolution[1])
    ### load textures and initial chunk
    global textures
    global Lchunk
    global player
    global world
    textures.append(loadImage('assets/stGrid1.png'))
    textures.append(loadImage('assets/player.png'))
    textures.append(loadImage('assets/bullet.png'))
    textures.append(loadImage('assets/stGriddeco.png'))

    player = player(bullet, joints, borrar)
    myListener = myContactListener(borrar, player)
    myDestructor = myDestructionListener()
    world=b2World(contactListener=myListener, destructorListener=myDestructor) # default gravity is (0,-10) and doSleep is True
    world.gravity = (0, 0)
    player.set_world(world)
    Lchunk.append(chunk(0,0, world))
    enable_vsync()

    pygame.mixer.init()
    music('a')
def music(file):

    pygame.mixer.music.load("assets/test.wav")
    pygame.mixer.music.play()

def sound(file):
    sound = pygame.mixer.Sound("assets/test.wav")
    sound.play()

def reshapeFun(wi,he):
    global resolution
    resolution = [wi,he]
    aspect = 1.9
    aspect = resolution[0] / resolution[1]
    glViewport(0, 0, wi, he)
    print "inv: " + str(aspect)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if (aspect >= 1.0):
        print wi, he
        print aspect
        glOrtho(-zoom * aspect, zoom * aspect, -zoom, zoom, -zoom, zoom)
    else:
        print "wtf"
        glOrtho(-zoom, zoom, -zoom / aspect, zoom / aspect, -zoom, zoom)
    glMatrixMode(GL_MODELVIEW)
    #glMatrixMode(GL_MODELVIEW);

    #if w>h:
    #    glViewport((w-h)/2,0,h,h)
    #else:
    #    glViewport(0,(h-w)/2,w,w)

def setupTexture(imageID):
    glEnable(GL_TEXTURE_2D)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glBindTexture(GL_TEXTURE_2D, textures[imageID])
    #texCoordsFrame1 = [0.32]
    #glTexCoordPointer(2, GL_FLOAT, 0, textures[imageID])
    #glTexCoordPointer(2, GL_FLOAT, 1000, 1000)
def new_frame(init):
    if init == True:
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glLoadIdentity()
        glTranslatef(0.0625*int(animate),0.0,0.0)
    else:
        glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def RenderGLFun():

    update()
    #---- Init Experimental zone ----
    global animate
    animate +=t_delta/60
    if animate < 16:
        animate = 0.0
    #---- End Experimental zone ----
    #Init Frame
    glClearColor(0.0,0.0,0.0,0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    create_camera()

    #draw time (optional)

    setupTexture(0)
    Lchunk[0].draw_static()
    setupTexture(3)
    Lchunk[0].draw_decoration()

    new_frame(True)
    Lchunk[0].draw_items(player.get_position())
    new_frame(False)
    Lchunk[0].draw_dynamics(player.get_position())
    setupTexture(1)
    player.draw(radians) #components.py:31 opengl
    setupTexture(2)
    for taa in list(bullet):
        taa.draw()
    draw_select()
    #go to gpu
    glutSwapBuffers()

def draw_select():
    tile = 2
    size_tile = 0.32
    #v_object_select = player.get_position()[0]
    #print v_object_select
    bx = (v_object_select[0] * size_tile)
    by = (v_object_select[1] * size_tile)

    texture_info_temp = [int(tile), 0];
    textureXOffset = float(texture_info_temp[0]/16.0)+0.001
    textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
    textureHeight  = float(0.060)
    textureWidth   = float(0.060)

    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(bx-(size_tile/2), by-(size_tile/2), 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(bx + (size_tile/2), by-(size_tile/2), 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f(bx + (size_tile/2), by+(size_tile/2), 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(bx-(size_tile/2),by+(size_tile/2), 0)

    glEnd()
def getDelta():
    global lastFrame
    #time = 7.000.000
    time = getTime()
    delta = float(time - lastFrame)
    lastFrame = time
    return delta

def getTime():
    return (time.time() * 1000)

def updateFPS():
    global fps
    global last_time
    fps += 1
    if time.time() - last_time >= 1:
        current_fps = fps / (time.time() - last_time)
        print current_fps, 'fps'
        fps = 0
        last_time = time.time()
        #print last_time

if __name__ == '__main__':
    getDelta()
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(resolution[0],resolution[1])
    glutCreateWindow("DesmadreTeam")

    #glutSpecialFunc(ControlFlechas)

    #glutSpecialUpFunc(ControlFlechasUp)
    #glutTimerFunc(16,update, 1)
    #glutTimerFunc(1000,clear_objects, 1)
    glutDisplayFunc(RenderGLFun)
    glutIdleFunc(RenderGLFun)
    glutReshapeFunc(reshapeFun)
    glutKeyboardFunc(ControlTeclado)
    glutKeyboardUpFunc(ControlTecladoUp)
    glutMouseFunc(ControlRaton)
    glutPassiveMotionFunc(ControlRatonPos)
    glutMotionFunc(ControlRatonPos)
    initFun()
    glutMainLoop()
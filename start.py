from __future__ import division
import time

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from clases.player import player
from clases.tren import tren
from clases.civil import civil
from clases.chunk import chunk
from clases.disparos import disparos
from clases.asteroids import asteroids
from clases.myContactListener import myContactListener
from clases.myDestructionListener import myDestructionListener
from PIL.Image import open
import sys
from Box2D import *
import clases.audio
from random import randint

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
status_global = 0
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
    glTranslate( -camera[0] , -camera[1], 0)

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
        print int(v_object_select[0]),int(v_object_select[1])
        Lchunk[0].set_object(v_object_select, 496)
        wasd[4] = 1

def object_select():
    v_object_select[0] = int((player.get_position()[0][0]+0.16) * 3.125)
    v_object_select[1] = int((player.get_position()[0][1]+0.16) * 3.125)
    #tmp = math.degrees(radians)
    #position = (player.get_position()[0][0]+(math.cos(radians)*0.5),player.get_position()[0][1]+(math.sin(radians)*0.5))
    #print "init"
    #print v_object_select
    #v_object_select[0] = int((position[0]+0.16) * 3.125)
    #v_object_select[1] = int((position[1]+0.16) * 3.125)
    #print tmp
    #90 top
    #if tmp > 0 and tmp < 45:
    #    v_object_select[1] += 1
    #    v_object_select[0] += 1
    #    #print "right top"
    #if tmp > 45 and tmp < 90:
    #    v_object_select[1] += 1
    #    #print "top"
    #if tmp > 90 and tmp < 135:
    #    v_object_select[1] += 1
    #    v_object_select[0] -= 1
    #    #print "left top"
    #if tmp > 135 and tmp < 180:
    #    v_object_select[0] -= 1
    #    #print "left"
    #if tmp > 180 and tmp < 225:
    #    v_object_select[1] -= 1
    #    v_object_select[0] -= 1
    #    #print "left bottom"
    #if tmp > 225 and tmp < 270:
    #    v_object_select[1] -= 1
    #    #print "bottom"
    #if tmp > 270 and tmp < 315:
    #    v_object_select[1] -= 1
    #    v_object_select[0] += 1
    #    #print "right bottom"
    #if tmp > 315 and tmp < 360:
    #    v_object_select[0] += 1
    #    #print "right"



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
            if taa.awake() == False:
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
    #draw posible options
    #draw_posible_options()
    #tmp = Lchunk[0].pick_object(v_object_select)
    #if tmp != False:
    #    print tmp
    #    player.add_hp(2.0)
    #print trenecito.get_position
    if (int(trenecito.get_position()[0][1]) == 4):
        if (len(civiles) < 1):
            generar_civiles()
    player.move(wasd, t_delta, radians)

def draw_posible_options():
    Lchunk[0].check_object(v_object_select)

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
    global civiles
    global civiles_muertos
    global civiles_muertos_DL
    global total_kills
    global last_kill
    global trenecito

    last_kill = [-1,-1]

    total_kills = 0
    civiles_muertos_DL = glGenLists(9)
    civiles = []
    civiles_muertos = []
    clases.audio.stationMusic(0)

    textures.append(loadImage('assets/stGrid1.png'))
    textures.append(loadImage('assets/player.png'))
    textures.append(loadImage('assets/bullet.png'))
    textures.append(loadImage('assets/stGriddeco.png'))
    textures.append(loadImage('assets/icons.png'))
    textures.append(loadImage('assets/tren_1.png'))
    textures.append(loadImage('assets/inicio.png'))
    textures.append(loadImage('assets/gameover.png'))
    textures.append(loadImage('assets/frases1.png'))

    player = player(bullet, joints, borrar)
    myListener = myContactListener(borrar, player)
    myDestructor = myDestructionListener()
    world=b2World(contactListener=myListener, destructorListener=myDestructor) # default gravity is (0,-10) and doSleep is True
    world.gravity = (0, 0)
    player.set_world(world)
    trenecito = tren([115,29], world, bullet)
    Lchunk.append(chunk(0,0, world))
    enable_vsync()
    getDelta()

def draw_pantallazo(num):
    setupTexture(num)
    texture_info_temp = 2
    textureXOffset = 1
    textureYOffset = 1
    textureHeight  = 1
    textureWidth   = 1

    #glTranslatef( self.body.position[0] , self.body.position[1], 0.00)
    glClearColor(0.0,0.0,0.0,0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glRotate(0, 0, 0, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)

    glVertex3f(-zoom, -zoom, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(zoom, -zoom, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f( zoom,  zoom, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-zoom, zoom, 0)
    glEnd()
    glRotate(0, 0, 0, -1)
    #glTranslatef( -self.body.position[0] , -self.body.position[1], 0.00)

def generar_civiles():
    for i in range(1):
        civiles.append(civil([18,7],world, i * 16, player, bullet, Lchunk))


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

        glTranslatef(0.0625*int(animate),0.0,0.0)
    else:
        #glMatrixMode(GL_TEXTURE)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

def RenderGLFun():
    global status_global
    if status_global == 0 or status_global == 3:
        getDelta()
        glClearColor(0.0,0.0,0.0,0.0)
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()
        glPushMatrix()
        glLoadIdentity()
        if status_global == 0:
            draw_pantallazo(6)
        else:
            draw_pantallazo(7)
        glPopMatrix()
        glutSwapBuffers()
        if (wasd[0] == True):

            status_global = 1
    #pepito
    elif status_global == 1:
        update()
        #---- Init Experimental zone ----
        global animate
        animate +=float(t_delta)/60.0
        if animate > 16:
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
        draw_civils()
        player.draw(radians, animate, wasd) #components.py:31 opengl
        setupTexture(2)
        for taa in list(bullet):
            taa.draw()
        setupTexture(5)
        trenecito.draw(t_delta)
        #GUI
        #
        setupTexture(1)
        glPushMatrix()
        glLoadIdentity()

        draw_caretos()
        setupTexture(4)
        draw_kills()
        setupTexture(3)
        draw_heals()
        draw_frases()
        glPopMatrix()
        #draw_select()
        #go to gpu
        glutSwapBuffers()

def draw_frases():
    #64 frases
    #0.015625
    setupTexture(8)
    texture_info_temp = 2
    textureXOffset = 1
    textureYOffset = last_kill[1]*0.015625
    textureHeight  = 0.015625
    textureWidth   = 1

    glTranslatef(-0.5,-2.7, 0)
    glRotate(0, 0, 0, 1)
    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(-1.8, -0.2, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(1.8, -0.2, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f( 1.8,  0.2, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-1.8, 0.2, 0)
    glEnd()
    glRotate(0, 0, 0, -1)
    glTranslatef(0.5,2.7, 0)

def draw_heals():
    tmp = 0
    hp = player.get_damage()
    if hp > 0.0:
        for a in range(int(hp)):
            tmp += 0.2
            draw_heal(tmp)
    else:
        global status_global
        status_global = 3
def draw_heal(bxs):

    tile = 82
    size_tile = 0.08
    #v_object_select = player.get_position()[0]
    #print v_object_select
    bx = zoom - bxs
    by = zoom-0.2

    texture_info_temp = [int(tile), 0];
    textureXOffset = float(texture_info_temp[0]/16.0)+0.001
    textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
    textureHeight  = float(0.060)
    textureWidth   = float(0.060)
    glTranslatef(bx,by, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(-0.1, -0.1, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(+0.1, -0.1, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f(+0.1, +0.1, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-0.1, + 0.1, 0)

    glEnd()
    glTranslatef(-bx,-by, 0)

def draw_kills():
    tmp = str(total_kills)
    tmp_len = len(tmp)
    if(tmp_len != 4):
        for a in range(4-tmp_len):
            tmp =  "0" + str(tmp)
    draw_kill(0.2, tmp[3])
    draw_kill(0.6, tmp[2])
    draw_kill(1.0, tmp[1])
    draw_kill(1.4, tmp[0])

def draw_kill(bxs,numerito):

    tile = int(numerito)+14
    size_tile = 0.16
    #v_object_select = player.get_position()[0]
    #print v_object_select
    bx = zoom - bxs
    by = -zoom+0.3

    texture_info_temp = [int(tile), 0];
    textureXOffset = float(texture_info_temp[0]/16.0)+0.001
    textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
    textureHeight  = float(0.060)
    textureWidth   = float(0.060)
    glTranslatef(bx,by, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(-0.2, -0.2, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(+0.2, -0.2, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f(+0.2, +0.2, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-0.2, + 0.2, 0)

    glEnd()
    glTranslatef(-bx,-by, 0)

def draw_caretos():

    tile = last_kill[0]
    size_tile = 0.32
    #v_object_select = player.get_position()[0]
    #print v_object_select
    bx = -zoom+0.2
    by = -zoom+0.2

    texture_info_temp = [int(tile), 0];
    textureXOffset = float(texture_info_temp[0]/16.0)+0.001
    textureYOffset = float(16 - int(texture_info_temp[0]/16)/16.0)-0.001
    textureHeight  = float(0.060)
    textureWidth   = float(0.060)
    glTranslatef(bx,by, 0)
    glBegin(GL_QUADS)
    glTexCoord2f(textureXOffset, textureYOffset - textureHeight)
    glVertex3f(-0.2, -0.2, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset - textureHeight)
    glVertex3f(+0.2, -0.2, 0)

    glTexCoord2f(textureXOffset + textureWidth, textureYOffset)
    glVertex3f(+0.2, +0.2, 0)

    glTexCoord2f(textureXOffset,textureYOffset)
    glVertex3f(-0.2, + 0.2, 0)

    glEnd()
    glTranslatef(-bx,-by, 0)
def draw_civils():
    tmp = False

    for taa in list(civiles):
        if (taa.get_normal() == True):
            taa.draw(t_delta, animate)
        else:
            tmp = True
            global total_kills
            global last_kill
            total_kills += 1
            print "total kills: " + str(total_kills)
            last_kill[0] = taa.get_tileid()+14
            last_kill[1] = randint(0,64)
            civiles_muertos.append(taa)
            civiles.remove(taa)
    if (tmp == True):
        glNewList(civiles_muertos_DL, GL_COMPILE)
        for taa in list(civiles_muertos):
            setupTexture(3)
            taa.draw_sangre()
            setupTexture(1)
            taa.draw(0,animate)
        glEndList()
    glCallList(civiles_muertos_DL)


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
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(resolution[0],resolution[1])
    glutCreateWindow("DesmadreTeam")

    #glutSpecialFunc(ControlFlechas)

    #glutSpecialUpFunc(ControlFlechasUp)
    #glutTimerFunc(16,update, 1)
    glutTimerFunc(1000,clear_objects, 1)
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
#!/usr/bin/env python3

import OpenGL.GL as GL
import glfw
import pyrr
from cpe3d import Object3D
from cpe3d import Text





class ViewerGL:
    def __init__(self):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(1280, 720, 'OpenGL', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)
        # choix de la couleur de fond
        GL.glClearColor(0.1, 0.2, 0.9, 1.0)
        print(f"OpenGL: {GL.glGetString(GL.GL_VERSION).decode('ascii')}")

        self.objs = []
        self.touch = {}
        self.tframe = glfw.get_time()
        self.dt = 0
        self.gravité = 30
        self.vitesse1 = pyrr.vector3.Vector3([0.0, 0.0, 0.0])
        self.vitesse0 = pyrr.vector3.Vector3([0.0, 0.0, 0.0])
        self.acceleration = pyrr.vector3.Vector3([0.0, - self.gravité, 0.0])
        self.clavier_enable = False


    def run(self):
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            # jump des stego
            self.dt = glfw.get_time() - self.tframe
            self.tframe = glfw.get_time()
            
            
            if self.objs[0].transformation.translation.y > self.objs[2].transformation.translation.y + 1:
                self.vitesse0 += self.acceleration * self.dt
                self.objs[0].transformation.translation += self.vitesse0 * self.dt
            if self.objs[1].transformation.translation.y > self.objs[2].transformation.translation.y + 1:
                self.vitesse1 += self.acceleration * self.dt
                self.objs[1].transformation.translation += self.vitesse1 * self.dt

            if self.clavier_enable:
                self.update_key()

            diff = self.objs[1].transformation.translation-self.objs[0].transformation.translation
            dist = pyrr.vector.length(diff)
            
            if  dist < 1.5:
                self.objs[0].transformation.translation = self.objs[1].transformation.translation - 1.5 * diff/dist
                
            
            #collision avec sol  
            if self.objs[0].transformation.translation.y < self.objs[2].transformation.translation.y + 1:
                self.objs[0].transformation.translation.y = self.objs[2].transformation.translation.y + 1
                
            if self.objs[1].transformation.translation.y < self.objs[2].transformation.translation.y + 1:
                self.objs[1].transformation.translation.y = self.objs[2].transformation.translation.y + 1 
            
            
                
            #déplacement de la flèche
            self.objs[3].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[3].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.03]))


            for obj in self.objs:
                #print(obj)
                if obj != -1:
                    GL.glUseProgram(obj.program)
                    if isinstance(obj, Object3D):
                        self.update_camera(obj.program)
                    obj.draw()
                if isinstance(obj, Text) and glfw.get_time() > 5:
                    self.objs.remove(obj)
                    self.clavier_enable = True
            
            #tentative de gestion de l'apparition des flèches
            #if self.objs[2].id == 0:
            #    self.objs[2].transformation.translation += \
            #        pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[2].transformation.rotation_euler), pyrr.Vector3([0, 0.02, 0]))
            
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
        
    def key_callback(self, win, key, scancode, action, mods):
        # sortie du programme si appui sur la touche 'échappement'
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            print('arrêt du jeu')
            glfw.set_window_should_close(win, glfw.TRUE)
        self.touch[key] = action

        #début du jump
        if key == glfw.KEY_V and action == glfw.PRESS and self.objs[0].transformation.translation.y == self.objs[2].transformation.translation.y + 1:
            self.vitesse0 = pyrr.Vector3([0.0, 15.0, 0.0])

        if key == glfw.KEY_SPACE and action == glfw.PRESS and self.objs[1].transformation.translation.y == self.objs[2].transformation.translation.y + 1:
            self.vitesse1 = pyrr.Vector3([0.0, 15.0, 0.0])


    
    def add_object(self, obj):
        self.objs.append(obj)

    def remove_object(self, obj):
        self.objs.remove(obj)

    def set_camera(self, cam):
        self.cam = cam
    
    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)
        

    def update_key(self):

        #deplacement du premier stego
        if glfw.KEY_UP in self.touch and self.touch[glfw.KEY_UP] > 0:
            self.objs[0].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.03]))
        if glfw.KEY_DOWN in self.touch and self.touch[glfw.KEY_DOWN] > 0:
            self.objs[0].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.03]))
        if glfw.KEY_LEFT in self.touch and self.touch[glfw.KEY_LEFT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.05
        if glfw.KEY_RIGHT in self.touch and self.touch[glfw.KEY_RIGHT] > 0:
            self.objs[0].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.05

        #deplacement du deuxieme stego
        if glfw.KEY_W in self.touch and self.touch[glfw.KEY_W] > 0:
            self.objs[1].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.03]))
        if glfw.KEY_S in self.touch and self.touch[glfw.KEY_S] > 0:
            self.objs[1].transformation.translation -= \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[1].transformation.rotation_euler), pyrr.Vector3([0, 0, 0.03]))
        if glfw.KEY_A in self.touch and self.touch[glfw.KEY_A] > 0:
            self.objs[1].transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.05
        if glfw.KEY_D in self.touch and self.touch[glfw.KEY_D] > 0:
            self.objs[1].transformation.rotation_euler[pyrr.euler.index().yaw] += 0.05

        #mouvement de camera
        if glfw.KEY_I in self.touch and self.touch[glfw.KEY_I] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] -= 0.1
        if glfw.KEY_K in self.touch and self.touch[glfw.KEY_K] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().roll] += 0.1
        if glfw.KEY_J in self.touch and self.touch[glfw.KEY_J] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] -= 0.1
        if glfw.KEY_L in self.touch and self.touch[glfw.KEY_L] > 0:
            self.cam.transformation.rotation_euler[pyrr.euler.index().yaw] += 0.1

        #jump
        if glfw.KEY_V in self.touch and self.touch[glfw.KEY_V] > 0:
            self.objs[0].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0.02, 0]))
        if glfw.KEY_SPACE in self.touch and self.touch[glfw.KEY_SPACE] > 0:
            self.objs[1].transformation.translation += \
                pyrr.matrix33.apply_to_vector(pyrr.matrix33.create_from_eulers(self.objs[0].transformation.rotation_euler), pyrr.Vector3([0, 0.02, 0]))


import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr


class Arrows(Object3D):
    def __init__(self,id):
        self.id = id
        self.mesh = Mesh.load_obj('arrow.obj')
        self.mesh.normalize()
        self.mesh.apply_matrix(pyrr.matrix44.create_from_scale([1, 1, 1, 1]))
        self.tr = Transformation3D()
        self.tr.translation.y = -np.amin(self.mesh.vertices, axis=0)[1]
        if id == 0: #gauche
            self.tr.translation.x = -10
            self.tr.translation.z = 0
            self.tr.rotation_center.y = -90
        if id == 1: #droite
            self.tr.translation.x = 10
            self.tr.translation.z = 0
            self.tr.rotation_center.y = 90
        if id == 2: #devant
            self.tr.translation.x = 0
            self.tr.translation.z = -10
            self.tr.rotation_center.y = 0
        if id == 3: #derriere
            self.tr.translation.x = 0
            self.tr.translation.z = 10
            self.tr.rotation_center.y = 180
    
    def setTexture(self, texture):
        self.texture = texture = glutils.load_texture(texture)
        
    def loadObject(self,program3d_id):
        o1 = Object3D(self.mesh.load_to_gpu(), self.mesh.get_nb_triangles(), program3d_id, self.texture, self.tr)
        return o1
    
    

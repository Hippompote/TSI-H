import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

class level(Object3D):
    def __init__(self):
        self.mesh = Mesh.load_obj('Level.obj')
        self.mesh.normalize()
        self.mesh.apply_matrix(pyrr.matrix44.create_from_scale([4, 4, 4, 1]))
        self.tr = Transformation3D()
        self.tr.translation.y = -np.amin(self.mesh.vertices, axis=0)[1]
        self.tr.translation.z = 0 
        self.tr.rotation_center.z = 0.2
    
    def setTexture(self, texture):
        self.texture = texture = glutils.load_texture(texture)
        
    def loadObject(self,program3d_id):
        o1 = Object3D(self.mesh.load_to_gpu(), self.mesh.get_nb_triangles(), program3d_id, self.texture, self.tr)
        return o1
    

    def calculate_dimensions(self):
        vertices = self.mesh.vertices
        max_x = np.amax(vertices[:, 0])  # Maximum x-coordinate
        min_x = np.amin(vertices[:, 0])  # Minimum x-coordinate
        self.length = max_x - min_x

        max_y = np.amax(vertices[:, 1])  # Maximum y-coordinate
        min_y = np.amin(vertices[:, 1])  # Minimum y-coordinate
        self.width = max_y - min_y
        return self.length, self.width
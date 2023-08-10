import glutils
from mesh import Mesh
from cpe3d import Object3D, Transformation3D
import numpy as np
import pyrr

class Players(Object3D):
    def __init__(self,x,z):
        self.mesh = Mesh.load_obj('stegosaurus.obj')
        self.mesh.normalize()
        self.mesh.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
        self.tr = Transformation3D()
        self.tr.translation.y = -np.amin(self.mesh.vertices, axis=0)[1]
        self.tr.translation.x = x
        self.tr.translation.z = z
        self.tr.rotation_center.z = 0.2


    
    def setTexture(self, texture):
        self.texture = texture = glutils.load_texture(texture)
        
    def loadObject(self,program3d_id):
        o1 = Object3D(self.mesh.load_to_gpu(), self.mesh.get_nb_triangles(), program3d_id, self.texture, self.tr)
        return o1
        
        """
    def get_mesh_height(self):
        mesh = self.mesh
        vertices = mesh.vertices
        max_y = np.amax(vertices[:, 1])
        min_y = np.amin(vertices[:, 1])
        height = max_y - min_y
        return height
        """
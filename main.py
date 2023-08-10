from viewerGL import ViewerGL
import glutils
from cpe3d import Camera,  Text
import numpy as np
import pyrr
import players
import level
import arrows
import random
import sounddevice as sd
import soundfile as sf

def play():
    data, samplerate = sf.read('music.wav')
    sd.play(data, samplerate)
    
def main():
   
   #lance la musique
    play()
    
    viewer = ViewerGL()

    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 7
    viewer.cam.transformation.translation.z = 20
    viewer.cam.transformation.rotation_euler[pyrr.euler.index().roll] = 44.5

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')

    #initialisation carl
    ca = players.Players(3,0)
    ca.setTexture('stegosaurus.jpg')
    cao = ca.loadObject(program3d_id)
    viewer.add_object(cao)

    #initialisation carlos
    cs = players.Players(-3,0)
    cs.setTexture('stegosaurus.jpg')
    cso = cs.loadObject(program3d_id)
    viewer.add_object(cso)

    #initialisation sol
    l = level.level()
    l.setTexture('grass.jpg')
    lo = l.loadObject(program3d_id)
    viewer.add_object(lo)
    
    #initialisation arrows
    lstArrows = []
    for i in range(3):
        lstArrows.append([arrows.Arrows(i),i])
    
    a = random.choice(lstArrows)
    a[0].setTexture('grass.jpg')
    ao = a[0].loadObject(program3d_id)
    viewer.add_object(ao)

    #initialisation text
    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    txt = Text('Carl & Carlos REVOLUTION', np.array([-0.8, 0.3], np.float32), np.array([0.8, 0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(txt)
    
    viewer.run()

if __name__ == '__main__':
    main()
# WARNING : only run this from within the blender file!

import bpy
import math
import mathutils

if bpy.context.view_layer.objects.active.mode != 'OBJECT':
    bpy.ops.object.mode_set(mode='OBJECT')
    

cam = bpy.data.objects['Camera']
bpy.context.view_layer.objects.active = cam

frame = 1

(delta_y, y, ymax) = (.1, -1, 3)

n_rotations_per_position = 8

print('[start] ------------------')

while (y < ymax) :
    for i in range(n_rotations_per_position) :
        cam.location = (0,y,1)
        cam.rotation_euler = (math.radians(80), 0, 2*i*math.pi/n_rotations_per_position)
        
        cam.keyframe_insert(data_path="location", index=-1)
        cam.keyframe_insert(data_path="rotation_euler", index=-1)
        
        rot = cam.rotation_euler.copy()
        rot.order = 'ZXY'
        
        pos = cam.location.copy()
        pos.z = -pos.z
        
        R = rot.to_matrix()
        q = rot.to_quaternion()

        t = -pos
        t.rotate(R)
        
        print(f'{frame} {q.w:.6f} {q.x:.6f} {q.y:.6f} {q.z:.6f} {t.x:.6f} {t.y:.6f} {t.z:.6f} 1 {frame:04d}.jpg\n')
        frame += 1
        
    y += delta_y
        
print('[done] ------------------')
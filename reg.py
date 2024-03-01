
from .format import abc,bvh,dae,fbx,gltf,mmd,obj,ply,stl,svg,usd,vrm,x3d,max3ds
from . import prop,ops
files = [
    ops,
    abc,bvh,dae,fbx,gltf,mmd,obj,ply,stl,svg,usd,vrm,x3d,max3ds,
]
def register():
    prop.register()
    for f in files:
        f.register()



def unregister():
    for f in files:
        f.unregister()

    prop.unregister()

# importing libraries doesn't work in freecad scripts



import FreeCAD
import Mesh
import MeshPart




def makePart(dstName, srcObjects, flipNormals):
    doc = FreeCAD.activeDocument()
    guiDoc = FreeCAD.Gui.activeDocument()
    dsts = []
    for i in srcObjects:
        mesh = doc.addObject("Mesh::Feature","Mesh")
        src = doc.getObject(i)
        shape = src.Shape
        #mesh.Mesh = MeshPart.meshFromShape(Shape=shape,MaxLength=250.8)
        mesh.Mesh = MeshPart.meshFromShape(Shape=shape,LinearDeflection=10, AngularDeflection=0.523599, Relative=False)

        if i in flipNormals:
            mesh.Mesh.flipNormals()
        mesh.Label = "%s Mesh" % i
        mesh.ViewObject.CreaseAngle=25.0
        dsts.append(mesh)
        guiDoc.getObject(i).Visibility=False

    part = FreeCAD.App.activeDocument().addObject('App::Part','Part')
    part.Label = dstName
    for i in dsts:
        part.addObject(i)
    return part




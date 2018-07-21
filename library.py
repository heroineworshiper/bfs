# importing libraries doesn't work in freecad scripts


import FreeCAD
import FreeCADGui
import Mesh
import MeshPart



doc = FreeCAD.ActiveDocument



def isPart(x):
    return str(type(x)) == '<type \'App.Part\'>'

# convert an App.Part to a mesh
def makePartPart(dsts, transform, part, doubleSided, flipNormals):
    transform = transform * part.Placement.toMatrix()
    for src in part.Group:
        if src.ViewObject.Visibility:
            if isPart(src):
                makePartPart(dsts, transform, src, doubleSided, flipNormals)
            else:
                makePolyPart(dsts, transform, src, doubleSided, flipNormals)
    #src.ViewObject.Visibility=False



# convert a polygon to a mesh
def makePolyPart(dsts, transform, src, doubleSided, flipNormals):
    #print "got it"
    mesh = doc.addObject("Mesh::Feature","Mesh")
    shape = src.Shape
    #mesh.Mesh = MeshPart.meshFromShape(Shape=shape,MaxLength=250.8)
    mesh.Mesh = MeshPart.meshFromShape(Shape=shape,LinearDeflection=10, AngularDeflection=0.523599, Relative=False)

    if src.Label in flipNormals:
        mesh.Mesh.flipNormals()
    if src.Label in doubleSided:
        mesh.ViewObject.Lighting = u"Two side"
        
    mesh.Label = "%s Mesh" % src.Label
    mesh.ViewObject.CreaseAngle=25.0
    mesh.Placement = App.Placement(transform)
    dsts.append(mesh)
    src.ViewObject.Visibility=False





def makePart(dstName, objects, doubleSided, flipNormals):
    dsts = []
    for src in doc.Objects:
        if src.Label in objects:
            transform = App.Matrix()
            print 'label=%s name=%s' % (src.Label, src.Name)
            if isPart(src):
                makePartPart(dsts, transform, src, doubleSided, flipNormals)
            else:
                makePolyPart(dsts, transform, src, doubleSided, flipNormals)
                
                
        

    part = App.activeDocument().addObject('App::Part','Part')
    part.Label = dstName
    for i in dsts:
        part.addObject(i)
    return part





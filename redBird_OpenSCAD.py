# Author: Yang XU <yang.xu@connect.ust.hk>
# LICENSE: MIT
import numpy as np
from solid import *
from solid.utils import *


def genRedBirdBodyPoints(targetHeight):
    points = np.genfromtxt("redBird_body_points.csv", delimiter=",")
    groundPointIndex = np.where(points == np.min(points[:, 1]))[0][0]
    groundPointXDistance = points[groundPointIndex][0]
    Xmax = max(points[:, 0])
    Xmin = min(points[:, 0])
    Ymax = max(points[:, 1])
    Ymin = min(points[:, 1])
    width = Xmax - Xmin
    height = Ymax - Ymin
    scaleFactor = targetHeight / height
    pointsNormalized = (points - np.array([groundPointXDistance, Ymin])) * scaleFactor
    return pointsNormalized, height/width


####################### Prepare geomoetry #######################
mm = 1
deg = 1

bodyHeight = 100*mm
startAngle = 12.5*deg
endAngle = startAngle + 27*deg

## Load points data & scale into `targetHeight` & move to the origin
pointsScaled, aspectRatio = genRedBirdBodyPoints(bodyHeight)

## Generate derivative parameters
bodyWidth = bodyHeight/aspectRatio
bodyThickness = bodyHeight/50
baseRadiusBottom = bodyWidth/2.5
baseRadiusTop = baseRadiusBottom/3
baseHeight = bodyThickness*1.1
dInterference = bodyHeight/100

##################### Generate OpenSCAD code #####################
## Generate redbird: body part
redbirdBody = polygon(pointsScaled)
redbirdBody = linear_extrude(bodyThickness)(redbirdBody)
redbirdBody = rotate(a=90, v=[1, 0, 0])(redbirdBody)
redbirdBody = translate([0, bodyThickness/2, 0])(redbirdBody)

## Generate redbird: wing part
wingSphereOuter = sphere(r=bodyWidth*0.52)
wingSphereOuter = color("green", alpha=0.7)(translate([-bodyWidth*0.01, 0, bodyWidth*0.52])(rotate(a=90, v=[1, 0, 0])((wingSphereOuter))))
wingSphereInner = sphere(r=bodyWidth*0.35)
wingSphereInner = color("blue", alpha=0.5)(translate([bodyWidth*0.07, 0, bodyWidth*0.59])(rotate(a=90, v=[1, 0, 0])((wingSphereInner))))
wingSphereInner = scale([1, 1.458, 1])(wingSphereInner)

xsecSurfaceLower = cube([bodyWidth*4, bodyWidth*4, bodyWidth])
xsecSurfaceLower = translate([-bodyWidth*2, -bodyWidth*2, 0])(xsecSurfaceLower)
xsecSurfaceLower = rotate(a = 90+startAngle, v=[0, 1, 0])(xsecSurfaceLower)
xsecSurfaceLower = translate([bodyWidth*0.07, 0, bodyWidth*0.58])(xsecSurfaceLower)
xsecSurfaceUpper = cube([bodyWidth*4, bodyWidth*4, bodyWidth])
xsecSurfaceUpper = translate([-bodyWidth*2, -bodyWidth*2, 0])(xsecSurfaceUpper)
xsecSurfaceUpper = rotate(a = 270+endAngle, v=[0, 1, 0])(xsecSurfaceUpper)
xsecSurfaceUpper = translate([bodyWidth*0.07, 0, bodyWidth*0.58])(xsecSurfaceUpper)

redbirdWing = wingSphereOuter - wingSphereInner - xsecSurfaceUpper - xsecSurfaceLower

## Generate redbird: merge into a whole redbird
redbird = color("red")(redbirdBody + redbirdWing)

## Generate supporting cylinders
baseTop = translate([0, 0, -baseHeight/2])(cylinder(r=baseRadiusTop, h=baseHeight+dInterference, center=True))
baseBottom = translate([0, 0, dInterference-baseHeight*3/2])(cylinder(r=baseRadiusBottom, h=baseHeight, center=True))
base = color("Ivory")(baseBottom + baseTop)

output = redbird + base
scad_render_to_file(output, "redBird_OpenSCAD.scad", file_header = '$fn= $preview ? 120 : 360;')

############ Please use OpenSCAD to generate 3D model ############
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Nerdfever.com personal Python library for SolidPython.

"""

__author__    = 'NerdFever.com'
__copyright__ = 'Copyright 2018-2019 NerdFever.com'
__version__   = ''
__email__     = 'dave@nerdfever.com'
__status__    = 'Development'
__license__   = """Copyright 2018-2019 NerdFever.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""


'''

Modifiers:

.set_modifier("*") # disable aka disable()
.set_modifier("!") # show only aka root()
.set_modifier("#") # highlight aka debug()
.set_modifier("%") # transparent aka background())

'''

import os, math
import numpy as np
from solid import *
from solid.utils import *
from solid import screw_thread
#from nerdlib import *

# controls number of segments in rendered circles (==$fn in OpenSCAD)
SEGMENTS = 128

''' CONSTANTS '''

ZortraxM200BuildVolume = [200, 200, 180] # x, y, z, max

# these work on Z-ABS at layer size 0.14 to 0.19 mm (at least - haven't tested enough otherwise)
# all are per side, use double for diameters

# NOTE - These work at 0.19 mm/layer, normal quality.
#        At 0.09mm/layer + high quality, they are all a little loose.

TightFit                    = 0.1875 # considerable resistance - stays put
SnugFit                     = 0.25   # virtually zero contact
LooseFit                    = 0.50
VeryLooseFit                = 0.75

# Major (outer) diameters - ref https://en.wikipedia.org/wiki/Unified_Thread_Standard
Screw_0_80_Major_Diameter   = 1.5240
Screw_1_64_Major_Diameter   = 1.8542
Screw_2_56_Major_Diameter   = 2.1844
Screw_4_40_Major_Diameter   = 2.8448
Screw_6_32_Major_Diameter   = 3.5052
Screw_10_24_Major_Diameter  = 4.8260
Screw_10_24_Drill           = 3.7973 # #25 drill

Screw_M3_Major_Diameter     = 2.93
Screw_M3_Head_Diameter      = 5.25

# Lens mounts (FFD = flange focal distance)
Pentax_Q_FFD                = 9.2
Leica_M_FFD                 = 27.8
B4_1_2inch_FFD              = 35.74     # 1/2" standard
B4_1_2inch_Sony_FFD         = 38.0      # 1/2" Sony
B4_2_3inch_FFD              = 48.0      # 2/3"
C_Mount_FFD                 = 17.526    # 0.69"
C_Mount_Diameter            = 25.4      # 1.0"
C_Mount_Threads_Per_MM      = 32/25.4   # 32.0 TPI
CS_Mount_FFD                = C_Mount_FFD - 5.0
CS_Mount_Diameter           = C_Mount_Diameter
CS_Mount_Threads_Per_MM     = C_Mount_Threads_Per_MM

def render(object, baseFilename=None, prefix="", suffix=""):
    """ Renders object, outputs to base filename with optional prefixes and suffixes added"""

    if baseFilename == None:
        import __main__ as main
        baseFilename = os.path.splitext(main.__file__)[0]

    scad_render_to_file(object, prefix+baseFilename+suffix + ".scad", file_header='$fn = %s;' % SEGMENTS, include_orig_code=True)


def ring(od, id, h, center=False):
    """
    Returns a ring (cylinder with a hole in it).
    od = outer diameter
    id = inner diameter
    h = height
    """

    if center==True:
        return cylinder(d=od, h=h, center=True) - cylinder(d=id, h=h+1, center=True)#.set_modifier("#")
    else:
        return cylinder(d=od, h=h) - down(1)(cylinder(d=id, h=h+2))#.set_modifier("#")


def squorus(wall, outer, center=False):
    """
    Creates a "squorus" (square torus; a cube with a square hole thru it).
    Argument names are optional if given in the order shown here.
    The hole is centered about the z axis. When center==True, it is also centered vertically along the z axis. (similar to "cylinder")
    As with "cube" if you give a single scalar as "outer", it will make all sides that same length.

    wall = wall thickness
    outer = tuple or list (x,y,z) of outer dimensions (or scalar) (same as "cube")
    center == False (default), squorus is in the 1st (positive) octant, one corner at (0,0,0) (same as "cube")
    center == True, squorus is centered at (0,0,0) (same as "cube")
    """

    if type(outer) not in (tuple, list):
        outer = ( outer, outer, outer )

    inner = (outer[0] - wall*2, outer[1] - wall*2, outer[2]+1) # +1 ensures hole extends past wall of outer cube (avoid z-fighting in OpenSCAD preview; https://github.com/openscad/openscad/issues/1793)

    if center:
        thing = cube(outer, center) - cube(inner, center)
    else:
        thing = cube(outer, center) - translate([wall, wall,-0.5])(cube(inner, center))

    return thing


def label(string, width=15, halign="left", valign="baseline", size=10, depth=0.5,
         lineSpacing=1.15, font="MgOpen Modata:style=Bold", segments=40):

    """Renders a multi-line string into a single 3D object."""

    lines = string.splitlines()

    texts = []

    for idx, l in enumerate(lines):

        t = text(text=l, halign=halign, valign=valign, font=font).add_param('$fn', segments)
        t = linear_extrude(height=1)(t)
        t = translate([0, -size * idx * lineSpacing, 0])(t)

        texts.append(t)

    result = union()(texts)
    result = resize([width, 0, depth])(result)
    result = translate([0, (len(lines)-1)*size / 2, 0])(result)

    return result

def thread(diameter, length, lead, tooth=None,
           toothBite=None, toothBottom=None, toothTop=None,
           external=True, starts=1, neckInDegrees=0, neckOutDegrees=0, segments=64):
    '''
    Makes an internal or external screw thread.

    diameter - of the base cylinder to which threads are referenced
    length - Z axis length of the thread (goes bottom to top)
    lead - Z distance the thread moves per turn (if starts==1, this is the pitch)
    tooth - the tooth profile (see below). if None, the default profile is used.
    toothBite - the extended radius of the tooth (from the base cylinder) [only if using default tooth profile]
    toothBottom - Z size of base of tooth [only if using default tooth profile]
    toothTop - Z size of end of tooth [only if using default tooth profile]
    external - if True makes an external thread (external to base cyldiner). Otherwise, an internal thread.
    starts - number of thread starts
    neckInDegrees - degrees used to feather bottom toothBite
    neckOutDegrees - degrees used to feather top toothBite
    segments - number of circle segments ($fs in OpenSCAD). More is smoother, but takes longer to render.

    The default thread profile will produce either a isosceles triangle profile (if tooothTop == 0),
    or an isosceles trapezoid profile (if toothTop > 0); this is a triangle with a truncated (flat) top.

    Re pitch and lead:
        pitch (Z distance between threads) == lead / starts, and,
        lead (Z distance per turn) == pitch * starts

    '''

    if tooth == None:
        # if toothTop==0, this gives a triangular thread. If toothTop>0, gives a thread with a flat (truncated) top.
        tooth = [[0,         -toothBottom / 2],
                 [toothBite, -toothTop    / 2],
                 [toothBite, +toothTop    / 2],
                 [0,         +toothBottom / 2]]

    thread = []

    for twist in np.linspace(0,360,num=starts,endpoint=False).tolist():

        start = screw_thread.thread(outline_pts=tooth,
                                inner_rad=diameter/2,
                                external=external,
                                pitch=lead,
                                length=length,
                                segments_per_rot=segments,
                                neck_in_degrees=neckInDegrees, neck_out_degrees=neckOutDegrees)

        start = rotate([0,0,twist])(start)

        thread += start

    return thread

def knurl(d, h, r=1, numKnurls=360/15, center=False):
    """
    Makes simple knurls that wrap around a cylinder in z. (Useful for control knobs or thumbscrews.)

    It places knurls on the outside a cylinder of diameter d and height h.
    Each knurl is a 90 degree corner.
    Knurls extend to an additional radius of r (resulting outside diameter is therefore d+2*r).
    d is the diamter of the base cylinder (not including knurls)
    h is the height
    r is the additional radius of each knurl (in addition the cylinder radius)
    numKnurls is the number of knurls around the cylinder (rounded up to the next multiple of 4).
    center is the same as for "cylinder" OpenSCAD primitive

    """
    knurlSide = math.sqrt((d+2*r)**2/2)

    knurl = cube([knurlSide, knurlSide, h])#.set_modifier("#")
    knurl = translate([-knurlSide/2, -knurlSide/2, 0])(knurl)

    knurls = []

    degreeStep = int(90/math.ceil(numKnurls/4))

    for deg in range(0, 90, degreeStep):
        knurls += rotate([0,0,deg])(knurl)

    knurls -= down(1)(cylinder(d=d, h=h+2))

    if center:
        knurls = down(h/2)(knurls)

    return knurls

if __name__ == '__main__':

    def main():
        offset = 0
        increment = 20
        thing = []

        def demo(d):
            nonlocal offset, thing

            thing += right(offset)(d)
            offset += increment

        demo( ring(10, 5, 2, center=False) )

        demo( ring(10, 5, 2, center=True) )

        demo( squorus(3, 10, center=False) )

        demo( squorus(3, [10, 20, 5], center=False) )

        demo( squorus(3, 10, center=True) )

        demo( squorus(3, [10, 20, 5], center=True) )

        demo ( label("""Hello\nworld!"""))

        demo( thread(diameter=5, length=10, lead=3,
                     toothBite=2,
                     toothBottom=1,
                     toothTop=1,
                     starts=2,
                     neckInDegrees=180,
                     neckOutDegrees=60,
                     external=True) )

        demo( knurl(d=5, h=3) )

        demo( knurl(d=5, h=3, center=True) )

        render(thing)

    main()
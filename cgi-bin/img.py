#!/usr/bin/env python
from PIL import Image, ImageFilter
import math, numpy

def find_coeffs(pa, pb):
	matrix = []
	for p1, p2 in zip(pa, pb):
		matrix.append([p1[0], p1[1], 1, 0, 0, 0, int(-p2[0]*p1[0]), int(-p2[0]*p1[1])])
		matrix.append([0, 0, 0, p1[0], p1[1], 1, int(-p2[1]*p1[0]), int(-p2[1]*p1[1])])

	A = numpy.matrix(matrix, dtype=numpy.float)
	B = numpy.array(pb).reshape(8)

	res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
	return numpy.array(res).reshape(8)


def getDist(A, B):	return math.hypot(B[0] - A[0], B[1] - A[1]) 
def resizeByPerc( img, perc ): return img.resize( (int(img.size[0] * perc), int(img.size[1] * perc)) )


print("Content-Type: text/html\n")

wall = Image.open("wall2.png")
outl = Image.open("outline3.png")

# these are the coords of the points on the wall to be transformed to
#wall_pts = [ (163,241), (827,138), (846, 563), (146,549) ]

#skewed version
wall_pts = [(167,227), (743,201), (849,565), (161,531)]

outl_pts = [ (33, 126), (513,50), (529,353), (24,338) ]
coeffs = find_coeffs( wall_pts, outl_pts )
outl=outl.transform( wall.size , Image.PERSPECTIVE, coeffs,
        Image.BICUBIC) #.save(sys.argv[3])

# why do we need an offset? cuz its not exact ... ?
offset=(0,0)
wall.paste(outl, offset, outl)
wall.show()


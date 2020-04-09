import  numpy as np
import argparse
import svgwrite
import sys
def updcircle(a,s,d,f,f_n, F_N):
    sys.stdout.write("\r" + str(f_n) + '/' + str(F_N))
    sys.stdout.flush()

def circle(coord,c,dwg):
    x=coord[0]
    y = coord[1]
    if c==1.:color='red'
    elif c == -1.:color = 'blue'
    else:color='white'
    dwg.add(dwg.circle((x, y), 25.13,stroke='black',stroke_width=2,fill=color))

def line(a,b,dwg):
    dwg.add(dwg.line((a[0],a[1]),(b[0],b[1]),  stroke='black', stroke_width=3 ))


def du_plot(coords_c,topo_c,allowed,fluor,N,M,name):
    coords_c=coords_c*100.
    w = ((N) * 3. - 1.) * 142.1
    h = (M - 0.5) * 3 ** 0.5 * 142.1
    dwg = svgwrite.Drawing(name+'.svg', profile='tiny', viewBox=("{} {} {} {}".format(0., 3. * 142.1, h, w)))
    for i in range(len(topo_c)):
        if (i in allowed):
            for j in topo_c[i]:
                if  (j in allowed) and(i<j):
                    line(coords_c[i], coords_c[j], dwg)
            circle(coords_c[i], fluor[i], dwg)
    dwg.save()




from Tkinter import *
import numpy as np
mycanvas=[]
canv_c={}
canv_wind=[]


class ResizingCanvas(Canvas):

    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()


    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height

        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        nsize=min(event.width,event.height)
        scale=min(float(event.width)/self.width,float(event.height)/self.height)
        self.width = nsize
        self.height = nsize
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,scale,scale)

def gen_coords_c(N, M):                                                                   # generate graphene's coordinates
    a0 = 142.1
    s3 = (3.)**0.5
    coords = []
    full_topo = {}
    x0 = s3 * a0 / 2.
    x1 = 0.
    for m in range(M):
        y0 = 0.
        y1 = a0 / 2.
        y2 = a0 * 1.5
        y3 = a0 * 2.
        z = 0.
        for n in range(N):
            coords.append((x0, y0, z))
            full_topo[4*N*m + 4*n] = []
            full_topo[4*N*m + 4*n].append(4*N*m + 4*n+1)                                  # connection wit this n
            if m < (M - 1):
                full_topo[4*N*m + 4*n].append(4*N*(m + 1) + 4*n + 1)                      # connection wit next m
            if n > 0:
                full_topo[4*N*m + 4*n].append(4*N*m + 4*n - 1)                            # connection wit previous n

            coords.append((x1, y1, z))
            full_topo[4*N*m + 4*n + 1] = []
            full_topo[4*N*m + 4*n + 1].append(4*N*m + 4*n)                                # connection wit this n
            full_topo[4*N*m + 4*n + 1].append(4*N*m + 4*n + 2)                            # connection wit this n
            if m > 0:
                full_topo[4*N*m + 4*n + 1].append(4*N*(m - 1) + 4*n)                      # connection wit previous m

            coords.append((x1, y2, z))
            full_topo[4*N*m + 4*n + 2] = []
            full_topo[4*N*m + 4*n + 2].append(4*N*m + 4*n + 1)                            # connection wit this n
            full_topo[4*N*m + 4*n + 2].append(4*N*m + 4*n + 3)                            # connection wit this n
            if m > 0:
                full_topo[4*N*m + 4*n + 2].append(4*N*(m - 1) + 4*n + 3)                  # connection wit previous m

            full_topo[4*N*m + 4*n + 3] = []
            coords.append((x0, y3, z))
            full_topo[4*N*m + 4*n + 3].append(4*N*m + 4*n + 2)                            # connection wit this n
            if m < (M - 1):
                full_topo[4*N*m + 4*n + 3].append(4*N*(m + 1) + 4*n + 2)                  # connection wit next m
            if n < (N - 1):
                full_topo[4*N*m + 4*n + 3].append(4*N*m + 4*(n+1))                        # connection wit next n

            y0 += 3.*a0
            y1 += 3.*a0
            y2 += 3.*a0
            y3 += 3.*a0
        x0 += s3*a0
        x1 += s3*a0

    return coords, full_topo



def newcircle(coord,ofset, c, canv):
    x = int(coord[0])+ofset[0]
    y = int(coord[1])+ofset[1]
    r=32
    ore=[x-r,y-r,x+r,y+r]
    if c == 1.:
        color='red'
    elif c == -1.:
        color = 'blue'
    else:
        color = 'white'
    return canv.create_oval(ore[0],ore[1],ore[2],ore[3], width=1,fill=color)

def line(a, b,ofset, canv):
    canv.create_line(int(a[0])+ofset[0],int(a[1])+ofset[1],int(b[0])+ofset[0],int(b[1])+ofset[1],width=1)

def plot_latt(N,M):
    canv_size = [3 * 140 * N + 140, int(3 ** 0.5 * M * 140 + 140)]
    canv_wind = Toplevel()
    canv_wind.geometry(str(canv_size[1]/10) + 'x' + str(canv_size[0]/10)+'+'+str(canv_wind.winfo_screenwidth()/2)+'+0')
    canv_wind.aspect(canv_size[1], canv_size[0], canv_size[1], canv_size[0])
    myframe = Frame(canv_wind)
    myframe.pack(fill=BOTH, expand=YES)
    global mycanvas
    mycanvas = ResizingCanvas(myframe, width=canv_size[1], height=canv_size[0], bg="white", highlightthickness=0)
    mycanvas.pack(fill=BOTH, expand=YES)
    global canv_c
    ofset=[140,140]
    coords_c,topo_c=gen_coords_c(N,M)
    for i, I in enumerate(topo_c.keys()):
        for j, J in enumerate(topo_c.keys()):
            if (J in topo_c[I]) and (J > I):
                line(coords_c[i], coords_c[j],ofset, mycanvas)
        canv_c[i]=newcircle(coords_c[i],ofset, 0, mycanvas)

def updcircle(i,N,M, c,f_n, F_N):
    if c == 1.:
        color='red'
    elif c == -1.:
        color = 'blue'
    else:
        color = 'white'

    j=(i//(4*N))*(4*(N-2))+i%(4*N)-4
    mycanvas.itemconfig(canv_c[j], fill=color)
    mycanvas.update()

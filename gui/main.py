from tkinter import *
from tkinter import filedialog
from gen_lattice import *
import svgwrite

def gen_lat():
    plot_latt(int(Nstr.get()), int(Mstr.get()))
    beta_scale.config(state='normal')
    fperc_scale.config(state='normal')
    one_side_but.config(state=NORMAL)
    f_gen_warn['text']=''
    e2.config(state=DISABLED)
    e1.config(state=DISABLED)
    b_gen_latt.config(state=DISABLED)
    b_res.config(state='normal')
    b_F.config(state='normal')
    b_res.config(state=DISABLED)

def reset():
    global mycanvas
    global canv_c
    mycanvas=[]
    canv_c={}
    e2.config(state='normal')
    e1.config(state='normal')
    b_gen_latt.config(state='normal')
    f_gen_warn['text'] = 'Set lattice parameters first'
    F_done['text']='...'
    b_save_c.config(state=DISABLED)
    b_save_svg.config(state=DISABLED)
    b_res.config(state=DISABLED)

fluor=[]
coord=[]
full_topo=[]
ncf = []
ncc = []
allowed=[]
# SVG part
def circle(coord,c,dwg):
    x=coord[0]
    y = coord[1]
    if c==1.:color='red'
    elif c == -1.:color = 'blue'
    else:color='white'
    dwg.add(dwg.circle((x, y), 25.13,stroke='black',stroke_width=2,fill=color))

def s_line(a,b,dwg):
    dwg.add(dwg.line((a[0],a[1]),(b[0],b[1]),  stroke='black', stroke_width=3 ))


def du_plot():
    fi = filedialog.asksaveasfile(mode='w',initialfile='N={}_M={}_b={}_f={}.svg'.format(int(Nstr.get()), int(Mstr.get()),beta.get(), f_perc.get()),defaultextension=".svg")
    if fi is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return

    N,M=int(Nstr.get()), int(Mstr.get())
    w = ((N) * 3. - 1.) * 142.1
    h = (M - 0.5) * 3 ** 0.5 * 142.1
    dwg = svgwrite.Drawing(fi.name, profile='tiny', viewBox=("{} {} {} {}".format(0., 3. * 142.1, h, w)))
    fi.close()
    for i in range(len(full_topo)):
        if (i in allowed):
            for j in full_topo[i]:
                if (j in allowed) and(i<j):
                    s_line(coord[i], coord[j], dwg)
            circle(coord[i], fluor[i], dwg)
    dwg.save()


def save_coord():
    fi = filedialog.asksaveasfile(mode='w',initialfile='N={}_M={}_b={}_f={}.xyz'.format(int(Nstr.get()), int(Mstr.get()), beta.get(),f_perc.get()), defaultextension=".xyz")
    if fi is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return

    i = 0
    for c in ncc:
        i += 1
        s = 'C' + "%8.3f" % c[0] + "%8.3f" % c[1] + "%8.3f" % c[
            2] + "\n"
        fi.write(s)
    j = 0
    for f in ncf:
        i += 1
        j += 1
        if f[2] != 0.:
            s = 'F' + "%8.3f" % f[0] + "%8.3f" % f[1] + "%8.3f" % f[2] + "\n"
            fi.write(s)
    fi.close()


def do_F():
    global fluor, coord,full_topo
    fluor, coord, full_topo=calcF(int(Nstr.get()), int(Mstr.get()),f_perc.get(), beta.get(),one_side.get())
#renormalization of coordinates
    ntf = []
    global ncf
    global ncc
    global allowed
    ncc=[]
    ncf=[]
    coords_c = np.array(coord) / 100.
    cc = []
    for i in range(len(coords_c)):
        if fluor[i] != 0:
            ncf.append([coords_c[i][0], coords_c[i][1], coords_c[i][2] + 1.7 * fluor[i]])
        cc.append([coords_c[i][0], coords_c[i][1], coords_c[i][2] + 0.2 * fluor[i]])
    allowed= []
    N,M=int(Nstr.get()), int(Mstr.get())
    m = 0
    for n in range(1, N + 1):
        for i in [0, 3]:
            allowed.append(4 * m * (N + 2) + 4 * n + i)
            ncc.append(cc[4 * m * (N + 2) + 4 * n + i])

    for m in range(1, M - 1):
        for n in range(1, N + 1):
            for i in range(4):
                allowed.append(4 * m * (N + 2) + 4 * n + i)
                ncc.append(cc[4 * m * (N + 2) + 4 * n + i])

    m = M - 1
    for n in range(1, N + 1):
        for i in [1, 2]:
            allowed.append(4 * m * (N + 2) + 4 * n + i)
            ncc.append(cc[4 * m * (N + 2) + 4 * n + i])


    #disabling buttons
    b_save_c.config(state=NORMAL)
    b_save_svg.config(state=NORMAL)
    b_res.config(state=NORMAL)
    beta_scale.config(state=DISABLED)
    fperc_scale.config(state=DISABLED)
    one_side_but.config(state=DISABLED)
    b_F.config(state=DISABLED)
    #save_coord()



#GUI:
root = Tk()
root.title('genCF')
one_side=IntVar()
one_side.set(1) # 1 - two side fluorination
                # 0 - one side fluorination
Nstr=StringVar()
Mstr=StringVar()

f_latt=LabelFrame(text="Lattice parameters")
f_lN=Frame(f_latt)
lln=Label(f_lN,text="N:")
e1 = Entry(f_lN,width=10,textvariable=Nstr)
e1.insert(END,'10')
f_lM=Frame(f_latt)
llm=Label(f_lM,text="M:")
e2 = Entry(f_lM,width=10,textvariable=Mstr)
e2.insert(END,'20')

f_mid=Frame()
b_gen_latt=Button(f_mid,text='generate lattice',command=gen_lat )

f_gen=LabelFrame(text="Fluorination parameters")
f_gen_warn=Label(f_gen)
f_gen_warn['text']='Set lattice parameters first'

one_side_but = Checkbutton(f_gen,text="One side fluorination", variable=one_side, onvalue=0, offvalue=1,state=DISABLED )
beta = DoubleVar()
beta_scale = Scale( f_gen, variable = beta, from_=0.,to=30,resolution=0.01,label='order degree',orient=HORIZONTAL,state=DISABLED )
f_perc= DoubleVar()
fperc_scale = Scale( f_gen, variable = f_perc, from_=0.,to=1.,resolution=0.01,label='fluorine content',orient=HORIZONTAL,state=DISABLED )



b_F=Button(f_gen,text='fluorinate',command=do_F,state=DISABLED)

F_done=Label(f_gen,text="..." )

save_frame=Frame(root)
b_save_c=Button(save_frame,text='save .xyz',command=save_coord,state=DISABLED)
b_save_svg=Button(save_frame,text='save .svg',command=du_plot,state=DISABLED)
save_frame.columnconfigure(0, weight=1)
save_frame.columnconfigure(1, weight=1)
b_save_c.grid(row=0, column=0)
b_save_svg.grid(row=0, column=1)

b_res=Button(text='reset',command=reset,state=DISABLED)

root.resizable(True, True)


f_latt.pack()
f_lN.pack()
f_lM.pack()
lln.pack(side=LEFT)
e1.pack(side=RIGHT)
llm.pack(side=LEFT)
e2.pack(side=RIGHT)
f_mid.pack()
b_gen_latt.pack()

f_gen.pack()
f_gen_warn.pack()
one_side_but.pack()
#two_side_but.pack()
beta_scale.pack()
fperc_scale.pack()

b_F.pack()


F_done.pack()
save_frame.pack(fill=X)
#b_save_c.pack()
#b_save_svg.pack()

b_res.pack()

root.mainloop()
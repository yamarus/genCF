from Tkinter import *
from gen_lattice import *

def gen_lat():
    plot_latt(int(Nstr.get()), int(Mstr.get()))
    beta_scale.config(state='normal')
    fperc_scale.config(state='normal')
    e2.config(state=DISABLED)
    e1.config(state=DISABLED)
    b_gen_latt.config(state=DISABLED)
    b_res.config(state='normal')
    b_F.config(state='normal')

def reset():
    global mycanvas
    global canv_c
    mycanvas=[]
    canv_c={}
    beta_scale.config(state=DISABLED)
    fperc_scale.config(state=DISABLED)
    e2.config(state='normal')
    e1.config(state='normal')
    b_gen_latt.config(state='normal')
    b_F.config(state=DISABLED)
    b_res.config(state=DISABLED)

def do_F():

    fluor, coord, full_topo=calcF(int(Nstr.get()), int(Mstr.get()),f_perc.get(), beta.get())

root = Tk()
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
beta = DoubleVar()
beta_scale = Scale( f_gen, variable = beta, from_=0.,to=30,resolution=0.01,label='order degree',orient=HORIZONTAL,state=DISABLED )
f_perc= DoubleVar()
fperc_scale = Scale( f_gen, variable = f_perc, from_=0.,to=1.,resolution=0.01,label='fluorine content',orient=HORIZONTAL,state=DISABLED )


F_done=Label(f_gen,text="....")
b_F=Button(f_gen,text='fluorinate',command=do_F,state=DISABLED)

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
beta_scale.pack()
fperc_scale.pack()
F_done.pack()
b_F.pack()
b_res.pack()

root.mainloop()
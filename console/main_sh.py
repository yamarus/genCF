from gen_lattice_sh import *

#    /                      |
#N=1|                       |
#    \                      \/ Y
#     |
#    /
#N=2|
#    \
#
#   M=1     M=2 ... ----> X

a0=1.421
s3=np.sqrt(3.)


parser = argparse.ArgumentParser()
#parser.add_argument("check", type=int)
parser.add_argument("-f", type=float,required=True, help='atomic fraction of F (float x for compound CFx)')
parser.add_argument("-b", type=float,required=True, default=0.3, help='ordering degree, default beta=0.3')
parser.add_argument("-N",type=int,required=True, help='number of "armchairs" along armchair edge')
parser.add_argument("-M",type=int,required=True, help='number of "zig-zags" along zig-zag edge')
parser.add_argument("-fig",type=str,default='yes', help='yes or no. Do you need a figure? default=yes')
parser.add_argument("-format",type=str,default='xyz', help='output coordinate format xyz or pdb. default=xyz ')
if len(sys.argv) <4:
    print '\nERROR! You must specified -f, -b, -N, -M options\n'
    parser.print_help()


args = parser.parse_args()

f_perc= float(args.f)
beta=args.b
M=int(args.M)
N=int(args.N)


#f_perc=1.
#beta=0.5
#M=7
#N=4


def write_pdb(coords,coords_f,filename):  #write coords into pdb
    fi = open(filename+'.pdb', 'w')
    fi.write('REMARK\n')
    i = 0
    for c in coords:
        i += 1
        s = 'ATOM' + "%7i" % i + '  CA  GRP A   1    ' + "%8.3f" % c[0] + "%8.3f" % c[1] + "%8.3f" % c[
            2] + "  1.00  0.00      GRP  C \n"
        fi.write(s)
    j=0
    for f in coords_f:
        i += 1
        j+=1
        if f[2]!=0.:
            s = 'ATOM' + "%7i" % i + '  F   GRP A   1    ' + "%8.3f" % f[0] + "%8.3f" % f[1] + "%8.3f" % f[2] + "  1.00  0.00      GRP  F \n"
            fi.write(s)


    fi.write('END\n')
    fi.close()


def write_xyz(coords,coords_f,filename):  #write coords into pdb
    fi = open(filename+'.xyz', 'w')
    i = 0
    for c in coords:
        i += 1
        s = 'C' + "%8.3f" % c[0] + "%8.3f" % c[1] + "%8.3f" % c[
            2] + "\n"
        fi.write(s)
    j=0
    for f in coords_f:
        i += 1
        j+=1
        if f[2]!=0.:
            s = 'F' + "%8.3f" % f[0] + "%8.3f" % f[1] + "%8.3f" % f[2] + "\n"
            fi.write(s)
    fi.close()



ntf=[]
ncf=[]
ncc=[]

fluor, coords_c, full_topo=calcF(N,M,f_perc,beta)
print('\n\n')



coords_c= np.array(coords_c)/100.
coords_f=[]
cc=[]
for i in range(len(coords_c)):
    if fluor[i]!=0:
        ncf.append([coords_c[i][0],coords_c[i][1],coords_c[i][2]+1.7*fluor[i]])
    cc.append([coords_c[i][0],coords_c[i][1],coords_c[i][2]+0.2*fluor[i]])
allowed_i=[]

m=0
for n in range(1, N + 1):
    for i in [0,3]:
        allowed_i.append(4 * m * (N + 2) + 4 * n + i)
        ncc.append(cc[4 * m * (N + 2) + 4 * n + i])
        ntf.append(fluor[4 * m * (N + 2) + 4 * n + i])
for m in range(1,M-1):
    for n in range(1,N+1):
        for i in range(4):
            allowed_i.append(4*m*(N+2)+4*n+i)
            ncc.append(cc[4*m*(N+2)+4*n+i])
            ntf.append(fluor[4 * m * (N+2)+ 4 * n + i])

m=M-1
for n in range(1, N + 1):
    for i in [1,2]:
        allowed_i.append(4 * m * (N + 2) + 4 * n + i)
        ncc.append(cc[4 * m * (N + 2) + 4 * n + i])
        ntf.append(fluor[4 * m * (N + 2) + 4 * n + i])


#print ncc
#print ncf

addname='_N='+str(N)+'_M='+str(M)+'_F='+str(f_perc)+'_b='+str(beta)

if args.fig=='yes':
    du_plot(coords_c,full_topo,allowed_i,fluor,N,M,'fig'+addname)
    print('figure saved as fig'+addname+'.svg file')
if args.format=='pdb':
    write_pdb(ncc,ncf,'coord'+addname)
    print('figure saved as coord' + addname + '.pdb file')
elif args.format=='xyz':
    write_xyz(ncc,ncf,'coord'+addname)
    print('figure saved as coord' + addname + '.xyz file')

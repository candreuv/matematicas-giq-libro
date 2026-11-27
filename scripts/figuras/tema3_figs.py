import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
plt.rcParams.update({"font.size":12,"mathtext.fontset":"cm"})
x=np.linspace(-1,5,100)
fig,axs=plt.subplots(1,3,figsize=(12,4))
cases=[("SCD: un punto",[(lambda x:5-2*x,r"$2x+y=5$",AZ),(lambda x:x-1,r"$x-y=1$",NA)],(2,1)),
       ("SCI: infinitos puntos",[(lambda x:3-x,r"$x+y=3$",AZ),(lambda x:3-x,r"$2x+2y=6$",NA)],None),
       ("SI: ningún punto",[(lambda x:3-x,r"$x+y=3$",AZ),(lambda x:1-x,r"$x+y=1$",NA)],None)]
for a,(t,ls,p) in zip(axs,cases):
    for k,(f,l,c) in enumerate(ls):
        a.plot(x,f(x),color=c,lw=3 if k==0 else 2,ls='-' if k==0 else '--',label=l)
    if p: a.plot(*p,'o',color='k',ms=8); a.annotate(r"$(2,1)$",p,xytext=(p[0]+.3,p[1]-.9))
    a.axhline(0,color=GR,lw=.8); a.axvline(0,color=GR,lw=.8); a.set_xlim(-1,5); a.set_ylim(-2,5); a.set_aspect('equal'); a.grid(alpha=.25)
    a.set_title(t); a.legend(loc='upper right',fontsize=10)
fig.tight_layout(); fig.savefig('sistemas_2d.png',dpi=110); plt.close()

fig=plt.figure(figsize=(12,4.4))
X,Y=np.meshgrid(np.linspace(-2,2,10),np.linspace(-2,2,10))
def plane(ax,a,b,c,d,col):
    Z=(d-a*X-b*Y)/c; Z[(Z<-3)|(Z>3)]=np.nan; ax.plot_surface(X,Y,Z,color=col,alpha=.45,edgecolor='none')
cfg=[("SCD: un punto común",[(0,0,1,0),(1,0,0.3,0),(0,1,-0.3,0)],'pt'),
     ("SCI: una recta común",[(0,0,1,0),(0,1,1,0),(0,1,-1,0)],'line'),
     ("SI: sin punto común",[(0,0,1,0),(0,1,1,1.5),(0,1,-1,1.5)],None)]
cols=[AZ,NA,VE]
for k,(t,pl,mark) in enumerate(cfg):
    ax=fig.add_subplot(1,3,k+1,projection='3d')
    for (a,b,c,d),col in zip(pl,cols):
        if abs(c)>1e-9: plane(ax,a,b,c,d,col)
        else:
            Yp,Zp=np.meshgrid(np.linspace(-2,2,10),np.linspace(-3,3,10)); ax.plot_surface(np.zeros_like(Yp)+d/a,Yp,Zp,color=col,alpha=.45,edgecolor='none')
    if mark=='pt': ax.scatter([0],[0],[0],color='k',s=40)
    if mark=='line': ax.plot([-2,2],[0,0],[0,0],color='k',lw=3)
    ax.set_title(t); ax.set_xlim(-2,2); ax.set_ylim(-2,2); ax.set_zlim(-3,3); ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([]); ax.view_init(20,-60)
fig.tight_layout(); fig.savefig('planos_3d.png',dpi=110); plt.close()

import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
AZ="#1f5fa8"; NA="#d35400"; GR="#555555"
plt.rcParams.update({"mathtext.fontset":"cm"})
L=[['a','b','c'],['d','e','f'],['g','h','i']]
pos=lambda r,c:(c,2-r)
plus=[[(0,0),(1,1),(2,2)],[(0,1),(1,2),(2,0)],[(0,2),(1,0),(2,1)]]
minus=[[(0,2),(1,1),(2,0)],[(0,1),(1,0),(2,2)],[(0,0),(1,2),(2,1)]]
nm=lambda tri:''.join(L[r][c] for r,c in tri)
fig,axs=plt.subplots(2,3,figsize=(10,7.4))
for row,(grp,col,sg) in enumerate([(plus,AZ,'+'),(minus,NA,'-')]):
    for k,tri in enumerate(grp):
        ax=axs[row,k]; pts=[pos(*p) for p in tri]
        if k==0: ax.plot([p[0] for p in pts],[p[1] for p in pts],color=col,lw=6,alpha=.8,solid_capstyle='round')
        else: ax.add_patch(Polygon(pts,closed=True,fc=col,alpha=.22,ec=col,lw=4))
        sel=set(tri)
        for r in range(3):
            for c in range(3):
                on=(r,c) in sel
                ax.text(*pos(r,c),f"${L[r][c]}$",ha='center',va='center',fontsize=24,color='k' if on else '#aaaaaa',
                        bbox=dict(boxstyle='circle,pad=0.25',fc='white',ec=col if on else '#cccccc',lw=2.5 if on else 1))
        ax.plot([-0.45,-0.45],[-0.4,2.4],color='k',lw=2); ax.plot([2.45,2.45],[-0.4,2.4],color='k',lw=2)
        ax.text(1,-0.95,f"${sg}\\,{nm(tri)}$",ha='center',fontsize=22,color=col)
        ax.set_xlim(-0.8,2.8); ax.set_ylim(-1.3,2.7); ax.set_aspect('equal'); ax.axis('off')
fig.text(0.5,0.955,r"Regla de Sarrus: $\det(A)=aei+bfg+cdh-ceg-bdi-afh$",ha='center',fontsize=17)
fig.text(0.02,0.72,"signo +",color=AZ,fontsize=15,rotation=90,va='center'); fig.text(0.02,0.27,"signo −",color=NA,fontsize=15,rotation=90,va='center')
fig.tight_layout(rect=(0.03,0,1,0.94)); fig.savefig('sarrus.png',dpi=105)

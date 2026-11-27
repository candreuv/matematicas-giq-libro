import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
AZ="#1f5fa8"; NA="#d35400"; GR="#999999"
plt.rcParams.update({"mathtext.fontset":"cm"})
REF=[["P","*","*","*","*"],["0","P","*","*","*"],["0","0","0","P","*"],["0","0","0","0","0"]]
RREF=[["1","0","*","0","*"],["0","1","*","0","*"],["0","0","0","1","*"],["0","0","0","0","0"]]
fig,axs=plt.subplots(1,2,figsize=(11,4.6))
for ax,M,col,tt,sub in [(axs[0],REF,AZ,"Forma escalonada (Gauss)",r"$\blacksquare$ = pivote $\neq0$,  $*$ = cualquier número"),(axs[1],RREF,NA,"Forma escalonada reducida (Gauss-Jordan)",r"pivotes $=1$ y ceros encima y debajo")]:
    n,m=len(M),len(M[0])
    for i in range(n):
        for j in range(m):
            v=M[i][j]; x,y=j,n-1-i
            if v=="P":
                ax.add_patch(Rectangle((x-0.28,y-0.28),0.56,0.56,color=col)); continue
            if v=="1": ax.add_patch(Rectangle((x-0.3,y-0.3),0.6,0.6,fc='white',ec=col,lw=3)); ax.text(x,y,"1",ha='center',va='center',fontsize=24,color=col,fontweight='bold'); continue
            if v=="0" and M is RREF and any(M[k][j]=="1" for k in range(n)):
                ax.text(x,y,"0",ha='center',va='center',fontsize=24,color=col); continue
            ax.text(x,y,"$*$" if v=="*" else v,ha='center',va='center',fontsize=26 if v=="*" else 24,color='k' if v=="*" else GR)
    # escalera
    steps=[(0,0),(1,1),(2,3)]
    xs=[];ys=[]
    for (i,j) in steps:
        xs+= [j-0.5,j+0.5]; ys+=[n-1-i-0.5]*2
    path_x=[-0.5]; path_y=[n-0.5-1+0.5]
    pts=[(-0.5,n-1.5)]
    for k,(i,j) in enumerate(steps):
        y=n-1-i-0.5
        nxt=steps[k+1][1]-0.5 if k+1<len(steps) else m-0.5
        pts+= [(j-0.5,y),(nxt,y)]
        if k+1<len(steps): pts.append((nxt,n-1-steps[k+1][0]-0.5))
    ax.plot([p[0] for p in pts],[p[1] for p in pts],color=col,lw=2,ls='--',alpha=.7)
    ax.plot([-0.75,-0.75],[-0.6,n-0.4],color='k',lw=2.5); ax.plot([-0.75,-0.6],[n-0.4,n-0.4],color='k',lw=2.5); ax.plot([-0.75,-0.6],[-0.6,-0.6],color='k',lw=2.5)
    ax.plot([m-0.25,m-0.25],[-0.6,n-0.4],color='k',lw=2.5); ax.plot([m-0.4,m-0.25],[n-0.4,n-0.4],color='k',lw=2.5); ax.plot([m-0.4,m-0.25],[-0.6,-0.6],color='k',lw=2.5)
    ax.set_title(tt,fontsize=15,color=col); ax.text((m-1)/2,-1.2,sub,ha='center',fontsize=13)
    ax.set_xlim(-1,m); ax.set_ylim(-1.6,n); ax.set_aspect('equal'); ax.axis('off')
fig.tight_layout(); fig.savefig('ref_rref.png',dpi=110)

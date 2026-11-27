from manim import *
from fractions import Fraction as Fr
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#777777"
def tex(x):
    x=Fr(x); return str(x.numerator) if x.denominator==1 else r"%s\tfrac{%d}{%d}"%("-" if x<0 else "",abs(x.numerator),x.denominator)
class Gauss(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK); Tex.set_default(color=BLACK)
        R=[[Fr(v) for v in r] for r in [[1,1,1,6],[2,-1,1,3],[1,2,-1,2]]]
        dx,dy=1.25,0.85; ox,oy=-2.2,0.9
        pos=lambda i,j: [ox+j*dx+(0.35 if j==3 else 0),oy-i*dy,0]
        E=[[MathTex(tex(R[i][j]),font_size=44).move_to(pos(i,j)) for j in range(4)] for i in range(3)]
        allE=VGroup(*[e for r in E for e in r])
        top,bot=oy+0.5,oy-2*dy-0.5; L=ox-0.55; Rr=ox+3*dx+0.35+0.55
        br=VGroup(Line([L,top,0],[L,bot,0]),Line([L,top,0],[L+0.2,top,0]),Line([L,bot,0],[L+0.2,bot,0]),
                  Line([Rr,top,0],[Rr,bot,0]),Line([Rr,top,0],[Rr-0.2,top,0]),Line([Rr,bot,0],[Rr-0.2,bot,0])).set_color(BLACK).set_stroke(width=3)
        xb=ox+2*dx+dx/2+0.17; bar=Line([xb,top-0.1,0],[xb,bot+0.1,0],color=BLACK,stroke_width=2)
        sys=MathTex(r"\begin{cases}x+y+z=6\\2x-y+z=3\\x+2y-z=2\end{cases}",font_size=36).to_corner(UL)
        ttl=Tex("Gauss: ceros debajo de los pivotes",font_size=34,color=AZ).to_corner(UR)
        self.play(FadeIn(sys),FadeIn(br),FadeIn(bar),FadeIn(allE),FadeIn(ttl))
        def op(label,col,target,src,f,pivot=None):
            nonlocal R
            hl=SurroundingRectangle(VGroup(*E[target]),color=col,buff=0.12,stroke_width=3)
            hs=SurroundingRectangle(VGroup(*E[src]),color=GR,buff=0.12,stroke_width=2) if src is not None else VMobject()
            lab=MathTex(label,font_size=40,color=col).move_to([ox+1.9,bot-0.7,0])
            self.play(Create(hl),Create(hs),FadeIn(lab),run_time=0.5)
            new=f(R); anims=[]
            for j in range(4):
                if new[target][j]!=R[target][j]:
                    ne=MathTex(tex(new[target][j]),font_size=44,color=col).move_to(pos(target,j))
                    anims.append(Transform(E[target][j],ne))
            self.play(*anims,run_time=0.9); R=new
            self.play(*[E[target][j].animate.set_color(BLACK) for j in range(4)],FadeOut(hl),FadeOut(hs),FadeOut(lab),run_time=0.4)
            if pivot:
                i,j=pivot; c=Circle(radius=0.32,color=col,stroke_width=3).move_to(pos(i,j)); self.add(c); return c
        def rowop(t,s,a,b): # R_t <- a R_t + b R_s
            return lambda R:[r if k!=t else [a*x+b*y for x,y in zip(R[t],R[s])] for k,r in enumerate(R)]
        def scale(t,a): return lambda R:[r if k!=t else [a*x for x in R[t]] for k,r in enumerate(R)]
        p1=Circle(radius=0.32,color=AZ,stroke_width=3).move_to(pos(0,0)); self.play(Create(p1))
        op(r"F_2\gets F_2-2F_1",AZ,1,0,rowop(1,0,1,-2))
        op(r"F_3\gets F_3-F_1",AZ,2,0,rowop(2,0,1,-1))
        p2=Circle(radius=0.32,color=AZ,stroke_width=3).move_to(pos(1,1)); self.play(Create(p2))
        op(r"F_3\gets 3F_3+F_2",AZ,2,1,rowop(2,1,3,1))
        p3=Circle(radius=0.32,color=AZ,stroke_width=3).move_to(pos(2,2)); self.play(Create(p3))
        ref=Tex(r"Forma escalonada: $z=3,\ y=2,\ x=1$",font_size=32,color=AZ).move_to([ox+1.9,bot-0.7,0])
        self.play(FadeIn(ref)); self.wait(1.8); self.play(FadeOut(ref))
        ttl2=Tex("Gauss-Jordan: pivotes 1 y ceros encima",font_size=34,color=NA).to_corner(UR)
        self.play(Transform(ttl,ttl2))
        op(r"F_3\gets -\tfrac17F_3",NA,2,None,scale(2,Fr(-1,7)))
        op(r"F_2\gets F_2+F_3",NA,1,2,rowop(1,2,1,1))
        op(r"F_1\gets F_1-F_3",NA,0,2,rowop(0,2,1,-1))
        op(r"F_2\gets -\tfrac13F_2",NA,1,None,scale(1,Fr(-1,3)))
        op(r"F_1\gets F_1-F_2",NA,0,1,rowop(0,1,1,-1))
        self.play(*[c.animate.set_color(NA) for c in (p1,p2,p3)])
        sol=MathTex(r"(x,y,z)=(1,2,3)",font_size=44,color=VE).move_to([ox+1.9,bot-0.75,0])
        self.play(FadeIn(sol)); self.wait(2.5)

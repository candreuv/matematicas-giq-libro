from manim import *
import numpy as np
from fractions import Fraction as Fr
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"
def fmt(x):
    x=Fr(x); return str(x.numerator) if x.denominator==1 else r"\tfrac{%d}{%d}"%(x.numerator,x.denominator)
def M(rows):
    s=r"\left(\begin{array}{ccc|c}"+r"\\".join("&".join(fmt(v) for v in r) for r in rows)+r"\end{array}\right)"
    return MathTex(s,font_size=48)
class Gauss(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK); Tex.set_default(color=BLACK)
        R=[[1,1,1,6],[2,-1,1,3],[1,2,-1,2]]
        R=[[Fr(v) for v in r] for r in R]
        sys=MathTex(r"\begin{cases}x+y+z=6\\2x-y+z=3\\x+2y-z=2\end{cases}",font_size=40).to_corner(UL)
        self.play(FadeIn(sys))
        cur=M(R).shift(DOWN*0.2); self.play(FadeIn(cur))
        ttl=Tex("Gauss: ceros debajo de los pivotes",font_size=34,color=AZ).to_edge(UP).shift(RIGHT*2)
        self.play(FadeIn(ttl))
        ops=[("F_2\\gets F_2-2F_1",lambda R:[R[0],[a-2*b for a,b in zip(R[1],R[0])],R[2]]),
             ("F_3\\gets F_3-F_1",lambda R:[R[0],R[1],[a-b for a,b in zip(R[2],R[0])]]),
             ("F_3\\gets 3F_3+F_2",lambda R:[R[0],R[1],[3*a+b for a,b in zip(R[2],R[1])]])]
        ops2=[("F_3\\gets -\\tfrac17F_3",lambda R:[R[0],R[1],[a/-7 for a in R[2]]]),
              ("F_2\\gets F_2+F_3",lambda R:[R[0],[a+b for a,b in zip(R[1],R[2])],R[2]]),
              ("F_1\\gets F_1-F_3",lambda R:[[a-b for a,b in zip(R[0],R[2])],R[1],R[2]]),
              ("F_2\\gets -\\tfrac13F_2",lambda R:[R[0],[a/-3 for a in R[1]],R[2]]),
              ("F_1\\gets F_1-F_2",lambda R:[[a-b for a,b in zip(R[0],R[1])],R[1],R[2]])]
        def run(ops,col):
            nonlocal R,cur
            for txt,f in ops:
                op=MathTex(txt,font_size=40,color=col).next_to(cur,DOWN,buff=0.5)
                self.play(FadeIn(op),run_time=0.5)
                R=f(R); new=M(R).move_to(cur)
                self.play(TransformMatchingTex(cur,new) if False else ReplacementTransform(cur,new),run_time=0.9); cur=new
                self.wait(0.6); self.play(FadeOut(op),run_time=0.3)
        run(ops,AZ)
        back=Tex(r"Sustitución regresiva: $z=3,\ y=2,\ x=1$",font_size=34,color=AZ).next_to(cur,DOWN,buff=0.5)
        self.play(FadeIn(back)); self.wait(1.5); self.play(FadeOut(back))
        ttl2=Tex("Gauss-Jordan: pivotes 1 y ceros encima",font_size=34,color=NA).move_to(ttl)
        self.play(Transform(ttl,ttl2))
        run(ops2,NA)
        sol=MathTex(r"(x,y,z)=(1,2,3)",font_size=44,color=VE).next_to(cur,DOWN,buff=0.5)
        self.play(FadeIn(sol)); self.wait(2.5)

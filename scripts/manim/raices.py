from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class Raices(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        pl=NumberPlane(x_range=[-1.5,1.5,0.5],y_range=[-1.5,1.5,0.5],x_length=5.6,y_length=5.6,
            background_line_style={"stroke_color":GR,"stroke_opacity":0.15},axis_config={"color":GR}).shift(LEFT*2.8+DOWN*0.2)
        c=lambda q: pl.c2p(q.real,q.imag)
        self.add(pl, Circle(radius=pl.x_axis.unit_size,color=GR,stroke_width=2).move_to(c(0)))
        theta=np.pi/2
        cur=None
        for n in [2,3,4,5,6]:
            ws=[np.exp(1j*(theta+2*np.pi*k)/n) for k in range(n)]
            dots=VGroup(*[Dot(c(w),color=AZ,radius=0.1) for w in ws])
            poly=Polygon(*[c(w) for w in ws],color=VE,stroke_width=4) if n>2 else Line(c(ws[0]),c(ws[1]),color=VE,stroke_width=4)
            t=VGroup(MathTex(r"w^{"+str(n)+r"}=i",font_size=48),
                     MathTex(r"w_k=e^{\,i\frac{\pi/2+2\pi k}{"+str(n)+r"}}",font_size=40),
                     MathTex(r"k=0,\dots,"+str(n-1),font_size=40),
                     Tex(f"{n} raíces, separadas $2\\pi/{n}$",font_size=36,color=VE)).arrange(DOWN,aligned_edge=LEFT,buff=0.3).to_edge(RIGHT,buff=0.5)
            g=VGroup(dots,poly,t)
            if cur is None:
                self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],lag_ratio=0.3),FadeIn(t)); self.play(Create(poly))
            else:
                self.play(FadeOut(cur),run_time=0.4)
                self.play(LaggedStart(*[GrowFromCenter(d) for d in dots],lag_ratio=0.25),FadeIn(t),run_time=1); self.play(Create(poly),run_time=0.8)
            cur=g; self.wait(1.3)
        self.wait(0.5)

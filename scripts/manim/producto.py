from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class Producto(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        pl=NumberPlane(x_range=[-3,3,1],y_range=[-0.5,3.5,1],x_length=7.2,y_length=4.8,
            background_line_style={"stroke_color":GR,"stroke_opacity":0.15},axis_config={"color":GR}).shift(LEFT*2.4+DOWN*0.4)
        self.add(pl)
        z=1.5*np.exp(1j*np.pi/9); w=1.3*np.exp(1j*np.pi/3)
        c=lambda q: pl.c2p(q.real,q.imag)
        az=Arrow(c(0),c(z),buff=0,color=AZ,stroke_width=6); lz=MathTex(r"z=1.5\,e^{i\pi/9}",font_size=36,color=AZ).next_to(c(z),RIGHT,buff=0.1)
        aw=Arrow(c(0),c(w),buff=0,color=NA,stroke_width=6); lw=MathTex(r"w=1.3\,e^{i\pi/3}",font_size=36,color=NA).next_to(c(w),RIGHT,buff=0.15).shift(UP*0.15)
        self.play(GrowArrow(az),FadeIn(lz)); self.play(GrowArrow(aw),FadeIn(lw))
        txt=VGroup(MathTex(r"zw=(1.5\cdot1.3)\,e^{i(\pi/9+\pi/3)}",font_size=36),
                   Tex(r"1) se estira $\times1.3$",font_size=34,color=VE),
                   Tex(r"2) gira $+\pi/3$",font_size=34,color=VE)).arrange(DOWN,aligned_edge=LEFT).to_corner(UR,buff=0.3)
        self.play(Write(txt[0]))
        m=Arrow(c(0),c(z),buff=0,color=VE,stroke_width=6)
        self.add(m)
        self.play(FadeIn(txt[1]),Transform(m,Arrow(c(0),c(1.3*z),buff=0,color=VE,stroke_width=6)),run_time=1.5)
        rot=ValueTracker(0)
        m2=always_redraw(lambda: Arrow(c(0),c(1.3*z*np.exp(1j*rot.get_value())),buff=0,color=VE,stroke_width=6))
        self.remove(m); self.add(m2)
        arc=always_redraw(lambda: Arc(radius=1.1,start_angle=np.angle(z),angle=rot.get_value(),arc_center=c(0),color=VE,stroke_width=3))
        self.add(arc)
        self.play(FadeIn(txt[2]),rot.animate.set_value(np.pi/3),run_time=2)
        lp=MathTex(r"zw=1.95\,e^{i4\pi/9}",font_size=36,color=VE).next_to(c(z*w),LEFT,buff=0.15)
        self.play(FadeIn(lp)); self.wait(2)

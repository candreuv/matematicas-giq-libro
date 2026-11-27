from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class Argumentos(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        O=LEFT*2.8+DOWN*0.3; R=2.2; th=PI/4
        ax=VGroup(Line(O+LEFT*2.6,O+RIGHT*2.6,color=GR),Line(O+DOWN*2.6,O+UP*2.6,color=GR))
        self.add(ax)
        z=O+R*np.array([np.cos(th),np.sin(th),0])
        v=Arrow(O,z,buff=0,color=AZ,stroke_width=6); d=Dot(z,color=AZ)
        lz=MathTex("z",color=AZ,font_size=44).next_to(z,UR,buff=0.1)
        self.play(GrowArrow(v),FadeIn(d),FadeIn(lz))
        txt=MathTex(r"\theta",font_size=42).to_corner(UR).shift(LEFT*1.2)
        self.add(txt)
        phi=ValueTracker(0)
        def spiral():
            p=phi.get_value()
            if p<0.01: return VMobject()
            ts=np.linspace(0,p,max(2,int(60*p)))
            pts=[O+(0.45+0.11*t)*np.array([np.cos(t),np.sin(t),0]) for t in ts]
            return VMobject(color=NA,stroke_width=4).set_points_smoothly(pts)
        sp=always_redraw(spiral); self.add(sp)
        steps=[(th,r"\theta=\frac{\pi}{4}"),(th+2*PI,r"\theta+2\pi=\frac{9\pi}{4}"),(th+4*PI,r"\theta+4\pi=\frac{17\pi}{4}")]
        for val,tex in steps:
            nt=MathTex(tex,font_size=42).move_to(txt,aligned_edge=RIGHT)
            self.play(phi.animate.set_value(val),Transform(txt,nt),run_time=2 if val>th else 1)
            self.play(Indicate(d,color=NA),run_time=0.6); self.wait(0.6)
        neg=MathTex(r"\theta-2\pi=-\frac{7\pi}{4}",font_size=42).move_to(txt,aligned_edge=RIGHT)
        self.play(phi.animate.set_value(0.001),run_time=1.2)
        sp2=always_redraw(lambda: VMobject(color=VE,stroke_width=4).set_points_smoothly([O+(0.45+0.06*abs(t))*np.array([np.cos(t),np.sin(t),0]) for t in np.linspace(0,phi.get_value(),max(2,int(60*abs(phi.get_value()))+2))]) if abs(phi.get_value())>0.01 else VMobject())
        self.remove(sp); self.add(sp2)
        self.play(phi.animate.set_value(th-2*PI),Transform(txt,neg),run_time=2); self.play(Indicate(d,color=VE),run_time=0.6)
        con=VGroup(Tex("Todos son el mismo ángulo:",font_size=36),MathTex(r"\theta+2\pi k,\ k\in\mathbb Z",font_size=42,color=NA)).arrange(DOWN,aligned_edge=LEFT).next_to(txt,DOWN,buff=0.6).align_to(txt,RIGHT)
        self.play(FadeIn(con)); self.wait(2.2)

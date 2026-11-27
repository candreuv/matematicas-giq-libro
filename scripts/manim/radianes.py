from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class Radianes(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        R=2.0; O=LEFT*2.6+DOWN*0.2
        circ=Circle(radius=R,color=GR,stroke_width=3).move_to(O)
        rad=Line(O,O+RIGHT*R,color=AZ,stroke_width=7)
        lr=MathTex("R",color=AZ,font_size=42).next_to(rad,DOWN,buff=0.12)
        self.play(Create(circ),Create(rad),FadeIn(lr),Dot(O,color=BLACK).animate.scale(1))
        tit=MathTex(r"\theta=\frac{s}{R}",font_size=50).to_corner(UR).shift(LEFT*0.6)
        self.play(Write(tit))
        # copia del radio que se enrolla sobre la circunferencia
        seg=rad.copy().set_color(NA)
        self.play(seg.animate.shift(UP*0.001),run_time=0.2)
        arc1=Arc(radius=R,start_angle=0,angle=1,arc_center=O,color=NA,stroke_width=9)
        self.play(Transform(seg,arc1),run_time=1.6)
        r2=Line(O,O+R*np.array([np.cos(1),np.sin(1),0]),color=AZ,stroke_width=4)
        ang=Arc(radius=0.55,start_angle=0,angle=1,arc_center=O,color=BLACK,stroke_width=3)
        t1=VGroup(MathTex(r"s=R",color=NA,font_size=40),MathTex(r"\Rightarrow\ \theta=1\ \text{rad}\approx57.3^\circ",font_size=40)).arrange(DOWN,aligned_edge=LEFT).next_to(tit,DOWN,buff=0.5).align_to(tit,RIGHT)
        self.play(Create(r2),Create(ang),FadeIn(t1)); self.wait(1.2)
        # cuantos radios caben en la vuelta
        arcs=VGroup(); cnt=ValueTracker(1)
        lab=always_redraw(lambda: MathTex(r"\text{radios: }"+f"{cnt.get_value():.2f}",font_size=38,color=NA).next_to(t1,DOWN,buff=0.5).align_to(tit,RIGHT))
        self.add(lab)
        cols=[NA,"#e59866"]
        for k in range(1,6):
            a=Arc(radius=R,start_angle=k,angle=1,arc_center=O,color=cols[k%2],stroke_width=9)
            self.play(Create(a),cnt.animate.set_value(k+1),run_time=0.6); arcs.add(a)
        a=Arc(radius=R,start_angle=6,angle=2*PI-6,arc_center=O,color=VE,stroke_width=9)
        self.play(Create(a),cnt.animate.set_value(2*PI),run_time=0.6)
        fin=VGroup(Tex("vuelta completa:",font_size=36),MathTex(r"2\pi\approx6.28\ \text{rad}=360^\circ",font_size=38)).arrange(DOWN,aligned_edge=RIGHT).next_to(lab,DOWN,buff=0.4).align_to(tit,RIGHT)
        self.play(FadeIn(fin)); self.wait(1.2)
        eq=MathTex(r"\pi\ \text{rad}=180^\circ",font_size=40,color=AZ).next_to(fin,DOWN,buff=0.35).align_to(tit,RIGHT)
        self.play(FadeIn(eq)); self.wait(2)

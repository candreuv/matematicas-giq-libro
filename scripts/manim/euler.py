from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class Euler(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        R=1.25; C=np.array([-4.6,1.75,0])
        sx=1.35   # unidades por radián en la onda seno (horizontal)
        cy=0.45   # unidades por radián en la onda coseno (vertical, hacia abajo)
        X0=C[0]+R+0.6; Y0=C[1]-R-0.45
        # ejes
        circ_ax=VGroup(Line(C+LEFT*1.6,C+RIGHT*1.6,color=GR,stroke_width=2),Line(C+DOWN*1.6,C+UP*1.6,color=GR,stroke_width=2))
        sax=VGroup(Line([X0,C[1],0],[X0+2*PI*sx+0.3,C[1],0],color=GR,stroke_width=2),Line([X0,C[1]-1.5,0],[X0,C[1]+1.5,0],color=GR,stroke_width=2))
        cax=VGroup(Line([C[0],Y0,0],[C[0],Y0-2*PI*cy-0.3,0],color=GR,stroke_width=2),Line([C[0]-1.5,Y0,0],[C[0]+1.5,Y0,0],color=GR,stroke_width=2))
        lsx=MathTex(r"\theta",font_size=32).next_to(sax[0],RIGHT,buff=0.1)
        lcx=MathTex(r"\theta",font_size=32).next_to(cax[0],DOWN,buff=0.05)
        ls=MathTex(r"\operatorname{Im}=\operatorname{sen}\theta",font_size=30,color=VE).next_to(sax[0].get_end(),UP,buff=1.1).shift(LEFT*0.9)
        lc=MathTex(r"\operatorname{Re}=\cos\theta",font_size=30,color=NA).next_to(cax[1],RIGHT,buff=0.6).shift(DOWN*0.6)
        self.add(circ_ax)
        th=ValueTracker(0.8)
        P=lambda: C+R*np.array([np.cos(th.get_value()),np.sin(th.get_value()),0])
        cx=always_redraw(lambda: Line(C,C+R*np.array([np.cos(th.get_value()),0,0]),color=NA,stroke_width=7))
        sy=always_redraw(lambda: Line(C+R*np.array([np.cos(th.get_value()),0,0]),P(),color=VE,stroke_width=7))
        vec=always_redraw(lambda: Line(C,P(),color=AZ,stroke_width=6))
        dot=always_redraw(lambda: Dot(P(),color=AZ,radius=0.08))
        arc=always_redraw(lambda: Arc(radius=0.4,start_angle=0,angle=th.get_value()%(2*PI)+1e-3,arc_center=C,color=BLACK,stroke_width=3))
        # texto (zona inferior derecha)
        T0=np.array([0.2,-0.9,0])
        s1=MathTex(r"w=\cos\theta+i\,\operatorname{sen}\theta",font_size=38).move_to(T0,aligned_edge=LEFT)
        s2=MathTex(r"|w|=\sqrt{\cos^2\theta+\operatorname{sen}^2\theta}=1",font_size=38).next_to(s1,DOWN,buff=0.3,aligned_edge=LEFT)
        s3=MathTex(r"\text{Euler: }e^{i\theta}=w\ \Rightarrow\ |e^{i\theta}|=1",font_size=38,color=AZ).next_to(s2,DOWN,buff=0.3,aligned_edge=LEFT)
        self.play(Write(s1)); self.play(Create(cx),Create(sy),Create(arc),FadeIn(dot))
        self.play(Create(vec)); self.play(Write(s2)); self.wait(0.6)
        # giro desde 0, con circunferencia y ondas
        self.play(th.animate.set_value(0.001),run_time=1)
        self.play(Create(sax),Create(cax),FadeIn(lsx),FadeIn(lcx),FadeIn(ls),FadeIn(lc),run_time=1)
        trc=TracedPath(lambda: P(),stroke_color=AZ,stroke_width=3)
        sw=always_redraw(lambda: ParametricFunction(lambda t: np.array([X0+t*sx,C[1]+R*np.sin(t),0]),t_range=[0,max(th.get_value(),0.002)],color=VE,stroke_width=5))
        cw=always_redraw(lambda: ParametricFunction(lambda t: np.array([C[0]+R*np.cos(t),Y0-t*cy,0]),t_range=[0,max(th.get_value(),0.002)],color=NA,stroke_width=5))
        hs=always_redraw(lambda: DashedLine(P(),[X0+th.get_value()*sx,P()[1],0],color=VE,stroke_width=2,dash_length=0.08))
        vs=always_redraw(lambda: DashedLine(P(),[P()[0],Y0-th.get_value()*cy,0],color=NA,stroke_width=2,dash_length=0.08))
        ds=always_redraw(lambda: Dot([X0+th.get_value()*sx,P()[1],0],color=VE,radius=0.07))
        dc=always_redraw(lambda: Dot([P()[0],Y0-th.get_value()*cy,0],color=NA,radius=0.07))
        self.add(trc,sw,cw,hs,vs,ds,dc)
        self.play(th.animate.set_value(2*PI),run_time=8,rate_func=linear)
        self.play(Write(s3)); self.wait(2.5)

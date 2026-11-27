from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class PlanoTangente(ThreeDScene):
    def construct(self):
        MathTex.set_default(color=BLACK); Tex.set_default(color=BLACK)
        ax=ThreeDAxes(x_range=[-1,1,0.5],y_range=[-1,1,0.5],z_range=[-7,7,7],x_length=4.4,y_length=4.4,z_length=4.2,axis_config={"color":GR,"stroke_width":1.5},tips=False)
        self.set_camera_orientation(phi=68*DEGREES,theta=-125*DEGREES,zoom=0.95,focal_distance=40)
        h=ValueTracker(1.0)
        f=lambda u,v,hh: 4*u+2*v+hh*(2*u*u+v*v)
        surf=always_redraw(lambda: Surface(lambda u,v: ax.c2p(u,v,f(u,v,h.get_value())),u_range=[-1,1],v_range=[-1,1],resolution=(12,12),
            fill_opacity=0.85,checkerboard_colors=["#3d85c6","#2f6fb0"],stroke_color=AZ,stroke_width=0.5))
        plane=Surface(lambda u,v: ax.c2p(u,v,4*u+2*v),u_range=[-1,1],v_range=[-1,1],resolution=(2,2),fill_opacity=0.6,checkerboard_colors=["#e67e22","#e67e22"],stroke_color=NA,stroke_width=1.5)
        P=Dot3D(ax.c2p(0,0,0),color=BLACK,radius=0.08)
        self.add(ax)
        t1=MathTex(r"z=f(x,y)=2x^2+y^2",font_size=34,color=AZ).to_corner(UL)
        t2=MathTex(r"z=L(x,y)=3+4(x-1)+2(y-1)",font_size=34,color=NA).next_to(t1,DOWN,aligned_edge=LEFT)
        t3=MathTex(r"P=(1,1,3)",font_size=34).next_to(t2,DOWN,aligned_edge=LEFT)
        for t in (t1,t2,t3): self.add_fixed_in_frame_mobjects(t); t.set_opacity(0)
        self.add(surf); self.play(t1.animate.set_opacity(1),run_time=0.8)
        self.add(P); self.play(t3.animate.set_opacity(1),run_time=0.6)
        self.play(FadeIn(plane),t2.animate.set_opacity(1),run_time=1.2)
        self.begin_ambient_camera_rotation(rate=0.06)
        self.wait(2)
        lab=always_redraw(lambda: MathTex(r"\text{ventana: }|x-1|,|y-1|\le"+f"{h.get_value():.2f}",font_size=32).to_corner(DL))
        lab2=MathTex(r"\text{zoom: al acercarnos, }f-L\text{ es despreciable}",font_size=30,color=VE).to_corner(DR)
        self.add_fixed_in_frame_mobjects(lab,lab2); lab2.set_opacity(0)
        self.play(lab2.animate.set_opacity(1),run_time=0.6)
        self.play(h.animate.set_value(0.05),run_time=7,rate_func=smooth)
        self.wait(1)
        lim=MathTex(r"\lim_{(x,y)\to(1,1)}\frac{f(x,y)-L(x,y)}{\sqrt{(x-1)^2+(y-1)^2}}=0",font_size=32).next_to(t3,DOWN,aligned_edge=LEFT,buff=0.3)
        self.add_fixed_in_frame_mobjects(lim); lim.set_opacity(0); self.play(lim.animate.set_opacity(1),run_time=0.8)
        self.wait(2.5)
        self.stop_ambient_camera_rotation()

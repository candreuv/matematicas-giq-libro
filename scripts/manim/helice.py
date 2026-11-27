from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
T=4*PI
class Helice(ThreeDScene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax=ThreeDAxes(x_range=[0,T+0.5,PI],y_range=[-1.5,1.5,1],z_range=[-1.5,1.5,1],x_length=7.5,y_length=3.6,z_length=3.6,axis_config={"color":GR,"stroke_width":2},tips=False)
        self.set_camera_orientation(phi=62*DEGREES,theta=-52*DEGREES,zoom=0.9,focal_distance=60)
        lt=MathTex(r"\theta",font_size=40); lr=MathTex(r"\mathrm{Re}",font_size=34,color=NA); li=MathTex(r"\mathrm{Im}",font_size=34,color=VE)
        for m,p in [(lt,ax.c2p(T+0.9,0,0)),(lr,ax.c2p(0,2.0,0)),(li,ax.c2p(0,0,1.95))]:
            m.move_to(p); self.add_fixed_orientation_mobjects(m)
        self.add(ax)
        for k in range(3):
            self.add(Circle(radius=ax.y_axis.unit_size,color=GR,stroke_width=1.5,stroke_opacity=0.5).rotate(PI/2,axis=UP).move_to(ax.c2p(2*PI*k,0,0)))
        tit=MathTex(r"e^{i\theta}=\cos\theta+i\,\operatorname{sen}\theta",font_size=40).to_corner(UL)
        self.add_fixed_in_frame_mobjects(tit)
        th=ValueTracker(0.001)
        hel=always_redraw(lambda: ParametricFunction(lambda t: ax.c2p(t,np.cos(t),np.sin(t)),t_range=[0,th.get_value()],color=AZ,stroke_width=6))
        dot=always_redraw(lambda: Dot3D(ax.c2p(th.get_value(),np.cos(th.get_value()),np.sin(th.get_value())),color=AZ,radius=0.09))
        rad=always_redraw(lambda: Line(ax.c2p(th.get_value(),0,0),ax.c2p(th.get_value(),np.cos(th.get_value()),np.sin(th.get_value())),color=AZ,stroke_width=3))
        self.add(hel,dot,rad)
        cap=Tex(r"Al crecer $\theta$, $e^{i\theta}$ gira con módulo 1: una hélice",font_size=34,color=AZ).to_corner(DL)
        self.add_fixed_in_frame_mobjects(cap)
        self.play(th.animate.set_value(T),run_time=8,rate_func=linear)
        self.wait(0.5)
        views=[(0,-90,r"Desde arriba: la parte real es $\cos\theta$",NA),
               (90,-90,r"De frente: la parte imaginaria es $\operatorname{sen}\theta$",VE),
               (90,0,r"A lo largo de $\theta$: la circunferencia $|e^{i\theta}|=1$",AZ)]
        for ph,tt,txt,col in views:
            new=Tex(txt,font_size=34,color=col).to_corner(DL)
            self.remove(cap); self.add_fixed_in_frame_mobjects(new); cap=new
            self.move_camera(phi=ph*DEGREES,theta=tt*DEGREES,run_time=2.2)
            self.wait(1.4)
        new=Tex(r"Al crecer $\theta$, $e^{i\theta}$ gira con módulo 1: una hélice",font_size=34,color=AZ).to_corner(DL)
        self.remove(cap); self.add_fixed_in_frame_mobjects(new)
        self.move_camera(phi=62*DEGREES,theta=-52*DEGREES,run_time=2)
        self.wait(1)

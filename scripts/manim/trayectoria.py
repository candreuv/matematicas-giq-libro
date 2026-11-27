from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; GR="#555555"; GC="#9a9a9a"
T=4*PI
def R(t): return 0.8+t/10
def r(t): return np.array([R(t)*np.cos(t), R(t)*np.sin(t), t/4])
def dr(t): return np.array([-np.cos(t)/10-R(t)*np.sin(t), -np.sin(t)/10+R(t)*np.cos(t), 1/4])

class Trayectoria(ThreeDScene):
    def construct(self):
        MathTex.set_default(color=BLACK); Tex.set_default(color=BLACK)
        ax=ThreeDAxes(x_range=[-2.5,2.5,1],y_range=[-2.5,2.5,1],z_range=[0,3.5,1],
                      x_length=5,y_length=5,z_length=3.5,
                      axis_config={"color":GR,"stroke_width":2},tips=False)
        self.set_camera_orientation(phi=68*DEGREES,theta=-40*DEGREES,zoom=1.2,focal_distance=40,frame_center=ORIGIN)
        self.add(ax)
        self.set_camera_orientation(frame_center=ax.c2p(0,0,1.4))
        for txt,p in [("x",(2.85,0,0)),("y",(0,2.85,0)),("z",(0,0,3.75))]:
            m=MathTex(txt,font_size=38,color=GR).move_to(ax.c2p(*p)); self.add_fixed_orientation_mobjects(m)
        O=ax.c2p(0,0,0)
        tr=ValueTracker(0.001)
        P=lambda: ax.c2p(*r(tr.get_value()))
        curva=always_redraw(lambda: ParametricFunction(lambda t: ax.c2p(*r(t)),t_range=[0,tr.get_value(),0.05],color=AZ,stroke_width=5))
        sombra=always_redraw(lambda: ParametricFunction(lambda t: ax.c2p(r(t)[0],r(t)[1],0),t_range=[0,tr.get_value(),0.05],color=GC,stroke_width=2.5))
        caida=always_redraw(lambda: DashedLine(P(),ax.c2p(r(tr.get_value())[0],r(tr.get_value())[1],0),color=GC,stroke_width=2,dash_length=0.08))
        pos=always_redraw(lambda: Arrow3D(O,P(),color=AZ,thickness=0.018,height=0.22,base_radius=0.07,resolution=8))
        vel=always_redraw(lambda: Arrow3D(P(),P()+0.55*(ax.c2p(*dr(tr.get_value()))-O),color=NA,thickness=0.018,height=0.22,base_radius=0.07,resolution=8))
        dot=always_redraw(lambda: Dot3D(P(),color=AZ,radius=0.07))
        self.add(sombra,caida,curva,pos,vel,dot)

        tit=MathTex(r"\vec r(t)=\big(x(t),\,y(t),\,z(t)\big)",font_size=38).to_corner(UL,buff=0.35)
        ley=VGroup(
            Tex(r"$\vec r(t)$: vector posición",font_size=30,color=AZ),
            Tex(r"$\vec r\,'(t)$: vector velocidad (tangente)",font_size=30,color=NA),
            Tex(r"sombra en el plano $XY$",font_size=30,color=GC)).arrange(DOWN,aligned_edge=LEFT,buff=0.15).to_corner(DL,buff=0.35)
        self.add_fixed_in_frame_mobjects(tit,ley)
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(tr.animate.set_value(T),run_time=12,rate_func=linear)
        self.stop_ambient_camera_rotation()
        self.wait(1.5)

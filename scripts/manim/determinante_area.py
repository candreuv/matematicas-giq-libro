from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"; GR="#555555"
class DeterminanteArea(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK); Tex.set_default(color=BLACK)
        pl=NumberPlane(x_range=[-3,5,1],y_range=[-1,4,1],x_length=7.2,y_length=4.5,background_line_style={"stroke_color":GR,"stroke_opacity":0.15},axis_config={"color":GR}).shift(LEFT*2.6+DOWN*0.6)
        self.add(pl)
        u=ValueTracker(np.array([2.0,0.5])) if False else None
        ux,uy,vx,vy=[ValueTracker(t) for t in (2.0,0.5,0.5,1.5)]
        U=lambda: np.array([ux.get_value(),uy.get_value()]); V=lambda: np.array([vx.get_value(),vy.get_value()])
        c=lambda p: pl.c2p(p[0],p[1])
        par=always_redraw(lambda: Polygon(c((0,0)),c(U()),c(U()+V()),c(V()),color=VE,fill_opacity=0.35,stroke_width=2))
        au=always_redraw(lambda: Arrow(c((0,0)),c(U()),buff=0,color=AZ,stroke_width=6))
        av=always_redraw(lambda: Arrow(c((0,0)),c(V()),buff=0,color=NA,stroke_width=6))
        det=lambda: U()[0]*V()[1]-U()[1]*V()[0]
        mat=always_redraw(lambda: MathTex(r"\det\begin{pmatrix}%.1f&%.1f\\%.1f&%.1f\end{pmatrix}=%.2f"%(U()[0],V()[0],U()[1],V()[1],det()),font_size=36).to_corner(UR).shift(LEFT*0.1))
        lu=always_redraw(lambda: MathTex(r"\mathbf u",color=AZ,font_size=36).next_to(c(U()),DR,buff=0.05))
        lv=always_redraw(lambda: MathTex(r"\mathbf v",color=NA,font_size=36).next_to(c(V()),UL,buff=0.05))
        self.add(par,au,av,lu,lv,mat)
        cap=Tex(r"Área del paralelogramo $=|\det|$",font_size=34,color=VE).next_to(mat,DOWN,buff=0.5).align_to(mat,RIGHT)
        self.play(FadeIn(cap)); self.wait(1)
        def say(t):
            n=Tex(t,font_size=32).next_to(cap,DOWN,buff=0.4).align_to(mat,RIGHT); return n
        s1=say(r"$\mathbf v\gets\mathbf v+\lambda\mathbf u$: área igual"); self.play(FadeIn(s1))
        self.play(vx.animate.set_value(0.5+2*1.0),vy.animate.set_value(1.5+0.5*1.0),run_time=2)
        self.play(vx.animate.set_value(0.5-2*0.8),vy.animate.set_value(1.5-0.5*0.8),run_time=2.5)
        self.play(vx.animate.set_value(0.5),vy.animate.set_value(1.5),run_time=1.2); self.play(FadeOut(s1))
        s2=say(r"$\mathbf u\gets2\mathbf u$: área $\times2$"); self.play(FadeIn(s2))
        self.play(ux.animate.set_value(4.0),uy.animate.set_value(1.0),run_time=1.8); self.wait(0.8)
        self.play(ux.animate.set_value(2.0),uy.animate.set_value(0.5),run_time=1.2); self.play(FadeOut(s2))
        s3=say(r"$\mathbf u\leftrightarrow\mathbf v$: cambia el signo"); self.play(FadeIn(s3))
        self.play(ux.animate.set_value(0.5),uy.animate.set_value(1.5),vx.animate.set_value(2.0),vy.animate.set_value(0.5),run_time=2); self.wait(0.8)
        self.play(FadeOut(s3))
        s4=say(r"$\mathbf v$ paralelo a $\mathbf u$: área $0$"); self.play(FadeIn(s4))
        self.play(vx.animate.set_value(1.0),vy.animate.set_value(3.0),run_time=2); self.wait(2)

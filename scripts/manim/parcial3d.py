from manim import *
import numpy as np
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"
f = lambda x, y: 3 - 0.35 * x ** 2 - 0.2 * y ** 2 + 0.25 * x * y * 0
fx = lambda x, y: -0.7 * x
fy = lambda x, y: -0.4 * y
X0, Y0 = 1.0, 1.0

class Parcial3D(ThreeDScene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax = ThreeDAxes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], z_range=[0, 3.5, 1], x_length=6, y_length=6, z_length=3.5,
                        axis_config={"color": GRIS, "include_tip": True, "include_ticks": False}).shift(IN * 1.0)
        lx = MathTex("x", font_size=36).move_to(ax.c2p(3.4, 0, 0)); ly = MathTex("y", font_size=36).move_to(ax.c2p(0, 3.4, 0)); lz = MathTex("z", font_size=36).move_to(ax.c2p(0, 0, 3.9))
        self.set_camera_orientation(phi=68 * DEGREES, theta=-50 * DEGREES, zoom=1.1)
        sup = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=[-2.2, 2.2], v_range=[-2.2, 2.2], resolution=(24, 24),
                      fill_opacity=0.55, checkerboard_colors=["#9ecae1", "#c6dbef"], stroke_color=AZUL, stroke_width=0.4)
        for m in (lx, ly, lz): self.add_fixed_orientation_mobjects(m)
        self.add(ax)
        self.play(Create(sup), run_time=1.5)
        tit = MathTex(r"z=f(x,y)", font_size=34, color=AZUL).to_corner(UL, buff=0.35)
        self.add_fixed_in_frame_mobjects(tit); self.play(FadeIn(tit))
        # plane y = Y0
        pl = Polygon(ax.c2p(-2.8, Y0, 0), ax.c2p(2.8, Y0, 0), ax.c2p(2.8, Y0, 3.4), ax.c2p(-2.8, Y0, 3.4), fill_color=NARANJA, fill_opacity=0.18, stroke_color=NARANJA, stroke_width=1.5)
        cur = ParametricFunction(lambda s: ax.c2p(s, Y0, f(s, Y0)), t_range=[-2.2, 2.2], color=NARANJA, stroke_width=5)
        e1 = MathTex(r"\text{plano } y=y_0:\ \text{curva } z=f(x,y_0)", font_size=30, color=NARANJA).to_corner(UR, buff=0.35)
        self.add_fixed_in_frame_mobjects(e1)
        self.play(FadeIn(pl), Create(cur), FadeIn(e1), run_time=1.5)
        xt = ValueTracker(-1.8)
        dot = always_redraw(lambda: Dot3D(ax.c2p(xt.get_value(), Y0, f(xt.get_value(), Y0)), color=BLACK, radius=0.07))
        tan = always_redraw(lambda: Line3D(ax.c2p(xt.get_value() - 0.9, Y0, f(xt.get_value(), Y0) - 0.9 * fx(xt.get_value(), Y0)),
                                           ax.c2p(xt.get_value() + 0.9, Y0, f(xt.get_value(), Y0) + 0.9 * fx(xt.get_value(), Y0)), color=BLACK, thickness=0.02))
        e2 = MathTex(r"\text{pendiente de la tangente} = \frac{\partial f}{\partial x}(x,y_0)", font_size=30).next_to(e1, DOWN, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(e2)
        self.add(dot, tan); self.play(FadeIn(e2), run_time=0.5)
        self.play(xt.animate.set_value(1.8), run_time=4, rate_func=smooth)
        self.wait(0.5)
        self.play(FadeOut(pl), FadeOut(cur), FadeOut(dot), FadeOut(tan), FadeOut(e1), FadeOut(e2))
        # plane x = X0
        pl2 = Polygon(ax.c2p(X0, -2.8, 0), ax.c2p(X0, 2.8, 0), ax.c2p(X0, 2.8, 3.4), ax.c2p(X0, -2.8, 3.4), fill_color=VERDE, fill_opacity=0.18, stroke_color=VERDE, stroke_width=1.5)
        cur2 = ParametricFunction(lambda s: ax.c2p(X0, s, f(X0, s)), t_range=[-2.2, 2.2], color=VERDE, stroke_width=5)
        e3 = MathTex(r"\text{plano } x=x_0:\ \text{curva } z=f(x_0,y)", font_size=30, color=VERDE).to_corner(UR, buff=0.35)
        e4 = MathTex(r"\text{pendiente de la tangente} = \frac{\partial f}{\partial y}(x_0,y)", font_size=30).next_to(e3, DOWN, aligned_edge=RIGHT)
        self.add_fixed_in_frame_mobjects(e3, e4); self.remove(e3, e4)
        self.play(FadeIn(pl2), Create(cur2), FadeIn(e3), run_time=1.5)
        yt = ValueTracker(-1.8)
        dot2 = always_redraw(lambda: Dot3D(ax.c2p(X0, yt.get_value(), f(X0, yt.get_value())), color=BLACK, radius=0.07))
        tan2 = always_redraw(lambda: Line3D(ax.c2p(X0, yt.get_value() - 0.9, f(X0, yt.get_value()) - 0.9 * fy(X0, yt.get_value())),
                                            ax.c2p(X0, yt.get_value() + 0.9, f(X0, yt.get_value()) + 0.9 * fy(X0, yt.get_value())), color=BLACK, thickness=0.02))
        self.add(dot2, tan2); self.play(FadeIn(e4), run_time=0.5)
        self.play(yt.animate.set_value(1.8), run_time=4, rate_func=smooth)
        self.wait(2)

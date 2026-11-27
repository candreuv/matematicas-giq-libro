from manim import *
import numpy as np
from scipy.integrate import quad
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"
f = lambda x, y: 1.2 + 0.25 * x * (3 - x) + 0.35 * np.sin(1.6 * y) + 0.15 * y
A, B, C, D = 0, 3, 0, 2

class Fubini(ThreeDScene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax = ThreeDAxes(x_range=[0, 3.6, 1], y_range=[0, 2.6, 1], z_range=[0, 3, 1], x_length=5.4, y_length=3.9, z_length=3.2,
                        axis_config={"color": GRIS, "include_tip": True, "include_ticks": False}).shift(IN * 1.2)
        lx = MathTex("x", font_size=34).move_to(ax.c2p(3.9, 0, 0)); ly = MathTex("y", font_size=34).move_to(ax.c2p(-0.35, 2.9, 0)); lz = MathTex("z", font_size=34).move_to(ax.c2p(0, 0, 3.3))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-55 * DEGREES, zoom=1.05)
        for m in (lx, ly, lz): self.add_fixed_orientation_mobjects(m)
        base = Polygon(ax.c2p(A, C, 0), ax.c2p(B, C, 0), ax.c2p(B, D, 0), ax.c2p(A, D, 0), fill_color=GRIS, fill_opacity=0.25, stroke_color=GRIS, stroke_width=2)
        sup = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=[A, B], v_range=[C, D], resolution=(18, 12),
                      fill_opacity=0.45, checkerboard_colors=["#9ecae1", "#c6dbef"], stroke_color=AZUL, stroke_width=0.4)
        tit = MathTex(r"V=\iint_R f(x,y)\,dA", font_size=34).to_corner(UL, buff=0.3)
        self.add_fixed_in_frame_mobjects(tit); self.remove(tit)
        self.add(ax); self.play(FadeIn(base), Create(sup), FadeIn(tit), run_time=2)
        xt = ValueTracker(0.15)
        def corte():
            x = xt.get_value(); ys = np.linspace(C, D, 30)
            pts = [ax.c2p(x, C, 0)] + [ax.c2p(x, y, f(x, y)) for y in ys] + [ax.c2p(x, D, 0)]
            return Polygon(*pts, fill_color=NARANJA, fill_opacity=0.8, stroke_color=NARANJA, stroke_width=2)
        sec = always_redraw(corte)
        e1 = MathTex(r"A(x)=\int_c^d f(x,y)\,dy", font_size=32, color=NARANJA).to_corner(UR, buff=0.3)
        val = always_redraw(lambda: MathTex(r"x=%.2f,\ A(x)=%.2f" % (xt.get_value(), quad(lambda y: f(xt.get_value(), y), C, D)[0]), font_size=28, color=NARANJA).next_to(e1, DOWN, aligned_edge=RIGHT))
        self.add_fixed_in_frame_mobjects(e1); self.remove(e1)
        self.add(sec); self.play(FadeIn(e1), run_time=0.6)
        self.add_fixed_in_frame_mobjects(val)
        self.play(xt.animate.set_value(2.85), run_time=5, rate_func=smooth)
        self.remove(val)
        e2 = MathTex(r"V=\int_a^b A(x)\,dx=\int_a^b\!\!\int_c^d f(x,y)\,dy\,dx", font_size=32).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(e2); self.remove(e2)
        self.play(FadeOut(sec), FadeIn(e2))
        yt = ValueTracker(0.1)
        def corte2():
            y = yt.get_value(); xs = np.linspace(A, B, 30)
            pts = [ax.c2p(A, y, 0)] + [ax.c2p(x, y, f(x, y)) for x in xs] + [ax.c2p(B, y, 0)]
            return Polygon(*pts, fill_color=VERDE, fill_opacity=0.8, stroke_color=VERDE, stroke_width=2)
        sec2 = always_redraw(corte2)
        e3 = MathTex(r"\text{o cortando en } y:\ \int_c^d\!\!\int_a^b f\,dx\,dy", font_size=30, color=VERDE).to_corner(UR, buff=0.3)
        self.add_fixed_in_frame_mobjects(e3); self.remove(e3)
        self.add(sec2); self.play(FadeOut(e1), FadeIn(e3))
        self.play(yt.animate.set_value(1.9), run_time=4, rate_func=smooth)
        self.wait(2)

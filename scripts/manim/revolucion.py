from manim import *
import numpy as np
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; GRIS = "#555555"
f = lambda x: 0.9 * np.sqrt(x) + 0.3

class Revolucion(ThreeDScene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ax = ThreeDAxes(x_range=[0, 4.6, 1], y_range=[-2.6, 2.6, 1], z_range=[-2.6, 2.6, 1], x_length=6.5, y_length=5, z_length=5,
                        axis_config={"color": GRIS, "include_tip": False, "include_ticks": False})
        self.set_camera_orientation(phi=90 * DEGREES, theta=-90 * DEGREES, zoom=0.95)
        tit = MathTex(r"V=\pi\int_a^b f(x)^2\,dx", font_size=36).to_corner(UL, buff=0.3)
        self.add_fixed_in_frame_mobjects(tit); self.remove(tit)
        g = ParametricFunction(lambda t: ax.c2p(t, f(t), 0), t_range=[0, 4], color=AZUL, stroke_width=5)
        reg = Polygon(*[ax.c2p(t, f(t), 0) for t in np.linspace(0, 4, 40)], ax.c2p(4, 0, 0), ax.c2p(0, 0, 0),
                      fill_color=AZUL, fill_opacity=0.3, stroke_width=0)
        self.add(ax); self.play(Create(g), FadeIn(reg), FadeIn(tit), run_time=1.2)
        self.wait(0.5)
        self.move_camera(phi=70 * DEGREES, theta=-60 * DEGREES, run_time=2)
        sup = Surface(lambda u, v: ax.c2p(u, f(u) * np.cos(v), f(u) * np.sin(v)), u_range=[0.04, 4], v_range=[0, TAU], resolution=(16, 32),
                      fill_opacity=0.35, checkerboard_colors=["#9ecae1", "#c6dbef"], stroke_color=AZUL, stroke_width=0.3)
        self.play(Create(sup), FadeOut(reg), run_time=2.5)
        xt = ValueTracker(0.4); dx = 0.3
        def disco():
            x = xt.get_value(); r = f(x)
            return Cylinder(radius=ax.x_length / 4.6 * 0 + r * ax.y_length / 5.2, height=dx * ax.x_length / 4.6, direction=RIGHT,
                            fill_color=NARANJA, fill_opacity=0.7, stroke_width=0, resolution=(1, 32)).move_to(ax.c2p(x, 0, 0))
        d = always_redraw(disco)
        lab = MathTex(r"\text{disco: } dV=\pi f(x)^2\,dx", font_size=32, color=NARANJA).to_corner(UR, buff=0.3)
        self.add_fixed_in_frame_mobjects(lab); self.remove(lab)
        self.add(d); self.play(FadeIn(lab), run_time=0.6)
        self.play(xt.animate.set_value(3.7), run_time=4, rate_func=smooth)
        self.begin_ambient_camera_rotation(rate=0.25)
        self.wait(2.5)

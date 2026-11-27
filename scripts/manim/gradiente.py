from manim import *
import numpy as np
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"; ROJO = "#c0392b"
f = lambda x, y: x ** 2 + 2 * y ** 2
P = np.array([1.0, 0.5]); G = np.array([2 * P[0], 4 * P[1]]); NG = np.linalg.norm(G); ang0 = np.arctan2(G[1], G[0])

class Gradiente(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        pl = NumberPlane(x_range=[-2.2, 2.2, 1], y_range=[-1.7, 1.7, 1], x_length=6.0, y_length=4.64,
                         background_line_style={"stroke_color": "#dddddd", "stroke_width": 1}, axis_config={"color": GRIS}).to_edge(LEFT, buff=0.4).shift(DOWN * 0.3)
        niv = VGroup(*[ParametricFunction(lambda t, c=c: pl.c2p(np.sqrt(c) * np.cos(t), np.sqrt(c / 2) * np.sin(t)), t_range=[0, TAU], color=AZUL, stroke_width=2, stroke_opacity=0.7) for c in [0.25, 0.75, 1.5, 2.5, 3.75]])
        tit = MathTex(r"f(x,y)=x^2+2y^2,\quad P=(1,\,0.5)", font_size=30).to_corner(UL, buff=0.3)
        self.add(pl); self.play(Create(niv), FadeIn(tit), run_time=1.2)
        p = pl.c2p(*P); sc = 0.55
        grad = Arrow(p, pl.c2p(*(P + sc * G / NG * 2.2)), buff=0, color=ROJO, stroke_width=5, max_tip_length_to_length_ratio=0.15)
        eg = MathTex(r"\nabla f(P)=(2,2)", font_size=28, color=ROJO).next_to(grad.get_end(), UP, buff=0.1)
        self.play(FadeIn(Dot(p, color=BLACK)), GrowArrow(grad), FadeIn(eg))
        # right: graph of D_u vs angle
        ax = Axes(x_range=[0, 360, 90], y_range=[-3, 3, 1], x_length=5.2, y_length=3.4, axis_config={"color": GRIS, "include_tip": False, "font_size": 20},
                  x_axis_config={"numbers_to_include": [90, 180, 270, 360]}, y_axis_config={"numbers_to_include": [-2, 2]}).to_edge(RIGHT, buff=0.35).shift(DOWN * 0.6)
        for l in ax.get_x_axis().numbers + ax.get_y_axis().numbers: l.set_color(GRIS)
        lx = MathTex(r"\theta\ (^\circ)", font_size=24, color=GRIS).next_to(ax.x_axis, DOWN, buff=0.35).shift(RIGHT * 2.2)
        ly = MathTex(r"D_{\mathbf u}f(P)", font_size=26, color=NARANJA).next_to(ax, UP, buff=0.05).shift(LEFT * 1.6)
        top = DashedLine(ax.c2p(0, NG), ax.c2p(360, NG), color=ROJO, stroke_width=1.5); bot = DashedLine(ax.c2p(0, -NG), ax.c2p(360, -NG), color=ROJO, stroke_width=1.5)
        et = MathTex(r"\|\nabla f\|=2\sqrt2", font_size=22, color=ROJO).next_to(top, UP, buff=0.04).align_to(top, RIGHT)
        self.play(Create(ax), FadeIn(lx), FadeIn(ly), Create(top), Create(bot), FadeIn(et), run_time=1)
        th = ValueTracker(0.0)
        uvec = always_redraw(lambda: Arrow(p, pl.c2p(*(P + 1.0 * np.array([np.cos(np.radians(th.get_value())), np.sin(np.radians(th.get_value()))]))), buff=0, color=NARANJA, stroke_width=5, max_tip_length_to_length_ratio=0.2))
        traza = always_redraw(lambda: ax.plot(lambda d: NG * np.cos(np.radians(d) - ang0), x_range=[0, max(th.get_value(), 0.5)], color=NARANJA, stroke_width=4))
        pto = always_redraw(lambda: Dot(ax.c2p(th.get_value(), NG * np.cos(np.radians(th.get_value()) - ang0)), color=NARANJA))
        def lectura():
            d = NG * np.cos(np.radians(th.get_value()) - ang0)
            return MathTex(r"D_{\mathbf u}f(P)=\nabla f\cdot\mathbf u=\|\nabla f\|\cos\varphi=%5.2f" % d, font_size=28, color=NARANJA).to_edge(DOWN, buff=0.25)
        lec = always_redraw(lectura)
        self.add(uvec, traza, pto, lec)
        self.play(th.animate.set_value(45), run_time=2, rate_func=linear)
        nota = MathTex(r"\text{máximo: } \mathbf u \text{ en la dirección de } \nabla f", font_size=26, color=ROJO).to_edge(UP, buff=0.9).shift(RIGHT * 3.3)
        self.play(FadeIn(nota)); self.wait(1)
        self.play(th.animate.set_value(135), run_time=2.4, rate_func=linear)
        nota2 = MathTex(r"\mathbf u \perp \nabla f:\ \text{tangente a la curva de nivel},\ D_{\mathbf u}f=0", font_size=26, color=AZUL).move_to(nota)
        self.play(ReplacementTransform(nota, nota2)); self.wait(1)
        self.play(th.animate.set_value(225), run_time=2.4, rate_func=linear)
        nota3 = MathTex(r"\text{mínimo: } \mathbf u=-\nabla f/\|\nabla f\|", font_size=26, color=ROJO).move_to(nota)
        self.play(ReplacementTransform(nota2, nota3)); self.wait(1)
        self.play(th.animate.set_value(360), run_time=3, rate_func=linear)
        self.wait(2)

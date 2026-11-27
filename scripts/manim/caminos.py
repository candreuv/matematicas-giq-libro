from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"
VERDE = "#1e8449"

f = lambda x, y: x * y / (x ** 2 + y ** 2)


class Caminos(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        L = 5.6
        fondo = ImageMobject("fondo_xy.png").set_height(L).to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        O = fondo.get_center()
        s = L / 2
        ejeX = Line(O + LEFT * s, O + RIGHT * s, color=GRIS, stroke_width=1.5)
        ejeY = Line(O + DOWN * s, O + UP * s, color=GRIS, stroke_width=1.5)
        self.add(fondo, ejeX, ejeY)
        tit = MathTex(r"f(x,y) = \frac{xy}{x^2+y^2}", font_size=40).to_corner(UR, buff=0.4).shift(LEFT * 0.4)
        leyenda = VGroup(Tex(r"rojo: $f>0$", font_size=26, color="#b40426"), Tex(r"azul: $f<0$", font_size=26, color="#3b4cc0")).arrange(RIGHT, buff=0.4).next_to(tit, DOWN, buff=0.2)
        self.play(FadeIn(tit), FadeIn(leyenda), run_time=0.6)
        X = 1.5
        cab = Tex(r"Hacia $(0,0)$ por la recta $y = mx$:", font_size=28).move_to([X, 1.55, 0], aligned_edge=LEFT)
        self.play(FadeIn(cab), run_time=0.4)
        filas = VGroup()
        for i, m in enumerate([0, 1, -1, 3]):
            ang = np.arctan(m)
            d = np.array([np.cos(ang), np.sin(ang), 0])
            linea = DashedLine(O - d * s * 0.98, O + d * s * 0.98, color=GRIS, stroke_width=2)
            self.play(Create(linea), run_time=0.4)
            tr = ValueTracker(0.95)
            p1 = always_redraw(lambda: Dot(O + d * s * tr.get_value(), color=VERDE, radius=0.09))
            p2 = always_redraw(lambda: Dot(O - d * s * tr.get_value(), color=VERDE, radius=0.09))
            self.add(p1, p2)
            self.play(tr.animate.set_value(0.03), run_time=1.6, rate_func=rate_functions.ease_in_quad)
            val = m / (1 + m ** 2)
            fila = MathTex(r"y = %s:\qquad f \to \frac{%g}{1+%g} = %s" % ({0: "0", 1: "x", -1: "-x", 3: "3x"}[m], m, m * m, {0: "0", 1: "0.5", -1: "-0.5", 3: "0.3"}[m]), font_size=30)
            fila.move_to([X, 0.85 - 0.7 * i, 0], aligned_edge=LEFT)
            self.play(FadeIn(fila), run_time=0.5)
            self.remove(p1, p2)
            self.play(FadeOut(linea), run_time=0.2)
            filas.add(fila)
        concl = VGroup(Tex(r"El valor depende del camino:", font_size=30),
                       MathTex(r"f(x, mx) = \frac{m}{1+m^2}", font_size=34),
                       Tex(r"$\Rightarrow$ el límite en $(0,0)$ \textbf{no existe}", font_size=30, color=NARANJA)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        concl.scale(0.9).move_to([X, -2.75, 0], aligned_edge=LEFT)
        self.play(FadeIn(concl), run_time=0.8)
        self.wait(3)

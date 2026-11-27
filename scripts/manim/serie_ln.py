from manim import *
import numpy as np
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; VERDE = "#1e8449"; GRIS = "#555555"

def S(n):
    return lambda x: sum((-1) ** (k + 1) * x ** k / k for k in range(1, n + 1))

class SerieLn(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[-1.5, 2, 0.5], y_range=[-3, 2, 1], x_length=10, y_length=5.0,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 22},
                    x_axis_config={"numbers_to_include": [2], "decimal_number_config": {"num_decimal_places": 0}}, y_axis_config={"numbers_to_include": [-2, -1, 1]}).shift(DOWN * 0.45 + LEFT * 0.3)
        for l in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers: l.set_color(GRIS)
        zona = Rectangle(width=ejes.c2p(1, 0)[0] - ejes.c2p(-1, 0)[0], height=5.0, fill_color=VERDE, fill_opacity=0.10, stroke_width=0).move_to([(ejes.c2p(1, 0)[0] + ejes.c2p(-1, 0)[0]) / 2, ejes.c2p(0, -0.5)[1], 0])
        bordes = VGroup(DashedLine(ejes.c2p(-1, -3), ejes.c2p(-1, 2), color=VERDE), DashedLine(ejes.c2p(1, -3), ejes.c2p(1, 2), color=VERDE))
        n1 = VGroup(MathTex("-1", font_size=24, color=GRIS).next_to(ejes.c2p(-1, 0), DL, buff=0.08), MathTex("1", font_size=24, color=GRIS).next_to(ejes.c2p(1, 0), DR, buff=0.08))
        etiq = MathTex(r"\text{convergencia: } (-1,\,1]", font_size=28, color=VERDE).next_to(zona, UP, buff=0.1)
        f = ejes.plot(lambda x: np.log(1 + x), x_range=[-0.95, 2], color=AZUL, stroke_width=5)
        tit = MathTex(r"\ln(1+x)=\sum_{k=1}^{\infty}\frac{(-1)^{k+1}}{k}\,x^k", font_size=32, color=AZUL).to_corner(UL, buff=0.3)
        self.add(ejes, n1); self.play(Create(f), FadeIn(tit), run_time=1.2)
        self.play(FadeIn(zona), Create(bordes), FadeIn(etiq), run_time=0.8)
        cur = None; lab = None
        for n in [1, 2, 3, 4, 5, 6, 8, 10, 14, 20, 30]:
            s = S(n)
            xs = np.arange(-1.5, 2.0001, 0.005); ok = [(-3 <= s(t) <= 2) for t in xs]
            runs = []; i = 0
            while i < len(xs):
                if ok[i]:
                    j = i
                    while j + 1 < len(xs) and ok[j + 1]: j += 1
                    if j > i: runs.append((xs[i], xs[j]))
                    i = j + 1
                else: i += 1
            g = VGroup(*[ejes.plot(s, x_range=[a0, b0, 0.005], color=NARANJA, stroke_width=4, use_smoothing=False) for a0, b0 in runs])
            nl = MathTex(r"S_{%d}(x)" % n, font_size=34, color=NARANJA).to_corner(UR, buff=0.4)
            if cur is None: self.play(Create(g), FadeIn(nl), run_time=0.9)
            else: self.play(ReplacementTransform(cur, g), ReplacementTransform(lab, nl), run_time=0.8)
            cur, lab = g, nl; self.wait(0.5)
        nota = MathTex(r"\text{dentro de } (-1,1] \text{ las sumas parciales se pegan a } \ln(1+x);\ \text{fuera, divergen}", font_size=26).to_edge(DOWN, buff=0.12)
        self.play(FadeIn(nota)); self.wait(2.5)

from manim import *
import math

config.background_color = WHITE

AZUL = "#1f5fa8"
VERDE = "#1e8449"
ROJO = "#c0392b"
GRIS = "#555555"
BANDA = "#f9e79f"

N = 20
S = [0.0]
for n in range(1, N + 1):
    S.append(S[-1] + (-1) ** (n + 1) / n)
L = math.log(2)


class Alternada(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = MathTex(r"1 - \frac12 + \frac13 - \frac14 + \dots = \ln 2 \approx 0.693", font_size=38).to_edge(UP, buff=0.25)
        self.add(titulo)

        ejes = Axes(
            x_range=[0, N + 1, 5], y_range=[0.4, 1.05, 0.1],
            x_length=7.0, y_length=5.2,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(5, N + 1, 5)},
            y_axis_config={"numbers_to_include": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                           "decimal_number_config": {"num_decimal_places": 1}},
        ).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=0.8)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        et_n = MathTex("n", font_size=30).next_to(ejes.c2p(N + 1, 0.4), RIGHT, buff=0.15)
        self.add(ejes, et_n)

        lin = DashedLine(ejes.c2p(0, L), ejes.c2p(N + 1, L), color=ROJO, stroke_width=2.5)
        et = MathTex(r"\ln 2", font_size=28, color=ROJO).next_to(ejes.c2p(N + 1, L), RIGHT, buff=0.1)
        self.play(Create(lin), FadeIn(et), run_time=0.6)

        X_INFO = 2.25
        cab = Tex(r"Suma parcial y cota del error", font_size=26).move_to([X_INFO, 2.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(cab), run_time=0.4)

        prev = None
        caja = None
        txt = None
        for n in range(1, N + 1):
            p = Dot(ejes.c2p(n, S[n]), radius=0.065, color=AZUL)
            anims = [FadeIn(p, scale=0.5)]
            if prev is not None:
                anims.append(Create(Line(prev.get_center(), p.get_center(), color=AZUL, stroke_width=1.5)))
            # intervalo garantizado: S está entre S_n y S_n ± 1/(n+1)
            b = 1 / (n + 1)
            lo, hi = sorted([S[n], S[n] + (-1) ** n * b])
            nueva = Rectangle(width=0.18, height=max(ejes.c2p(0, hi)[1] - ejes.c2p(0, lo)[1], 0.01),
                              fill_color=BANDA, fill_opacity=0.9, stroke_color=VERDE, stroke_width=1.5)
            nueva.move_to(ejes.c2p(n + 0.5, (lo + hi) / 2))
            nueva.set_z_index(-1)
            nuevo_txt = VGroup(MathTex(rf"S_{{{n}}} = {S[n]:.4f}", font_size=30), MathTex(r"|S - S_{%d}| \leq \tfrac{1}{%d} \approx %.3f" % (n, n + 1, 1 / (n + 1)), font_size=30)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            nuevo_txt[0].set_color(AZUL)
            nuevo_txt[1].set_color(VERDE)
            nuevo_txt.move_to([X_INFO, 1.35, 0], aligned_edge=LEFT)
            if caja is None:
                caja, txt = nueva, nuevo_txt
                anims += [FadeIn(caja), FadeIn(txt)]
            else:
                anims += [Transform(caja, nueva), Transform(txt, nuevo_txt)]
            self.play(*anims, run_time=0.6 if n < 8 else 0.35)
            prev = p

        notas = VGroup(
            Tex(r"Las sumas parciales saltan por", font_size=25),
            Tex(r"encima y por debajo del límite,", font_size=25),
            Tex(r"cada vez más cerca.", font_size=25),
            Tex(r"El error es menor que el primer", font_size=25, color=VERDE),
            Tex(r"término no sumado: $\tfrac{1}{n+1}$.", font_size=25, color=VERDE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([X_INFO, -0.9, 0], aligned_edge=LEFT)
        self.play(FadeIn(notas), run_time=0.8)
        self.wait(3)

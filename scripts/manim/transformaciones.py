from manim import *

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"


class Transformaciones(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        ejes = Axes(x_range=[-3, 4, 1], y_range=[-1, 9, 1], x_length=6.0, y_length=6.2,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 24},
                    x_axis_config={"numbers_to_include": [-2, -1, 1, 2, 3]},
                    y_axis_config={"numbers_to_include": [2, 4, 6, 8]}).to_edge(LEFT, buff=0.6).shift(DOWN * 0.2)
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        self.add(ejes)

        def par(h, a, k, color=NARANJA, w=4):
            return ejes.plot(lambda x: a * (x - h) ** 2 + k, x_range=[-3, 4], color=color, stroke_width=w, use_smoothing=True).set_z_index(1)

        def recortar(m):
            return m

        base = ejes.plot(lambda x: x ** 2, x_range=[-3, 3], color=AZUL, stroke_width=3)
        base_dash = DashedVMobject(base.copy().set_color(AZUL).set_stroke(width=2), num_dashes=40)
        f0 = MathTex(r"f(x) = x^2", font_size=36, color=AZUL).move_to([3.3, 3.0, 0], aligned_edge=LEFT)
        self.play(Create(base), FadeIn(f0), run_time=1.2)
        self.wait(0.5)

        X = 2.4
        pasos = [
            (r"f(x-1) = (x-1)^2", r"\text{1 a la \textbf{derecha}}", 1, 1, 0),
            (r"2f(x-1) = 2(x-1)^2", r"\text{estirada verticalmente} \times 2", 1, 2, 0),
            (r"2f(x-1)+3 = 2(x-1)^2 + 3", r"\text{3 hacia \textbf{arriba}}", 1, 2, 3),
        ]
        actual = base.copy().set_color(NARANJA).set_stroke(width=4)
        self.add(base_dash)
        self.remove(base)
        self.add(actual)
        vert = Dot(ejes.c2p(0, 0), color=NARANJA, radius=0.08).set_z_index(2)
        self.add(vert)
        y0 = 1.8
        textos = []
        for i, (ec, desc, h, a, k) in enumerate(pasos):
            t1 = MathTex(ec, font_size=32, color=NARANJA)
            t2 = MathTex(desc, font_size=28, color=GRIS)
            g = VGroup(t1, t2).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([X, y0 - 1.25 * i, 0], aligned_edge=LEFT)
            nueva = ejes.plot(lambda x, h=h, a=a, k=k: a * (x - h) ** 2 + k,
                              x_range=[h - ((9 - k) / a) ** 0.5, h + ((9 - k) / a) ** 0.5],
                              color=NARANJA, stroke_width=4)
            if textos:
                self.play(textos[-1].animate.set_opacity(0.45), run_time=0.3)
            self.play(FadeIn(g), run_time=0.6)
            self.play(Transform(actual, nueva), vert.animate.move_to(ejes.c2p(h, k)), run_time=1.6)
            textos.append(g)
            self.wait(0.7)

        aviso = VGroup(Tex(r"Cuidado: $f(x-c)$ con $c>0$ desplaza", font_size=26),
                       Tex(r"a la \textbf{derecha}: el vértice pasa a $x=c$.", font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        aviso.move_to([X, -2.6, 0], aligned_edge=LEFT)
        vtx = MathTex(r"\text{vértice } (1,\ 3)", font_size=28, color=NARANJA).next_to(ejes.c2p(1, 3), DR, buff=0.12).shift(RIGHT * 0.2)
        self.play(FadeIn(aviso), FadeIn(vtx), run_time=0.8)
        self.wait(3)

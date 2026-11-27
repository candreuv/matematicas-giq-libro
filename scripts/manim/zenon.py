from manim import *

config.background_color = WHITE

AZUL = "#1f5fa8"
VERDE = "#27ae60"
ROJO = "#c0392b"
GRIS = "#555555"
NARANJA = "#d35400"

PASOS = 8


class Zenon(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"La paradoja de Aquiles y la tortuga", font_size=38).to_edge(UP, buff=0.3)
        sub = Tex(r"La tortuga sale con 1 m de ventaja; Aquiles corre el doble de rápido", font_size=28, color=GRIS).next_to(titulo, DOWN, buff=0.15)
        self.add(titulo, sub)

        recta = NumberLine(x_range=[0, 2.2, 0.5], length=12, color=GRIS, include_numbers=True,
                           decimal_number_config={"num_decimal_places": 1, "color": GRIS}, font_size=26).shift(UP * 0.2)
        et_m = Tex(r"metros", font_size=24, color=GRIS).next_to(recta, RIGHT, buff=0.15).shift(DOWN * 0.35)
        self.add(recta, et_m)

        meta = DashedLine(recta.n2p(2) + UP * 1.3, recta.n2p(2) + DOWN * 0.5, color=ROJO, stroke_width=2.5)
        et_meta = Tex(r"punto de encuentro", font_size=22, color=ROJO).next_to(meta, UP, buff=0.05)

        aquiles = Dot(recta.n2p(0), radius=0.13, color=AZUL)
        et_a = Tex(r"Aquiles", font_size=24, color=AZUL).next_to(aquiles, UP, buff=0.15)
        tortuga = Square(side_length=0.24, color=VERDE, fill_color=VERDE, fill_opacity=1).move_to(recta.n2p(1))
        et_t = Tex(r"tortuga", font_size=24, color=VERDE).next_to(tortuga, DOWN, buff=0.95)
        self.play(FadeIn(aquiles), FadeIn(et_a), FadeIn(tortuga), FadeIn(et_t), run_time=0.8)

        suma = MathTex(r"D_0 = 1", font_size=40).move_to(DOWN * 2.55)
        tramos_txt = MathTex(r"1", font_size=36, color=NARANJA).move_to(DOWN * 1.75)

        pos_a, pos_t = 0.0, 1.0
        terminos = [r"1"]
        acum = 0.0
        tramos = VGroup()
        for k in range(PASOS):
            d = 0.5 ** k
            nuevo_a = pos_a + d
            nuevo_t = pos_t + d / 2
            seg = Line(recta.n2p(pos_a) + DOWN * 0.8, recta.n2p(nuevo_a) + DOWN * 0.8,
                       color=NARANJA, stroke_width=6)
            tramos.add(seg)
            acum += d
            if k > 0:
                terminos.append(rf"\tfrac{{1}}{{{2**k}}}")
            expr = " + ".join(terminos) if k < 5 else " + ".join(terminos[:5]) + r" + \cdots"
            nueva_suma = MathTex(rf"D_{{{k}}} = {acum:.4f}".rstrip("0").rstrip("."), font_size=40).move_to(suma)
            nuevo_tramos = MathTex(expr, font_size=36, color=NARANJA).move_to(tramos_txt)
            anims = [
                aquiles.animate.move_to(recta.n2p(nuevo_a)),
                tortuga.animate.move_to(recta.n2p(nuevo_t)),
                Create(seg),
            ]
            if k == 0:
                anims += [FadeIn(suma), FadeIn(tramos_txt)]
            else:
                anims += [Transform(suma, nueva_suma), Transform(tramos_txt, nuevo_tramos)]
            self.play(*anims, et_a.animate.next_to(recta.n2p(nuevo_a), UP, buff=0.28),
                      et_t.animate.next_to(recta.n2p(nuevo_t), DOWN, buff=1.0),
                      run_time=1.0 if k < 4 else 0.6)
            pos_a, pos_t = nuevo_a, nuevo_t
            if k == 1:
                self.play(Create(meta), FadeIn(et_meta), run_time=0.6)

        concl = MathTex(
            r"\sum_{k=0}^{\infty} \left(\tfrac12\right)^k = \frac{1}{1 - \frac12} = 2 \text{ m}",
            font_size=40, color=ROJO,
        ).move_to(DOWN * 3.3)
        nota = Tex(r"Infinitos tramos, pero una distancia (y un tiempo) finitos", font_size=28).move_to(DOWN * 2.45)
        self.play(FadeOut(suma), FadeIn(nota), FadeIn(concl), run_time=0.8)
        self.wait(3)

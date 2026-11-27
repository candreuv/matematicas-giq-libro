from manim import *

config.background_color = WHITE

AZUL = "#1f5fa8"
ROJO = "#c0392b"
GRIS = "#555555"
NARANJA = "#d35400"
POB = 8e9


def fmt(v):
    return f"{v:,.0f}".replace(",", ".")


class Ponzi(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"Esquema piramidal: cada miembro recluta a 3", font_size=36).to_edge(UP, buff=0.25)
        self.add(titulo)

        # --- Fase 1: árbol de los primeros niveles ---
        Y0, DY = 2.4, 0.95
        X_C = -3.2
        anchos = [0, 2.6, 4.6, 5.8, 6.3]
        niveles = []
        for n in range(5):
            m = 3 ** n
            if n == 0:
                xs = [X_C]
            else:
                w = anchos[n]
                xs = [X_C - w / 2 + w * j / (m - 1) for j in range(m)]
            r = [0.12, 0.1, 0.08, 0.045, 0.028][n]
            niveles.append([Dot([x, Y0 - n * DY, 0], radius=r, color=NARANJA if n == 0 else AZUL) for x in xs])

        X_INFO = 1.6
        tabla_cab = VGroup(Tex(r"nivel $n$", font_size=26), Tex(r"personas $3^n$", font_size=26), Tex(r"total $S_n$", font_size=26))
        cols = [X_INFO, X_INFO + 1.6, X_INFO + 3.6]
        for m, x in zip(tabla_cab, cols):
            m.move_to([x, 2.4, 0], aligned_edge=LEFT)
        self.play(FadeIn(tabla_cab), run_time=0.5)

        filas = VGroup()
        todas_lineas = VGroup()
        total = 0
        et_fund = Tex(r"fundador", font_size=22, color=NARANJA).next_to(niveles[0][0], LEFT, buff=0.15)
        for n in range(5):
            anims = [FadeIn(VGroup(*niveles[n]))]
            if n == 0:
                anims.append(FadeIn(et_fund))
            else:
                lineas = VGroup()
                for j, p in enumerate(niveles[n]):
                    padre = niveles[n - 1][j // 3]
                    lineas.add(Line(padre.get_center(), p.get_center(), color=GRIS, stroke_width=0.8 if n < 4 else 0.4))
                lineas.set_z_index(-1)
                todas_lineas.add(lineas)
                anims.append(Create(lineas))
            total += 3 ** n
            fila = VGroup(MathTex(str(n), font_size=28), MathTex(fmt(3 ** n), font_size=28), MathTex(fmt(total), font_size=28))
            for m, x in zip(fila, cols):
                m.move_to([x, 1.95 - 0.42 * n, 0], aligned_edge=LEFT)
            filas.add(fila)
            anims.append(FadeIn(fila))
            self.play(*anims, run_time=0.9)
        self.wait(0.6)

        # --- Fase 2: barra de población ---
        arbol = VGroup(*[d for nivel in niveles for d in nivel])
        nota = Tex(r"Seguimos sumando niveles\dots", font_size=30).move_to([X_INFO + 1.8, -0.4, 0])
        self.play(FadeIn(nota), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(VGroup(arbol, todas_lineas, et_fund, filas, tabla_cab, nota)), run_time=0.8)

        X0, ANCHO = -5.6, 9.0
        Y_BAR = -1.6
        marco = Rectangle(width=ANCHO, height=0.6, color=GRIS, stroke_width=2).move_to([X0 + ANCHO / 2, Y_BAR, 0])
        et_pob = Tex(r"población mundial ($\approx 8.000$ millones)", font_size=26, color=ROJO).next_to(marco, DOWN, buff=0.15)
        lim = DashedLine([X0 + ANCHO, Y_BAR + 0.6, 0], [X0 + ANCHO, Y_BAR - 0.6, 0], color=ROJO, stroke_width=3)
        self.play(Create(marco), FadeIn(et_pob), Create(lim), run_time=0.8)

        nivel_txt = MathTex(r"n = 4", font_size=44).move_to([0, 1.7, 0])
        total_txt = MathTex(r"S_4 = 121", font_size=44, color=AZUL).move_to([0, 0.85, 0])
        pct_txt = Tex(r"0\,\% de la población", font_size=32).move_to([0, 0.05, 0])
        self.play(FadeIn(nivel_txt), FadeIn(total_txt), FadeIn(pct_txt), run_time=0.5)

        barra = Rectangle(width=0.001, height=0.6, color=AZUL, fill_color=AZUL, fill_opacity=0.9, stroke_width=0)
        barra.move_to([X0, Y_BAR, 0], aligned_edge=LEFT)
        self.add(barra)

        for n in range(5, 22):
            S = (3 ** (n + 1) - 1) // 2
            frac = S / POB
            w = max(min(frac, 1.0) * ANCHO, 0.001)
            nb = Rectangle(width=w, height=0.6, color=ROJO if frac >= 1 else AZUL,
                           fill_color=ROJO if frac >= 1 else AZUL, fill_opacity=0.9, stroke_width=0)
            nb.move_to([X0, Y_BAR, 0], aligned_edge=LEFT)
            pct = frac * 100
            pct_s = f"{pct:.4f}".replace(".", ",") if pct < 0.01 else (f"{pct:.2f}".replace(".", ",") if pct < 10 else f"{pct:.0f}")
            self.play(Transform(barra, nb),
                      Transform(nivel_txt, MathTex(rf"n = {n}", font_size=44).move_to(nivel_txt)),
                      Transform(total_txt, MathTex(rf"S_{{{n}}} = {fmt(S)}", font_size=44, color=ROJO if frac >= 1 else AZUL).move_to(total_txt)),
                      Transform(pct_txt, Tex(rf"{pct_s}\,\% de la población", font_size=32).move_to(pct_txt)),
                      run_time=0.55 if n < 18 else 1.0)
            if n in (15, 19, 20):
                self.wait(0.5)

        concl = Tex(r"¡En el nivel 21 ya no quedan personas a las que reclutar!", font_size=30, color=ROJO).move_to([0, -3.3, 0])
        self.play(FadeIn(concl), run_time=0.8)
        self.wait(3)

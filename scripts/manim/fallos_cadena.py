from manim import *

config.background_color = WHITE

GRIS = "#555555"
ROJO = "#c0392b"
ROJO_CLARO = "#f5b7b1"
NARANJA = "#d35400"
MORADO = "#7d3c98"

N_PASOS = 7  # pasos 0..6  ->  1, 1, 2, 3, 5, 8, 13
TIPOS = ["R", "IC", "B", "CD", "T", "V"]
NOMBRES = {
    "R": "reactor",
    "IC": "intercambiador de calor",
    "B": "bomba",
    "CD": "columna de destilación",
    "T": "tanque",
    "V": "válvula",
}

ANCHO = 0.52
X_CENTRO = -2.0
Y0 = 2.35
DY = 0.86
SEP = 0.58


def construir_red():
    """Cada unidad afectada provoca un fallo en el paso siguiente y otro dos pasos después.
    Así, el número de unidades en el paso n es F_n = F_{n-1} + F_{n-2}."""
    filas = [[{"padre": None, "tipo": "R"}], [{"padre": (0, 0), "tipo": "IC"}]]
    k = 2
    for n in range(2, N_PASOS):
        hijos = []
        for i in range(len(filas[n - 1])):
            hijos.append({"padre": (n - 1, i), "salto": 1})
        for i in range(len(filas[n - 2])):
            hijos.append({"padre": (n - 2, i), "salto": 2})
        filas.append(hijos)
    # posiciones x: ordenar los hijos según la x del padre para evitar cruces
    xs = [[X_CENTRO]]
    xs.append([X_CENTRO])
    for n in range(2, N_PASOS):
        orden = sorted(range(len(filas[n])), key=lambda j: (xs[filas[n][j]["padre"][0]][filas[n][j]["padre"][1]], filas[n][j]["salto"]))
        filas[n] = [filas[n][j] for j in orden]
        m = len(filas[n])
        xs.append([X_CENTRO + (j - (m - 1) / 2) * SEP for j in range(m)])
        for h in filas[n]:
            h["tipo"] = TIPOS[k % len(TIPOS)]
            k += 1
    return filas, xs


class FallosCadena(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        filas, xs = construir_red()

        titulo = Tex(r"Propagación de un fallo en una planta química", font_size=36).to_edge(UP, buff=0.2)
        self.add(titulo)

        # Leyenda de equipos
        leyenda = VGroup(Tex(r"\textbf{Equipos}", font_size=26))
        for t in TIPOS:
            caja = RoundedRectangle(width=ANCHO, height=0.36, corner_radius=0.06, color=GRIS, stroke_width=2)
            et = Tex(t, font_size=20).move_to(caja)
            leyenda.add(VGroup(VGroup(caja, et), Tex(NOMBRES[t], font_size=22)).arrange(RIGHT, buff=0.15))
        leyenda.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_corner(UR, buff=0.4).shift(DOWN * 0.55)

        lin_1 = VGroup(Line(ORIGIN, RIGHT * 0.5, color=NARANJA, stroke_width=3),
                       Tex(r"afecta en el paso siguiente", font_size=20)).arrange(RIGHT, buff=0.12)
        lin_2 = VGroup(DashedLine(ORIGIN, RIGHT * 0.5, color=MORADO, stroke_width=3),
                       Tex(r"afecta dos pasos después", font_size=20)).arrange(RIGHT, buff=0.12)
        lineas_ley = VGroup(lin_1, lin_2).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(leyenda, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(FadeIn(leyenda), FadeIn(lineas_ley), run_time=0.8)

        contador = MathTex(r"F_0 = 1", font_size=40, color=ROJO).next_to(lineas_ley, DOWN, aligned_edge=LEFT, buff=0.45)
        etiq_paso = Tex(r"unidades afectadas en el paso", font_size=22).next_to(contador, UP, aligned_edge=LEFT, buff=0.1)

        cajas = []
        for n in range(N_PASOS):
            y = Y0 - n * DY
            fila_cajas = []
            for j, u in enumerate(filas[n]):
                caja = RoundedRectangle(width=ANCHO, height=0.4, corner_radius=0.06,
                                        color=ROJO, fill_color=ROJO_CLARO, fill_opacity=1, stroke_width=2.5)
                caja.move_to([xs[n][j], y, 0])
                et = Tex(u["tipo"], font_size=20).move_to(caja)
                g = VGroup(caja, et)
                g.set_z_index(1)
                fila_cajas.append(g)
            cajas.append(fila_cajas)

        etiq_n = [Tex(rf"paso {n}", font_size=22, color=GRIS).move_to([-6.45, Y0 - n * DY, 0]) for n in range(N_PASOS)]

        F = [len(f) for f in filas]
        for n in range(N_PASOS):
            anims = [FadeIn(etiq_n[n])]
            for j, u in enumerate(filas[n]):
                if u["padre"] is not None:
                    pn, pj = u["padre"]
                    a = cajas[pn][pj][0].get_bottom()
                    b = cajas[n][j][0].get_top()
                    if u.get("salto", 1) == 1:
                        lin = Line(a, b, color=NARANJA, stroke_width=2)
                    else:
                        lin = DashedLine(a, b, color=MORADO, stroke_width=2, dash_length=0.08)
                    lin.set_z_index(-1)
                    anims.append(Create(lin))
                anims.append(GrowFromCenter(cajas[n][j]))
            nuevo = MathTex(rf"F_{n} = {F[n]}", font_size=40, color=ROJO).move_to(contador, aligned_edge=LEFT)
            if n == 0:
                anims += [FadeIn(contador), FadeIn(etiq_paso)]
                self.play(*anims, run_time=1.0)
                nota = Tex(r"Fallo inicial de temperatura en el reactor", font_size=24, color=ROJO)
                nota.next_to(cajas[0][0], RIGHT, buff=0.25)
                self.play(FadeIn(nota), run_time=0.6)
                self.wait(0.6)
                self.play(FadeOut(nota), run_time=0.4)
            else:
                anims.append(Transform(contador, nuevo))
                self.play(*anims, run_time=1.1)
            self.wait(0.5)

        resumen = MathTex(r"1,\ 1,\ 2,\ 3,\ 5,\ 8,\ 13,\ \dots \qquad F_n = F_{n-1} + F_{n-2}",
                          font_size=34).to_edge(DOWN, buff=0.12).shift(LEFT * 2.0)
        self.play(FadeIn(resumen), run_time=0.8)
        self.wait(3)

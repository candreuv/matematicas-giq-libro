from manim import *
import math

config.background_color = WHITE

AZUL = "#1f5fa8"
GRIS = "#7f8c8d"
NARANJA = "#d35400"
VERDE = "#1e8449"
R = 0.075
APORTE = 200
T_APORTES = 10
T_FIN = 30


def V(t):
    """Valor real de la cartera en el instante t (años)."""
    if t <= T_APORTES:
        n = int(math.floor(t * 12 + 1e-9)) + 1  # aportaciones hechas hasta t (la primera en t = 0)
        n = min(n, 120)
        return sum(APORTE * math.exp(R * (t - j / 12)) for j in range(n))
    return V(T_APORTES) * math.exp(R * (t - T_APORTES))


def aportado(t):
    n = min(int(math.floor(t * 12 + 1e-9)) + 1, 120)
    return APORTE * n


def euros(v):
    return f"{v:,.0f}".replace(",", ".") + r"\ \text{€}"


class DCA(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"Aportaciones periódicas (DCA): 200 € al mes durante 10 años", font_size=32).to_edge(UP, buff=0.25)
        sub = Tex(r"Rentabilidad real del 7.5\,\% anual, capitalización continua (euros de hoy)", font_size=24, color=GRIS).next_to(titulo, DOWN, buff=0.1)
        self.add(titulo, sub)

        ejes = Axes(
            x_range=[0, T_FIN, 5], y_range=[0, 170000, 40000],
            x_length=7.4, y_length=5.0,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(5, T_FIN + 1, 5)},
        ).to_edge(DOWN, buff=0.55).to_edge(LEFT, buff=1.25)
        for lab in ejes.get_x_axis().numbers:
            lab.set_color(GRIS)
        marcas_y = VGroup(*[Tex(f"{k*40}\\,000", font_size=20, color=GRIS).next_to(ejes.c2p(0, k * 40000), LEFT, buff=0.1) for k in range(1, 5)])
        et_x = Tex(r"años", font_size=22, color=GRIS).next_to(ejes.c2p(T_FIN, 0), RIGHT, buff=0.15)
        self.add(ejes, marcas_y, et_x)

        fin_ap = DashedLine(ejes.c2p(T_APORTES, 0), ejes.c2p(T_APORTES, 170000), color=GRIS, stroke_width=1.5)
        et_fin = Tex(r"fin de las\\ aportaciones", font_size=20, color=GRIS).next_to(ejes.c2p(T_APORTES, 150000), RIGHT, buff=0.08)

        t = ValueTracker(0.001)

        def curva_valor():
            tt = t.get_value()
            xs = [k / 12 for k in range(int(tt * 12) + 1)] + [tt]
            pts = [ejes.c2p(x, V(x)) for x in xs]
            return VMobject(color=AZUL, stroke_width=3.5).set_points_as_corners(pts if len(pts) > 1 else pts * 2)

        def curva_aportado():
            tt = t.get_value()
            xs = [k / 12 for k in range(int(tt * 12) + 1)] + [tt]
            pts = []
            for x in xs:
                pts.append(ejes.c2p(x, aportado(x)))
            return VMobject(color=NARANJA, stroke_width=3).set_points_as_corners(pts if len(pts) > 1 else pts * 2)

        def relleno():
            tt = t.get_value()
            xs = [k / 6 for k in range(int(tt * 6) + 1)] + [tt]
            if len(xs) < 2:
                return VMobject()
            sup = [ejes.c2p(x, V(x)) for x in xs]
            inf = [ejes.c2p(x, aportado(x)) for x in reversed(xs)]
            return Polygon(*sup, *inf, fill_color=VERDE, fill_opacity=0.18, stroke_width=0)

        cv = always_redraw(curva_valor)
        ca = always_redraw(curva_aportado)
        rl = always_redraw(relleno)

        X_INFO = 2.6
        ley = VGroup(
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=AZUL, stroke_width=4), Tex(r"valor de la cartera", font_size=24)).arrange(RIGHT, buff=0.12),
            VGroup(Line(ORIGIN, RIGHT * 0.45, color=NARANJA, stroke_width=4), Tex(r"dinero aportado", font_size=24)).arrange(RIGHT, buff=0.12),
            VGroup(Square(0.28, fill_color=VERDE, fill_opacity=0.3, stroke_width=0), Tex(r"intereses generados", font_size=24)).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([X_INFO, 1.75, 0], aligned_edge=LEFT)

        info_t = always_redraw(lambda: Tex(f"Año {int(t.get_value() + 1e-6)}", font_size=30).move_to([X_INFO, 0.6, 0], aligned_edge=LEFT))
        info_v = always_redraw(lambda: MathTex(r"\text{Valor: }" + euros(V(t.get_value())), font_size=30, color=AZUL).move_to([X_INFO, 0.05, 0], aligned_edge=LEFT))
        info_a = always_redraw(lambda: MathTex(r"\text{Aportado: }" + euros(aportado(min(t.get_value(), 10))), font_size=30, color=NARANJA).move_to([X_INFO, -0.5, 0], aligned_edge=LEFT))

        self.add(rl, ca, cv, info_t, info_v, info_a)
        self.play(FadeIn(ley), run_time=0.6)
        self.play(t.animate.set_value(T_APORTES), run_time=5, rate_func=linear)
        p10 = Dot(ejes.c2p(T_APORTES, V(T_APORTES)), radius=0.06, color=AZUL)
        et10 = MathTex(euros(V(T_APORTES)), font_size=22, color=AZUL).next_to(p10, LEFT, buff=0.1).shift(UP * 0.2)
        self.play(Create(fin_ap), FadeIn(et_fin), FadeIn(p10), FadeIn(et10), run_time=0.6)
        self.wait(0.6)
        for meta in (20, 30):
            self.play(t.animate.set_value(meta), run_time=2.5, rate_func=linear)
            p = Dot(ejes.c2p(meta, V(meta)), radius=0.06, color=AZUL)
            et = MathTex(euros(V(meta)), font_size=22, color=AZUL).next_to(p, LEFT, buff=0.1).shift(UP * 0.15)
            self.play(FadeIn(p), FadeIn(et), run_time=0.4)
            self.wait(0.4)

        concl = VGroup(Tex(r"Con 24\,000 € aportados, a los 30 años", font_size=24), Tex(r"la cartera vale unas 6.7 veces más", font_size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([X_INFO, -1.55, 0], aligned_edge=LEFT)
        self.play(FadeIn(concl), run_time=0.8)
        self.wait(3)

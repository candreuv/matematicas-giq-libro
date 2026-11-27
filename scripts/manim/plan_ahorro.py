from manim import *
import math

config.background_color = WHITE

AZUL = "#1f5fa8"
VERDE = "#1e8449"
ROJO = "#c0392b"
GRIS = "#555555"
NARANJA = "#d35400"

R_REAL = 0.07
C0 = 1e6 / math.exp(R_REAL * 67)  # ~ 9186.69


def C(t):
    return C0 * math.exp(R_REAL * t)


def euros(v):
    s = f"{v:,.0f}".replace(",", ".")
    return s + r"\ \text{€}"


class PlanAhorro(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)

        titulo = Tex(r"Plan de ahorro: $C(t) = C_0\, e^{0.07\,t}$ \quad (euros de hoy)", font_size=34).to_edge(UP, buff=0.25)
        self.add(titulo)

        ejes = Axes(
            x_range=[0, 70, 10], y_range=[0, 1.1e6, 2e5],
            x_length=7.0, y_length=5.3,
            axis_config={"color": GRIS, "include_tip": False},
            x_axis_config={"numbers_to_include": range(10, 71, 10)},
        ).to_edge(DOWN, buff=0.55).to_edge(LEFT, buff=1.2)
        for lab in ejes.get_x_axis().numbers:
            lab.set_color(GRIS)
        marcas_y = VGroup(*[
            Tex(f"{k*200}\\,000", font_size=22, color=GRIS).next_to(ejes.c2p(0, k * 2e5), LEFT, buff=0.12)
            for k in range(1, 6)
        ])
        et_x = Tex(r"edad (años)", font_size=24, color=GRIS).next_to(ejes.c2p(35, 0), DOWN, buff=0.62)
        et_y = Tex(r"capital (€)", font_size=24, color=GRIS).next_to(ejes.c2p(0, 1.1e6), UP, buff=0.1)
        self.add(ejes, marcas_y, et_x, et_y)

        objetivo = DashedLine(ejes.c2p(0, 1e6), ejes.c2p(70, 1e6), color=ROJO, stroke_width=2.5)
        et_obj = Tex(r"objetivo: 1 millón", font_size=24, color=ROJO).next_to(ejes.c2p(2, 1e6), UP, buff=0.08).align_to(ejes.c2p(2, 0), LEFT)
        self.play(Create(objetivo), FadeIn(et_obj), run_time=0.8)

        t = ValueTracker(0)
        curva = always_redraw(lambda: ejes.plot(C, x_range=[0, max(t.get_value(), 0.01)], color=AZUL, stroke_width=4))
        punto = always_redraw(lambda: Dot(ejes.c2p(t.get_value(), C(t.get_value())), radius=0.08, color=AZUL))

        X_INFO = 2.15
        info_edad = always_redraw(lambda: Tex(f"Edad: {int(t.get_value())} años", font_size=30).move_to([X_INFO, 2.2, 0], aligned_edge=LEFT))
        info_cap = always_redraw(lambda: MathTex(euros(C(int(t.get_value()))), font_size=36, color=AZUL).move_to([X_INFO, 1.6, 0], aligned_edge=LEFT))
        inicial = MathTex(r"C_0 \approx " + euros(C0), font_size=30).move_to([X_INFO, 0.9, 0], aligned_edge=LEFT)

        self.add(curva, punto, info_edad, info_cap)
        self.play(FadeIn(inicial), run_time=0.6)

        hitos = [(20, "a los 20"), (40, "a los 40"), (60, "a los 60")]
        marcas = VGroup()
        for edad, _ in hitos:
            self.play(t.animate.set_value(edad), run_time=2.0 if edad == 20 else 1.6, rate_func=linear)
            m = Dot(ejes.c2p(edad, C(edad)), radius=0.06, color=NARANJA)
            et = MathTex(euros(C(edad)), font_size=22, color=NARANJA).next_to(m, UP + LEFT, buff=0.08)
            marcas.add(m, et)
            self.play(FadeIn(m), FadeIn(et), run_time=0.4)
        self.play(t.animate.set_value(67), run_time=1.0, rate_func=linear)
        self.wait(0.4)

        nota1 = Tex(r"A los 40 años solo tiene el 15\,\% del objetivo;\\ en los últimos 7 años gana más de 380\,000 €", font_size=23)
        nota1.move_to([X_INFO, -0.2, 0], aligned_edge=LEFT)
        renta = VGroup(Tex(r"A los 67, el millón genera cada año", font_size=24),
                       MathTex(r"10^6\,(e^{0.07} - 1) \approx 72\,508\ \text{€}", font_size=28, color=VERDE)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        renta.move_to([X_INFO, -1.3, 0], aligned_edge=LEFT)
        self.play(FadeIn(nota1), run_time=0.8)
        self.wait(1.2)
        self.play(FadeIn(renta), run_time=0.8)
        self.wait(3)

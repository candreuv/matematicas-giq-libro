from manim import *
import math

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
VERDE = "#1e8449"
GRIS = "#555555"


class SenxX(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        R = 2.3
        O = np.array([-5.0, -1.6, 0])
        circ = Arc(radius=R, start_angle=-0.15, angle=math.pi / 2 + 0.3, arc_center=O, color=GRIS, stroke_width=2)
        ejeX = Line(O + LEFT * 0.2, O + RIGHT * (R + 0.6), color=GRIS, stroke_width=2)
        ejeY = Line(O + DOWN * 0.2, O + UP * (R + 1.0), color=GRIS, stroke_width=2)
        tang = DashedLine(O + RIGHT * R, O + RIGHT * R + UP * 3.4, color=GRIS, stroke_width=1.5)
        self.add(circ, ejeX, ejeY, tang)

        x = ValueTracker(1.1)

        def pt(t):
            return O + R * np.array([math.cos(t), math.sin(t), 0])

        seno = always_redraw(lambda: Line(pt(x.get_value()), O + R * np.array([math.cos(x.get_value()), 0, 0]), color=NARANJA, stroke_width=5))
        arco = always_redraw(lambda: Arc(radius=R, start_angle=0, angle=x.get_value(), arc_center=O, color=AZUL, stroke_width=6))
        tg = always_redraw(lambda: Line(O + RIGHT * R, O + RIGHT * R + UP * R * math.tan(x.get_value()), color=VERDE, stroke_width=5))
        radio = always_redraw(lambda: Line(O, O + RIGHT * R + UP * R * math.tan(x.get_value()), color=GRIS, stroke_width=1.5))
        leyenda = VGroup(MathTex(r"\sin x", color=NARANJA, font_size=30), MathTex(r"x\ \text{(arco)}", color=AZUL, font_size=30),
                         MathTex(r"\tan x", color=VERDE, font_size=30)).arrange(RIGHT, buff=0.4).move_to([-4.6, 3.3, 0])
        self.play(FadeIn(leyenda), Create(arco), Create(seno), Create(tg), Create(radio), run_time=1.2)

        # derecha: grafica de sin x / x
        ejes = Axes(x_range=[-1.3, 1.3, 0.5], y_range=[0, 1.2, 0.5], x_length=5.4, y_length=4.2,
                    axis_config={"color": GRIS, "include_tip": False, "font_size": 22},
                    y_axis_config={"numbers_to_include": [0.5, 1]},
                    x_axis_config={"numbers_to_include": [-1, 1]}).move_to([3.3, -0.6, 0])
        for lab in ejes.get_x_axis().numbers + ejes.get_y_axis().numbers:
            lab.set_color(GRIS)
        uno = DashedLine(ejes.c2p(-1.3, 1), ejes.c2p(1.3, 1), color=GRIS, stroke_width=2)
        cosg = ejes.plot(lambda t: math.cos(t), x_range=[-1.3, 1.3], color=VERDE, stroke_width=2.5)
        sg = ejes.plot(lambda t: math.sin(t) / t if abs(t) > 1e-6 else 1, x_range=[-1.3, 1.3], color=AZUL, stroke_width=4)
        e1 = MathTex(r"y=1", font_size=26, color=GRIS).next_to(ejes.c2p(1.3, 1), UP, buff=0.08)
        e2 = MathTex(r"\cos x", font_size=26, color=VERDE).next_to(ejes.c2p(1.3, math.cos(1.3)), RIGHT, buff=0.08)
        e3 = MathTex(r"\frac{\sin x}{x}", font_size=30, color=AZUL).move_to(ejes.c2p(0.75, 0.62))
        desig = MathTex(r"\cos x \le \frac{\sin x}{x} \le 1", font_size=36).move_to([3.3, 2.8, 0])
        self.play(Create(ejes), Create(uno), Create(cosg), Create(sg), FadeIn(e1), FadeIn(e2), FadeIn(e3), FadeIn(desig), run_time=1.5)
        punto = always_redraw(lambda: Dot(ejes.c2p(x.get_value(), math.sin(x.get_value()) / x.get_value()), color=NARANJA, radius=0.08))
        vals = always_redraw(lambda: MathTex(r"x = %.2f:\ \ \frac{\sin x}{x} = %.4f" % (x.get_value(), math.sin(x.get_value()) / x.get_value()), font_size=30).move_to([3.3, 1.75, 0]))
        self.add(punto, vals)
        self.play(x.animate.set_value(0.05), run_time=7, rate_func=smooth)
        fin = MathTex(r"\lim_{x\to 0}\frac{\sin x}{x} = 1", font_size=38, color=AZUL).move_to([-4.0, -2.9, 0])
        self.play(FadeIn(fin), run_time=0.8)
        self.wait(3)

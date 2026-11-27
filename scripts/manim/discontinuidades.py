from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"
NEGRO = "#222222"

YMAX = 3


def clip(y):
    return max(-YMAX, min(YMAX, y))


class Discontinuidades(Scene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        casos = [
            ("Evitable", lambda x: x + 1, [(-1, 1)], (0, 1), (0, 2.3)),
            ("De salto", lambda x: 1 + 0.5 * x if x < 0 else 2.2 + 0.4 * x, [(-1, 0), (0, 1)], (0, 1), (0, 2.2)),
            ("Infinita", lambda x: 0.4 / x, [(-1, -0.134), (0.134, 1)], None, None),
            ("Esencial", lambda x: 1.5 * np.sin(1 / x), None, None, None),
        ]
        posiciones = [np.array([-3.4, 1.55, 0]), np.array([3.4, 1.55, 0]), np.array([-3.4, -2.05, 0]), np.array([3.4, -2.05, 0])]
        d = ValueTracker(0.95)
        todo = []
        for (nombre, f, tramos, hueco, lleno), pos in zip(casos, posiciones):
            ax = Axes(x_range=[-1, 1, 0.5], y_range=[-YMAX, YMAX, 1], x_length=5.2, y_length=2.9,
                      axis_config={"color": GRIS, "include_tip": False, "include_ticks": False}).move_to(pos)
            tit = Tex(nombre, font_size=30).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
            grupo = VGroup(ax, tit)
            if tramos is not None:
                for a, b in tramos:
                    grupo.add(ax.plot(f, x_range=[a + 1e-3, b - 1e-3], color=NEGRO, stroke_width=3))
            else:
                xs = np.concatenate([np.linspace(-1, -0.012, 3000), [np.nan], np.linspace(0.012, 1, 3000)])
                for seg in [np.linspace(-1, -0.012, 4000), np.linspace(0.012, 1, 4000)]:
                    m = VMobject(color=NEGRO, stroke_width=1.6)
                    m.set_points_as_corners([ax.c2p(x, f(x)) for x in seg])
                    grupo.add(m)
            if hueco:
                grupo.add(Circle(radius=0.07, color=NEGRO, stroke_width=2.5, fill_color=WHITE, fill_opacity=1).move_to(ax.c2p(*hueco)).set_z_index(3))
            if lleno:
                grupo.add(Dot(ax.c2p(*lleno), color=NEGRO, radius=0.07).set_z_index(3))
            if nombre == "Infinita":
                grupo.add(DashedLine(ax.c2p(0, -YMAX), ax.c2p(0, YMAX), color=GRIS, stroke_width=1.5))
            todo.append((grupo, ax, f))
        self.play(*[FadeIn(g) for g, _, _ in todo], run_time=1.2)

        for g, ax, f in todo:
            pL = always_redraw(lambda ax=ax, f=f: Dot(ax.c2p(-d.get_value(), clip(f(-d.get_value()))), color=AZUL, radius=0.085).set_z_index(5))
            pR = always_redraw(lambda ax=ax, f=f: Dot(ax.c2p(d.get_value(), clip(f(d.get_value()))), color=NARANJA, radius=0.085).set_z_index(5))
            self.add(pL, pR)
        self.play(d.animate.set_value(0.02), run_time=6, rate_func=rate_functions.ease_in_out_sine)
        notas = [
            MathTex(r"\lim_{x\to a^-} = \lim_{x\to a^+} \neq f(a)", font_size=24),
            MathTex(r"\lim_{x\to a^-} \neq \lim_{x\to a^+}", font_size=24),
            MathTex(r"\lim = \pm\infty", font_size=24),
            Tex(r"no hay límite (oscila)", font_size=24),
        ]
        for (g, ax, f), n in zip(todo, notas):
            n.next_to(ax, UP, buff=0.05).align_to(ax, RIGHT)
        self.play(*[FadeIn(n) for n in notas], run_time=0.8)
        self.wait(3)

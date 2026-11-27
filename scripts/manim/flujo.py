from manim import *
import numpy as np

config.background_color = WHITE
AZUL = "#1f5fa8"
NARANJA = "#d35400"
GRIS = "#555555"


class Flujo(Scene):
    def fase(self, F, titulo, sub, dur=5, yr=(-3, 3), ypart=(-2.8, 2.2), paredes=False, wrap=False):
        campo = ArrowVectorField(lambda p: F(p) * 0.45, x_range=[-4, 4, 0.8], y_range=[yr[0], yr[1], 0.8],
                                 colors=[GRIS, AZUL], length_func=lambda n: min(n, 0.7), min_color_scheme_value=0, max_color_scheme_value=2)
        campo.shift(DOWN * 0.3)
        t = VGroup(MathTex(titulo, font_size=36), Tex(sub, font_size=28, color=GRIS)).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.15)
        fondo = BackgroundRectangle(t, color=WHITE, fill_opacity=0.9, buff=0.1)
        extra = VGroup()
        if paredes:
            extra.add(Line([-4.6, 2.3, 0], [4.6, 2.3, 0], color=BLACK, stroke_width=8), Line([-4.6, -2.9, 0], [4.6, -2.9, 0], color=BLACK, stroke_width=8))
        self.play(Create(campo), FadeIn(fondo), FadeIn(t), FadeIn(extra), run_time=1.2)
        rng = np.random.default_rng(3)
        puntos = VGroup(*[Dot([x, y, 0], radius=0.07, color=NARANJA) for x, y in rng.uniform([-3.5, ypart[0]], [3.5, ypart[1]], (36, 2))])
        self.play(FadeIn(puntos), run_time=0.5)
        estelas = VGroup() if wrap else VGroup(*[TracedPath(d.get_center, stroke_color=NARANJA, stroke_width=2, dissipating_time=0.8) for d in puntos])
        self.add(estelas)

        def mover(m, dt):
            for d in m:
                p = d.get_center()
                q = p + F(p - np.array([0, -0.3, 0])) * dt * 0.45
                if wrap and q[0] > 4.4:
                    q[0] -= 8.8
                d.move_to(q)
        puntos.add_updater(mover)
        self.wait(dur)
        puntos.clear_updaters()
        self.play(FadeOut(campo), FadeOut(puntos), FadeOut(t), FadeOut(fondo), FadeOut(extra), *[FadeOut(e) for e in estelas], run_time=0.6)
        self.remove(estelas)

    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        self.fase(lambda p: np.array([-p[1], p[0], 0]), r"\vec v(x,y) = (-y,\ x)", r"Rotación: las partículas giran alrededor del origen")
        self.fase(lambda p: np.array([p[0], p[1], 0]) * 0.6, r"\vec v(x,y) = (x,\ y)", r"Fuente: las partículas se alejan del origen", dur=3)
        self.fase(lambda p: np.array([1.2 * max(0, 1 - (p[1] / 2.6) ** 2), 0, 0]) * 2, r"\vec v(x,y) = v_{\max}\left(1 - \frac{y^2}{R^2}\right)\vec{i}", r"Flujo en una tubería: más rápido en el centro", dur=4, yr=(-2.4, 2.4), ypart=(-2.6, 2.0), paredes=True, wrap=True)

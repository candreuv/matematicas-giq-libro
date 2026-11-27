from manim import *
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

config.background_color = WHITE
GRIS = "#555555"


def f(x, y):
    return 2.5 * np.exp(-((x - 0.8) ** 2 + y ** 2)) + 1.6 * np.exp(-((x + 1.0) ** 2 + (y - 0.6) ** 2) / 0.5)


NIVELES = [0.4, 0.9, 1.4, 1.9, 2.3]
COLORES = ["#440154", "#3b528b", "#21918c", "#5ec962", "#c8a800"]
g = np.linspace(-2.5, 2.5, 300)
X, Y = np.meshgrid(g, g)
cs = plt.contour(X, Y, f(X, Y), levels=NIVELES)
SEGS = cs.allsegs
plt.close()


class CurvasNivel(ThreeDScene):
    def construct(self):
        Tex.set_default(color=BLACK)
        MathTex.set_default(color=BLACK)
        ejes = ThreeDAxes(x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0, 3, 1],
                          x_length=5, y_length=5, z_length=3, axis_config={"color": GRIS, "include_tip": False})
        self.set_camera_orientation(phi=65 * DEGREES, theta=-50 * DEGREES, zoom=1.1)
        sup = Surface(lambda u, v: ejes.c2p(u, v, f(u, v)), u_range=[-2.5, 2.5], v_range=[-2.5, 2.5], resolution=(36, 36))
        sup.set_style(fill_opacity=0.55, stroke_width=0.3, stroke_color=GRIS)
        sup.set_fill_by_value(axes=ejes, colorscale=[(BLUE_E, 0), (TEAL, 1.2), (YELLOW_D, 2.5)], axis=2)
        titulo = MathTex(r"z = f(x,y)", font_size=36)
        self.add_fixed_in_frame_mobjects(titulo)
        titulo.to_corner(UL)
        self.add(ejes)
        self.play(Create(sup), run_time=2)

        info = Tex(r"Cortamos con planos $z=c$", font_size=30)
        self.add_fixed_in_frame_mobjects(info)
        info.to_corner(UR)
        self.play(FadeIn(info), run_time=0.4)
        planos_curvas = []
        altas = []
        for c, col, segs in zip(NIVELES, COLORES, SEGS):
            plano = Square(side_length=5).set_fill(col, opacity=0.15).set_stroke(col, 1).move_to(ejes.c2p(0, 0, c))
            et = MathTex(r"c = %.1f" % c, font_size=30, color=col)
            self.add_fixed_in_frame_mobjects(et)
            et.next_to(info, DOWN, buff=0.2)
            self.play(FadeIn(plano), FadeIn(et), run_time=0.4)
            arriba = VGroup(); abajo = VGroup()
            for s in segs:
                if len(s) < 3:
                    continue
                p = [ejes.c2p(x, y, c) for x, y in np.vstack([s[::3], s[-1:]])]
                q = [ejes.c2p(x, y, 0) for x, y in np.vstack([s[::3], s[-1:]])]
                arriba.add(VMobject(stroke_color=col, stroke_width=4).set_points_as_corners(p))
                abajo.add(VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(q))
            self.play(Create(arriba), run_time=0.7)
            self.play(TransformFromCopy(arriba, abajo), FadeOut(plano), run_time=0.8)
            self.remove(et)
            planos_curvas.append(abajo)
            altas.append(arriba)
        self.remove(info)
        nota = Tex(r"Proyectamos en el plano $xy$: \\ \textbf{mapa de curvas de nivel}", font_size=30)
        self.add_fixed_in_frame_mobjects(nota)
        nota.to_corner(UR)
        self.play(FadeOut(sup), *[FadeOut(a) for a in altas], run_time=0.8)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.2, run_time=2.5)
        self.wait(3)

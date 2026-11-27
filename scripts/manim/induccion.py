from manim import *
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; GRIS = "#555555"; VERDE = "#1e8449"

class Induccion(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        tit = MathTex(r"F(n):\ 1+2+\dots+n=\frac{n(n+1)}{2}", font_size=38).to_edge(UP, buff=0.25)
        self.add(tit)
        N = 8; fichas = VGroup(); labs = VGroup()
        for i in range(N):
            r = Rectangle(width=0.32, height=2.2, fill_color=AZUL, fill_opacity=0.85, stroke_color=BLACK, stroke_width=2)
            r.move_to([-4.6 + i * 1.25, -0.6, 0], aligned_edge=DOWN).shift(DOWN * 1.1)
            fichas.add(r)
            labs.add(MathTex(str(i + 1), font_size=30).next_to(r, DOWN, buff=0.15))
        suelo = Line([-5.5, -1.75, 0], [5.6, -1.75, 0], color=GRIS)
        self.play(Create(suelo), FadeIn(fichas), FadeIn(labs), run_time=1)
        b = Tex(r"1. Base: $F(1)$ es cierta: $1=\frac{1\cdot2}{2}$", font_size=32, color=VERDE).to_edge(DOWN, buff=0.2)
        self.play(FadeIn(b)); self.play(fichas[0].animate.set_fill(VERDE), run_time=0.5); self.wait(1)
        p = Tex(r"2. Paso: si cae la ficha $k$, cae la $k+1$:\ $F(k)\Rightarrow F(k+1)$", font_size=32, color=NARANJA).to_edge(DOWN, buff=0.2)
        self.play(FadeOut(b), FadeIn(p))
        arr = Arrow(fichas[2].get_top() + UP * 0.25, fichas[3].get_top() + UP * 0.25, color=NARANJA, buff=0.05, path_arc=-1.2)
        kk = MathTex("k", font_size=30, color=NARANJA).next_to(fichas[2], UP, buff=0.6); k1 = MathTex("k+1", font_size=30, color=NARANJA).next_to(fichas[3], UP, buff=0.6)
        self.play(Create(arr), FadeIn(kk), FadeIn(k1)); self.wait(1.5); self.play(FadeOut(arr), FadeOut(kk), FadeOut(k1))
        c = Tex(r"Conclusión: caen todas: $F(n)$ es cierta para todo $n\in\mathbb{N}$", font_size=32).to_edge(DOWN, buff=0.2)
        self.play(FadeOut(p), FadeIn(c))
        for i in range(N):
            f = fichas[i]
            f.set_fill(VERDE)
            ang = -0.44 if i < N - 1 else -1.2
            self.play(Rotate(f, angle=ang, about_point=f.get_corner(DR)), run_time=0.35)
        dots = MathTex(r"\cdots", font_size=50).move_to([5.3, -1.45, 0])
        self.play(FadeIn(dots)); self.wait(2)

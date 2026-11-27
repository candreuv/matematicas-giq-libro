from manim import *
config.background_color = WHITE
AZUL = "#1f5fa8"; NARANJA = "#d35400"; GRIS = "#555555"; VERDE = "#1e8449"

class VennOps(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        U = Rectangle(width=8.6, height=5.0, color=GRIS, stroke_width=3).shift(DOWN * 0.45)
        lu = MathTex("E", font_size=40, color=GRIS).next_to(U.get_corner(UL), DR, buff=0.15)
        cA = Circle(radius=1.6, color=AZUL, stroke_width=4).shift(LEFT * 1.0 + DOWN * 0.45)
        cB = Circle(radius=1.6, color=NARANJA, stroke_width=4).shift(RIGHT * 1.0 + DOWN * 0.45)
        lA = MathTex("A", font_size=44, color=AZUL).move_to(cA.get_center() + LEFT * 1.0 + UP * 1.2)
        lB = MathTex("B", font_size=44, color=NARANJA).move_to(cB.get_center() + RIGHT * 1.0 + UP * 1.2)
        self.add(U, lu); self.play(Create(cA), Create(cB), FadeIn(lA), FadeIn(lB), run_time=1.2)
        Ufill = Rectangle(width=8.6, height=5.0).shift(DOWN * 0.45)
        ops = [
            (r"A\cup B=\{x:\ x\in A\ \text{o}\ x\in B\}", lambda: Union(cA.copy(), cB.copy())),
            (r"A\cap B=\{x:\ x\in A\ \text{y}\ x\in B\}", lambda: Intersection(cA.copy(), cB.copy())),
            (r"A-B=\{x\in A:\ x\notin B\}", lambda: Difference(cA.copy(), cB.copy())),
            (r"B-A=\{x\in B:\ x\notin A\}", lambda: Difference(cB.copy(), cA.copy())),
            (r"A^c=\{x\in E:\ x\notin A\}", lambda: Difference(Ufill.copy(), cA.copy())),
            (r"A\,\Delta\,B=(A-B)\cup(B-A)", lambda: Union(Difference(cA.copy(), cB.copy()), Difference(cB.copy(), cA.copy()))),
        ]
        cur = None; tit = None
        for tex, mk in ops:
            reg = mk().set_fill(VERDE, opacity=0.55).set_stroke(width=0)
            t = MathTex(tex, font_size=40).to_edge(UP, buff=0.25)
            if cur is None:
                self.play(FadeIn(reg), FadeIn(t), run_time=0.8)
            else:
                self.play(FadeOut(cur), FadeOut(tit), run_time=0.4)
                self.play(FadeIn(reg), FadeIn(t), run_time=0.6)
            self.bring_to_front(cA, cB, lA, lB)
            cur, tit = reg, t
            self.wait(1.6)
        self.wait(0.8)

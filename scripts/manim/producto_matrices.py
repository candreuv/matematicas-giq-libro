from manim import *
import numpy as np
config.background_color = WHITE
AZ="#1f5fa8"; NA="#d35400"; VE="#1e8449"
class ProductoMatrices(Scene):
    def construct(self):
        MathTex.set_default(color=BLACK)
        A=[[1,2,0],[-1,3,4]]; C=[[1,0],[2,-1],[0,3]]
        P=np.array(A)@np.array(C)
        mA=Matrix(A,h_buff=0.9).set_color(BLACK).scale(0.9)
        mC=Matrix(C,h_buff=0.9).set_color(BLACK).scale(0.9)
        res=[["?","?"],["?","?"]]
        mR=Matrix(res,h_buff=1.1).set_color(BLACK).scale(0.9)
        eq=MathTex("=",font_size=50)
        g=VGroup(mA,mC,eq,mR).arrange(RIGHT,buff=0.35).shift(UP*0.9)
        la=MathTex(r"A\ (2\times3)",font_size=34).next_to(mA,UP); lc=MathTex(r"C\ (3\times2)",font_size=34).next_to(mC,UP); lr=MathTex(r"AC\ (2\times2)",font_size=34).next_to(mR,UP)
        for m in (mA,mC,mR): 
            for e in m.get_entries(): e.set_color(BLACK)
        for b in (mA,mC,mR): b.get_brackets().set_color(BLACK)
        self.play(FadeIn(g),FadeIn(la),FadeIn(lc),FadeIn(lr))
        rA=mA.get_rows(); cC=mC.get_columns(); eR=mR.get_entries()
        for i in range(2):
            for j in range(2):
                hr=SurroundingRectangle(rA[i],color=AZ,buff=0.12,stroke_width=4)
                hc=SurroundingRectangle(cC[j],color=NA,buff=0.12,stroke_width=4)
                k=i*2+j; he=SurroundingRectangle(eR[k],color=VE,buff=0.12,stroke_width=4)
                terms=[f"({A[i][t]})({C[t][j]})" for t in range(3)]
                calc=MathTex(r"c_{%d%d}="%(i+1,j+1)+"+".join(terms)+f"={P[i,j]}",font_size=40).shift(DOWN*1.6)
                calc[0].set_color(BLACK)
                self.play(Create(hr),Create(hc),Create(he),FadeIn(calc),run_time=0.8)
                new=MathTex(str(P[i,j]),font_size=40,color=VE).move_to(eR[k])
                self.play(Transform(eR[k],new),run_time=0.6)
                self.wait(0.9)
                self.play(FadeOut(hr),FadeOut(hc),FadeOut(he),FadeOut(calc),run_time=0.4)
        rule=MathTex(r"(m\times\boxed{p})\cdot(\boxed{p}\times n)=m\times n",font_size=40).shift(DOWN*1.6)
        rule2=MathTex(r"c_{ij}=\text{fila } i \text{ de } A\ \cdot\ \text{columna } j \text{ de } C",font_size=36).next_to(rule,DOWN)
        self.play(FadeIn(rule),FadeIn(rule2)); self.wait(2.5)

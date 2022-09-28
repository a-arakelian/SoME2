import math
import numpy as np
from manim import *
MY_LIST = [
    1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1,
    10, 20, 30, 40, 50, 60, 70, 80, 90,
    100, 200, 300, 400, 500, 600, 700, 800, 900,
    1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000,
]
HOT_COLORS = [
    "#fff10f",
    "#ff8c0f",
    "#e8113f",
    "#ec008f",
    "#b03dff",
    "#60ffff",
    "#00bcff",
    "#00b29f",
    "#009e4f",

]

def lighting_rectangular(
    color = YELLOW,
    height = 0.05,
    width= 1,
    Height = 5,
    Width= 1,
    n_partitions = 32,
    height_function = rate_functions.ease_in_quint,
    width_function = rate_functions.rush_from,
    opacity_function = rate_functions.ease_out_quart,
):
    n = n_partitions
    def get_interpolation(x, function, start, end):
        y = start*(1-function(x)) + end*function(x)
        return y

    rectangles = VGroup(
        *[
            Rectangle(
                color,
                get_interpolation(i/n, height_function, height, Height),
                get_interpolation(i/n, width_function, width, Width),
                fill_color = color,
                fill_opacity = get_interpolation(i/n, opacity_function, 1, 0.015),
                stroke_opacity = 0.1 * get_interpolation(i/n, opacity_function, 1, 0),
                stroke_width = 0.1
            )
            for i in range(n)
        ]
    )
    return rectangles

def lighting_point(
    color = YELLOW,
    radius = 0.05,
    Radius= 3,
    n_partitions = 32,
    radius_function = rate_functions.ease_in_quint,
    opacity_function = rate_functions.ease_out_quart,
):
    n = n_partitions
    def get_interpolation(x, function, start, end):
        y = start*(1-function(x)) + end*function(x)
        return y

    dots = VGroup(
        *[
            Dot(
                ORIGIN,
                get_interpolation(i/n, radius_function, radius, Radius),
                stroke_width = 0,
                fill_opacity = get_interpolation(i/n, opacity_function, 1, 0.01),
                color = color               
            )
            for i in range(n)
        ]
    )
    return dots

def starting_with(n):
    text = r"\text{Starting with: }"
    number = r"{:,}".format(int(n))
    return MathTex(text, number).set_color(HOT_COLORS[n-1])
    
def replace(lighting_rectangular, mobject):
    lighting_rectangular.stretch_to_fit_width(mobject.width)
    lighting_rectangular.move_to(mobject)

class NumberLineScene(Scene):
    def construct(self):

        self.setup_number_line()
        nl = self.numberline
        nl.to_edge(LEFT).shift(3*DOWN)
        zero_point = nl.n2p(0)

        self.add(nl)
        labels = VGroup()
        #nl.add(labels)
        for i in range(3):
            if i == 0:
                N = 4
                a = 0
            else:
                N = 3
                a = 1

            labels.add(
                *[
                self.add_pow_to_number_line(2, 3*i + a + j)
                for j in range(N)
            ])
            self.play(AnimationGroup(
                *[Write(label) for label in labels[3*i + a:]],
                lag_ratio=0.5
            ))
            nl.add(*[label for label in labels[3*i + a:]])
            
            self.play(nl.animate.scale(1/10, about_point=zero_point), run_time = 2)
            if i == 2:
                i += 1
                labels.add(
                    *[
                    self.add_pow_to_number_line(2, 3*i + a + j)
                    for j in range(N+1)
                ])
                self.play(AnimationGroup(
                    *[Write(label) for label in labels[3*i + a:]],
                    lag_ratio=0.5
                ))
                nl.add(*[label for label in labels[3*i + a:]])
        self.play(nl.animate.scale(10**3, about_point=zero_point), run_time = 6)

        l_dots = VGroup(*[lighting_point(color) for color in HOT_COLORS])
        
        for i in range(9):
            l_dots[i].move_to([-6, 3.5 -i/2, 0])
        
        text_labels = VGroup(*[starting_with(n+1).scale(0.6).next_to(l_dots[n][0], RIGHT, buff=0.2) for n in range(9)])
        background = VGroup(*[SurroundingRectangle(text_label, BLACK, corner_radius=0.1, fill_opacity= 0.6, stroke_width = 0) for text_label in text_labels])
        self.play(*[FadeIn(l_dots[i], background[i], text_labels[i]) for i in range(9)])


        l_rects = VGroup()
        for i in range(3):
            if i == 0:
                N = 4
                a = 0
            else:
                N = 3
                a = 1

            l_rects.add(
                *[
                self.turn_on_ligth(pow(2, 3*i + a + j))
                for j in range(N)
            ])
            self.play(AnimationGroup(
                *[FadeIn(l_rect) for l_rect in l_rects[3*i + a:]],
                lag_ratio=0.9
            ))
            nl.add(*[l_rect for l_rect in l_rects[3*i + a:]])
            
            self.play(nl.animate.scale(1/10, about_point=zero_point), run_time = 2)
            if i == 2:
                i += 1
                l_rects.add(
                    *[
                    self.turn_on_ligth(pow(2, 3*i + a + j))
                    for j in range(N+1)
                ])
                self.play(AnimationGroup(
                    *[FadeIn(l_rect) for l_rect in l_rects[3*i + a:]],
                    lag_ratio=0.9
                ))
                nl.add(*[l_rect for l_rect in l_rects[3*i + a:]])
        self.wait(1)
        r_tip = self.add_pow_to_number_line(2, 11)
        self.play(Circumscribe(r_tip[0], color=HOT_COLORS[-1]))
        self.wait()
        inequality = self.inequality_of_starting(r_tip, r"2^{11}")
        inequality.move_to([3, 0, 0]).align_to([0, 3, 0], UP)
        inequality[0].save_state()
        inequality[0][0].scale(0.001)
        inequality[0][2].scale(0.001)
        inequality[0].move_to(r_tip[0])

        self.play(Restore(inequality[0]), run_time = 2.5)
        self.wait(1.5)
        self.play(
            AnimationGroup(
                FadeIn(inequality[1]), FadeIn(inequality[2]), lag_ratio=0.8
            )
        )

        self.wait()
        inequality.generate_target()
        r_tip.generate_target()
        r_tip.target.shift(0.65*RIGHT)
        r_tip.target[0].become(
            MathTex(r"a")
            .move_to(r_tip.target[0])
            .scale(1.2)
            .set_color(GRAY_A)
        )
        inequality.target.become(self.inequality_of_starting(r_tip.target, r"a"))
        inequality.target.move_to([3, 0, 0]).align_to([0, 3, 0], UP)

        self.play(MoveToTarget(inequality), MoveToTarget(r_tip), run_time = 2)
        self.wait(1.5)

        inequality.add_updater(
            lambda mob, dt: mob.become(
                self.inequality_of_starting(r_tip, r"a")
                .move_to([3, 0, 0])
                .align_to([0, 3, 0], UP)
            )
        )
        box = SurroundingRectangle(inequality, WHITE, buff=0.5, fill_color = DARKER_GRAY, stroke_width = 2.5).set_opacity(0.95).set_z_index(-1)
        self.play(Write(box))
        
        self.play(r_tip.animate.shift(3*RIGHT), run_time = 3)
        self.wait(0.5)
        nl.set_z_index(-2)
        self.wait(1)
        self.play(nl.animate.scale(10, about_point=zero_point), r_tip.animate.shift(1.5*RIGHT), run_time = 8)
        self.wait()
        self.play(Indicate(inequality[1]))
        self.wait(0.5)
        self.play(nl.animate.scale(10, about_point=zero_point), run_time = 8)
        self.wait()
        inequality.clear_updaters()
        
        inequality[1].generate_target()
        inequality[1].target.become(MathTex(r"\Updownarrow").move_to(inequality[1]))
        
        inequality[0][0].generate_target()
        inequality[0][2].generate_target()

        inequality[0][0].target.become(MathTex(r"5 \cdot 10", r"^{q}", r"\leqslant").align_to(inequality[0][0], RIGHT+DOWN))
        inequality[0][0].target[1].set_color(RED)
        inequality[0][2].target.become(MathTex(r"< 6 \cdot 10", r"^{q}").align_to(inequality[0][2], LEFT+DOWN))
        inequality[0][2].target[1].set_color(RED)

        for_s_q = Tex(r"for some ", r"$q \in \mathbb{N} \cup \{0\}$").scale(0.4).align_to(box, LEFT+UP)
        for_s_q[1][0].set_color(RED)
        for_s_q.shift(0.05*(RIGHT+DOWN))
        
        self.play(
            Write(for_s_q),
            MoveToTarget(inequality[1]),
            MoveToTarget(inequality[0][0]),
            MoveToTarget(inequality[0][2])
        )
        self.wait()
        inequality[0][2].generate_target()
        inequality[0][2].target.become(MathTex(r"< (5+1) \cdot 10", r"^{q}").align_to(inequality[0][2], LEFT+UP))
        inequality[0][2].target[1].set_color(RED)
        box.generate_target()
        box.target.become(SurroundingRectangle(VGroup(inequality, inequality[0][2].target), WHITE, buff=0.5, fill_color = DARKER_GRAY, stroke_width = 2.5).set_opacity(0.95).set_z_index(-1))

        ineq = inequality[1:]
        ineq.generate_target()
        ineq.target.next_to(VGroup(inequality[0][0], inequality[0][2].target), DOWN, buff =0.3)
        self.play(MoveToTarget(inequality[0][2]), MoveToTarget(box), MoveToTarget(ineq))

        self.play(
            inequality[0][0][1].animate.set_color(RED),
            inequality[0][2][1].animate.set_color(RED)
        )

        inequality[0][0].generate_target()
        inequality[0][2].generate_target()

        inequality[2][2].generate_target()

        inequality[0][0].target.become(MathTex(r"k \cdot 10", r"^{q}", r"\leqslant").align_to(inequality[0][0], RIGHT+DOWN))
        inequality[0][0].target[1].set_color(RED)
        inequality[0][2].target.become(MathTex(r"< (k + 1) \cdot 10", r"^{q}").align_to(inequality[0][2], LEFT+UP))
        inequality[0][2].target[1].set_color(RED)

        inequality[2][2].target.become(MathTex(r"k").move_to(inequality[2][2]))
        inequality[2][2].target.set_color(WHITE)
        self.wait(1.5)
        self.play(
            MoveToTarget(inequality[2][2]),
            MoveToTarget(inequality[0][0]),
            MoveToTarget(inequality[0][2]),
            inequality[2][0].animate.set_color(WHITE),
            inequality[2][1].animate.set_color(WHITE),
            FadeOut(r_tip)
        )
        
        self.wait(2.5)


        #self.play(nl.animate.scale(10**3, about_point=zero_point), run_time = 6)

    def setup_number_line(self):
        self.numberline = NumberLine(
            x_range=[0, 10000, 1],
            length=15000,
            include_tip=False,
            include_numbers=False,
            include_ticks=False
        )
        nl = self.numberline

        # For start
        xs0 = range(0, 10, 1)
        nl.add(*[
            nl.get_tick(x, size=0.15)
            for x in xs0
        ])
        nl.add_numbers(
            xs0,
            buff=0.2,
            font_size=36,
        )

        
        # For first zoom
        xs1 = range(10, 100, 10)
        nl.add(*[
            nl.get_tick(x, size=1.5)
            for x in xs1
        ])
        nl.add_numbers(
            xs1,
            buff=2,
            font_size=360,
        )

        # For second zoom
        xs2 = range(100, 1000, 100)
        nl.add(*[
            nl.get_tick(x, size=15)
            for x in xs2
        ])
        nl.add_numbers(
            xs2,
            buff=20,
            font_size=3600,
        )

        # For third zoom
        xs3 = range(1000, 10000, 1000)
        nl.add(*[
            nl.get_tick(x, size=150)
            for x in xs3
        ])
        nl.add_numbers(
            xs3,
            buff=200,
            font_size=36000,
        )
        for n in nl.numbers:
            n[1].scale(0.5)


    def add_pow_to_number_line(self, a, n):
        x = a**n
        tip = Triangle().scale(0.3).rotate(60*DEGREES).stretch(0.2, 0)
        tip.set_opacity(1)
        nl = self.numberline
        tip.next_to(nl.n2p(x), UP, buff=0.2)
        label = MathTex(
            r"{:,}".format(int(a)),
            r"^{" + r"{:,}".format(int(n)) + r"}",
        ).next_to(tip, UP)
        label[1].set_color(BLUE)
        return VGroup(label, tip)
    
    def turn_on_ligth(self, n):
        nl = self.numberline
        digits = int(math.log10(n))
        starting_n = int(n/pow(10, digits))
        n_max = int(starting_n + 1)*pow(10, digits)
        n_min = int(starting_n)*pow(10, digits)
        points = VGroup(
            VectorizedPoint(nl.n2p(n_min)),
            VectorizedPoint(nl.n2p(n_max)),
        )
        #print(n)
        #print(n_max)
        #print(n_min)
        lighting_rect = lighting_rectangular(HOT_COLORS[starting_n-1])
        replace(lighting_rect, points)
        return lighting_rect

    def inequality_of_starting(self, mob, label, concrete = True):
        nl = self.numberline
        if concrete:
            pass
        n = nl.p2n(mob.get_center())
        digits = int(math.log10(n))
        starting_n = int(n/pow(10, digits))
        starting_string = r"{:,}".format(starting_n)
        n_max = int(starting_n + 1)*pow(10, digits)
        n_min = int(starting_n)*pow(10, digits)

        t_min = r"{:,}".format(int(n_min)) + r"\leqslant"
        t_max = r"<" + r"{:,}".format(int(n_max))
        
        inequal = MathTex(t_min, t_max)
        inequality = VGroup(inequal[0], mob[0].copy(), inequal[1]).arrange(RIGHT)
        inequality[1].align_to(inequality[2][0], DOWN)
        downarrow = MathTex(r"\Downarrow")
        downarrow.next_to(inequality[1], DOWN, buff=0.3)
        starting = MathTex(label, r"\text{ is starting with: }", starting_string)
        starting.set_color(HOT_COLORS[starting_n-1]).next_to(downarrow, DOWN, buff=0.3)
        return VGroup(inequality, downarrow, starting)


class LogScene(NumberLineScene):
    def construct(self):
        self.setup_number_line()
        self.set_inequality()
        nl = self.numberline
        formula = self.formula
        log_formula = self.log_formula
        nl.to_edge(LEFT).shift(2.25*DOWN)
        zero_point = nl.n2p(0)
        pows = VGroup(*[self.add_pow_to_number_line(2, i) for i in range(14)])
        lights = VGroup(*[self.turn_on_ligth(i) for i in MY_LIST])
        nl.add(pows, lights)

        rec_formula = MathTex(
            r"a \leqslant b < c",
            r"\Leftrightarrow",
            r"\log_{10}a \leqslant \log_{10}b < \log_{10}c"
        ).scale(0.7)

        self.play(FadeIn(formula))
        
        rec_formula.set_color(YELLOW)
        rec_formula.to_edge(UL)
        self.wait()
        self.play(Write(rec_formula[0]))
        self.wait(0.5)
        self.play(Write(rec_formula[1]))
        self.wait(0.5)
        self.play(Write(rec_formula[2]))
        self.wait(1.5)
        formula.generate_target()
        VGroup(log_formula, formula.target).arrange(DOWN, buff=0.25)
        self.play(MoveToTarget(formula), FadeIn(log_formula), FadeOut(rec_formula))
        self.wait()
        rec_formula.become(MathTex(
            r"\log_{10}(a \cdot b)",
            r"=",
            r"\log_{10}a + \log_{10}b"
        ).scale(0.7))
        rec_formula.set_color(YELLOW)
        rec_formula.to_edge(UL)
        self.play(Write(rec_formula[0]))
        self.wait(0.5)
        self.play(Write(rec_formula[1]))
        self.play(Write(rec_formula[2]))
        self.wait(1.5)

        log_formula_0_1 = log_formula[0][1].copy()

        log_formula_0_0 = MathTex(r"\log_{10} k + \log_{10} 10", r"^{q}", r" \leqslant")
        log_formula_0_0.align_to(log_formula[0][0], RIGHT+DOWN)
        log_formula_0_0[1].set_color(RED) 
        log_formula_0_2 = MathTex(r"< \log_{10} (k + 1) + \log_{10} 10", r"^{q}", r" ")
    
        log_formula_0_2.align_to(log_formula[0][2], LEFT+DOWN)
        log_formula_0_2[1].set_color(RED) 
        log_formula[2].generate_target()
        log_formula[2].target.next_to(
            VGroup(
                log_formula_0_0,
                log_formula_0_1,
                log_formula_0_2,
            ).next_to(log_formula[1], UP, buff=0.25),
            UP,
            aligned_edge=LEFT
        )
        
        
        self.play(
            TransformMatchingShapes(log_formula[0][0], log_formula_0_0, path_arc=PI/2),
            TransformMatchingShapes(log_formula[0][1], log_formula_0_1, path_arc=PI/2),
            TransformMatchingShapes(log_formula[0][2], log_formula_0_2, path_arc=PI/2),
            MoveToTarget(log_formula[2]),
            FadeOut(rec_formula)
        )
        self.wait(1.5)

        
        log_formula_0_fin = MathTex(r"\log_{10} k +", r"{q}", r" \leqslant")
        log_formula_0_fin.align_to(log_formula_0_0, RIGHT+DOWN)
        log_formula_0_fin[1].set_color(RED) 

        log_formula_1_fin = MathTex(r"n", r"\log_{10}2 ")
        log_formula_1_fin.align_to(log_formula_0_0, RIGHT+DOWN)
        log_formula_1_fin[0].set_color(BLUE)


        log_formula_2_fin = MathTex(r"< \log_{10} (k + 1) + ", r"{q}", r" ")
        log_formula_2_fin.align_to(log_formula[0][2], LEFT+DOWN)
        log_formula_2_fin[1].set_color(RED) 

        log_formula_fin = VGroup(
            log_formula_0_fin,
            log_formula_1_fin,
            log_formula_2_fin
        ).arrange(RIGHT, buff=0.15).next_to(log_formula[1], UP, buff=0.25)

        log_formula[2].generate_target()
        log_formula[2].target.next_to(
            log_formula_fin,
            UP,
            aligned_edge=LEFT
        )
       
        self.play(
            TransformMatchingShapes(log_formula_0_0, log_formula_0_fin),
            TransformMatchingShapes(log_formula_0_1, log_formula_1_fin, path_arc=PI/2),
            TransformMatchingShapes(log_formula_0_2, log_formula_2_fin),
            MoveToTarget(log_formula[2]),

        )
        self.wait()
        self.play(
            FadeOut(formula[0], formula[1], formula[3]),
            formula[2].animate.next_to(log_formula[1], DOWN, buff=0.25)
        )
        final_form = VGroup(log_formula_fin, log_formula[1], formula[2], log_formula[2])
        final_box = SurroundingRectangle(final_form, WHITE, stroke_width = 2, fill_color = DARK_GRAY).set_z_index(-1)
        final_box.set_opacity(0.85)
        self.play(Write(final_box))
        self.play(VGroup(final_box, final_form).animate.scale(0.5).to_edge(UR))
        self.wait(1.5)
        self.play(nl.animate.scale(1/100, about_point=zero_point), run_time = 2)

        
        
        self.lgnl = lgnl = NumberLine(
            x_range=[0, 4, 1],
            length=9,
            include_tip=False,
            include_numbers=True,
            include_ticks=True
        )
        

        v_point = VectorizedPoint().move_to(nl.n2p(400))
        self.wait(1.5)
        tip = always_redraw(lambda: self.get_tip(nl.p2n(v_point.get_center())))
        
        self.play(Write(tip))
        self.play(Create(lgnl))
        self.wait()
        lgtip = always_redraw(lambda: self.get_lgtrip_from_trip(nl.p2n(v_point.get_center())))
        self.play(Write(lgtip))
        
        self.add(lgtip)
        self.play(v_point.animate.shift(2*RIGHT), run_time = 2)
        self.wait(1.5)
        one_point = nl.n2p(100)
        self.play(nl.animate.scale(100, about_point=zero_point), v_point.animate.move_to(one_point), run_time = 6)
        self.wait(1)
        log_lighting_rects = always_redraw(lambda : self.tuen_on_ligths_onlg(nl.p2n(v_point.get_center())))
        self.add(log_lighting_rects)
        self.play(nl.animate.scale(1/10, about_point=zero_point), run_time = 5)
        self.wait(1)
        self.play(nl.animate.scale(1/10, about_point=zero_point), run_time = 5)
        
        self.wait(1)
        self.play(v_point.animate.move_to( nl.n2p(200)), run_time = 3)
        self.play(v_point.animate.move_to( nl.n2p(100)), run_time = 2)
        self.play(v_point.animate.move_to( nl.n2p(900)), run_time = 8)
        self.play(v_point.animate.move_to( nl.n2p(10000)), run_time = 8)
        log_lighting_rects.clear_updaters()
        tip.clear_updaters()
        lgtip.clear_updaters

        self.play(FadeOut(lgtip, tip))

        foemula_box = VGroup(final_box, final_form)

        one_period = log_lighting_rects[:9].copy()
        
        #self.wait()
        #self.play(MoveAlongPath(one_period, Line(one_period.get_center(), l_l_rects[9:18].get_center(), path_arc=-1)))
        #self.wait(0.5)
        #self.play(MoveAlongPath(one_period, Line(one_period.get_center(), l_l_rects[18:27].get_center(), path_arc=-1)))
        #self.wait(0.5)
        #self.play(MoveAlongPath(one_period, Line(one_period.get_center(), l_l_rects[27:36].get_center(), path_arc=-1)))
        #self.wait()
        #self.play(FadeOut(one_period))
        

        arrows = always_redraw(lambda : self.add_pow_path_to_lg())
        self.play(
            FadeIn(arrows), lag_ratio=0.5
        )


        
        
        self.wait()
        self.play(nl.animate.scale(100, about_point=zero_point))
        points = VGroup(*[Dot(color = WHITE).scale(0.5).move_to(nl.n2p(pow(2, i))) for i in range(4)])
        self.wait(0.5)
        self.play(AnimationGroup(
            *[points[i].animate.move_to(lgnl.n2p(math.log10(pow(2, i)))) for i in range(4)],
            lag_ratio=0.3
        ))
        self.wait(0.5)
        self.play(nl.animate.scale(1/10, about_point=zero_point))
        points.add(*[Dot(color = WHITE).scale(0.5).move_to(nl.n2p(pow(2, i))) for i in range(4, 7)])
        self.wait(0.5)
        self.play(AnimationGroup(
            *[points[i].animate.move_to(lgnl.n2p(math.log10(pow(2, i)))) for i in range(4, 7)],
            lag_ratio=0.3
        ))
        self.wait(0.5)
        self.play(nl.animate.scale(1/10, about_point=zero_point))
        points.add(*[Dot(color = WHITE).scale(0.5).move_to(nl.n2p(pow(2, i))) for i in range(7, 10)])
        self.wait(0.5)
        self.play(AnimationGroup(
            *[points[i].animate.move_to(lgnl.n2p(math.log10(pow(2, i)))) for i in range(7, 10)],
            lag_ratio=0.3
        ))
        self.wait(0.5)
        self.play(nl.animate.scale(1/10, about_point=zero_point))
        points.add(*[Dot(color = WHITE).scale(0.5).move_to(nl.n2p(pow(2, i))) for i in range(10, 14)])
        self.wait(0.5)
        self.play(AnimationGroup(
            *[points[i].animate.move_to(lgnl.n2p(math.log10(pow(2, i)))) for i in range(10, 14)],
            lag_ratio=0.3
        ))
        self.wait(0.5)
        arrows.clear_updaters()
        log_arrows = VGroup(
            *[
                Line(
                    p.get_center() + 0.75*DOWN,
                    p.get_center(),
                    stroke_width = DEFAULT_STROKE_WIDTH/2
                ).add_tip(tip_length=0.1)
                for p in points
            ]
        )

        labels = VGroup(
            *[
                MathTex(r"\log_{10}2", r"^{" + r"{:,}".format(int(i)) + r"}").scale(0.55).rotate(90*DEGREES).next_to(log_arrows[i], DOWN, buff = 0.15)
                for i in range(14)
            ]
        )
        for l in labels:
            l[1].set_color(BLUE)
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(ReplacementTransform(arrows[i], log_arrows[i]), Write(labels[i]), lag_ratio=0.8)
                    for i in range(14)
                ],
                lag_ratio=0.2
            ),
            FadeOut(nl)
        )
        self.wait()
        nlabels = VGroup(
            *[
                MathTex(r"{:,}".format(int(i)), r"\log_{10}2").scale(0.55).rotate(90*DEGREES).next_to(log_arrows[i], DOWN, buff = 0.15)
                for i in range(14)
            ]
        )

        for l in nlabels:
            l[0].set_color(BLUE)

        self.play(
            AnimationGroup(
                *[
                    TransformMatchingTex(labels[i], nlabels[i])
                    for i in range(14)
                ],
                lag_ratio=0.5
            )
        )


        self.wait(2)

     
    def tuen_on_ligths_onlg(self, x):
        lgnl = self.lgnl
        lgx = math.log10(x)
        round_x = int(x)
        v_points = []
        index = 1
        while index <= round_x:
            v_points.append(VectorizedPoint().move_to(lgnl.n2p(math.log10(index))))
            digits = int(math.log10(index))
            index += pow(10, digits)

        if x/round_x != 1:
            v_points.append(VectorizedPoint().move_to(lgnl.n2p(math.log10(x))))
        elif x == 1:
            v_points.append(VectorizedPoint().move_to(lgnl.n2p(math.log10(x+0.01))))

        pos_list=[]
        for i in range(len(v_points) - 1):
            pos_list.append(VGroup(v_points[i], v_points[i+1]))
        
        lighting_rects = VGroup()
        for i in range(len(pos_list)):
            lighting_rects.add(lighting_rectangular(
                HOT_COLORS[int(i%9)],
                height=0.05,
                Height=2
            ))
            replace(lighting_rects[i], pos_list[i])
        
        return lighting_rects

    def set_inequality(self):
        for_s_q = Tex(r"for some ", r"$q \in \mathbb{N} \cup \{0\}$").scale(0.4)
        for_s_q[1][0].set_color(RED)

        inequality_left = MathTex(r"k \cdot 10", r"^{q}", r"\leqslant")
        inequality_left[1].set_color(RED)
        inequality_right = MathTex(r"< (k + 1) \cdot 10", r"^{q}")
        inequality_right[1].set_color(RED)
        label = MathTex(
            r"2",
            r"^{n}",
        )
        label[1].set_color(BLUE)
        
        inequality = VGroup(inequality_left, label, inequality_right).arrange(RIGHT, buff=0.2)
        updown = MathTex(r"\Updownarrow")

        starting = MathTex(r"\text{ is starting with: } k" )
        l_starting = VGroup(label.copy(), starting).arrange(RIGHT, buff=0.2)
        ineq = VGroup(inequality, updown, l_starting)
        ineq.arrange(DOWN, buff=0.25)
        for_s_q.next_to(inequality, UP, aligned_edge=LEFT)
        ineq.add(for_s_q)
        self.formula = ineq

        log_inequality_left = MathTex(r"\log_{10} (k \cdot 10", r"^{q}", r") \leqslant")
        log_inequality_left[1].set_color(RED)
        log_inequality_right = MathTex(r"< \log_{10} ((k + 1) \cdot 10", r"^{q}", r")")
        log_inequality_right[1].set_color(RED)

        log_label = VGroup(MathTex(r"\log_{10}"), label.copy()).arrange(RIGHT, buff=0.1)
        log_inequality = VGroup(log_inequality_left, log_label, log_inequality_right).arrange(RIGHT, buff=0.2)
        
        log_ineq = VGroup(log_inequality, updown.copy()).arrange(DOWN, buff=0.25)
        log_ineq.add(for_s_q.copy().next_to(log_inequality, UP, aligned_edge=LEFT))
        self.log_formula = log_ineq

    def get_tip(self, x):
        nl = self.numberline
        digits = int(math.log10(x))
        starting_n = int(x/pow(10, digits)) 
        tip = Triangle().scale(0.3).rotate(60*DEGREES).stretch(0.2, 0)
        tip.set_opacity(1)
        label = MathTex(
            r"x", r"=",
            r"{:.2f}".format(x)
        ).scale(0.8)
        label[0].set_color(BLUE)
        label[2].set_color(HOT_COLORS[starting_n-1])

        trp = VGroup(label, tip)
        
        tip.next_to(nl.n2p(x), UP, buff=0.2)
        label.next_to(tip, UP, aligned_edge=LEFT)
        return trp

    def get_lgtrip_from_trip(self, x):
        lgnl = self.lgnl
        
        digits = int(math.log10(x))
        lgx = math.log10(x)
        starting_n = int(x/pow(10, digits))
        lgtip = Triangle().scale(0.3).rotate(60*DEGREES).stretch(0.2, 0)
        lgtip.set_opacity(1)
        label = MathTex(
            r"\log_{10}", r"x", r"=",
            r"{:.3f}".format(lgx)
        ).scale(0.8)
        label[1].set_color(BLUE)
        label[3].set_color(HOT_COLORS[starting_n-1])

        trp = VGroup(label, lgtip)
        
        lgtip.next_to(lgnl.n2p(lgx), UP, buff=0.2)
        label.next_to(lgtip, UP, aligned_edge=LEFT)
        return trp

    def add_pow_to_number_line(self, a, n):
        nl = self.numberline
        x = a**n
        tip = Triangle().scale(0.3).rotate(240*DEGREES).stretch(0.2, 0)
        tip.set_opacity(0.6)
        tip.set_stroke(opacity=0.6)
        label = MathTex(
            r"{:,}".format(int(a)),
            r"^{" + r"{:,}".format(int(n)) + r"}",
        ).next_to(tip, DOWN)
        label[1].set_color(BLUE)
        trp = VGroup(label, tip)
        digits = int(math.log10(x))
        trp.scale(10**(digits))
        trp.next_to(nl.n2p(x), DOWN, buff=0.2 * 10**(digits))
        return trp.set_z_index(-1)

    def turn_on_ligth(self, n):
        nl = self.numberline
        digits = int(math.log10(n))
        starting_n = int(n/pow(10, digits))
        n_max = int(starting_n + 1)*pow(10, digits)
        n_min = int(starting_n)*pow(10, digits)
        points = VGroup(
            VectorizedPoint(nl.n2p(n_min)),
            VectorizedPoint(nl.n2p(n_max)),
        )

        lighting_rect = lighting_rectangular(
            HOT_COLORS[starting_n-1],
            height=0.05*(10**digits),
            Height=2*(10**digits)
        )
        replace(lighting_rect, points)
        return lighting_rect
        
    def add_pow_path_to_lg(self):
        lgnl = self.lgnl
        nl = self.numberline
        arrows = VGroup()
        for i in range(14):
            a = nl.n2p(pow(2, i))
            b = lgnl.n2p(math.log10(pow(2, i)))
            arrows.add(Line(a, b, stroke_width = DEFAULT_STROKE_WIDTH/2, buff=0).add_tip(tip_length=0.1).set_opacity(0.5))
        return arrows

class PeriodicStructure(LogScene):
    def construct(self):
        self.setup_log_numberline()
        log_numberline = self.lgnl = self.log_numberline
        self.tuen_on_ligths_onlg(10**20)
        indicating_lights = self.indicating_lights
        self.add(log_numberline)
        self.play(FadeIn(indicating_lights))
        x_1 = MathTex(r"x_1 = 2", r"^{10}}", r"=", r"1024").scale(0.8)
        x_1.to_edge(UL)
        x_1[1].set_color(BLUE)
        x_1_tip = self.get_tip(math.log10(1024), r"x_1")
        #x_1[3].set_color(HOT_COLORS[4])
        self.play(Write(x_1))
        self.wait()
        self.play(Circumscribe(x_1[3][0], color=HOT_COLORS[0]), x_1[3].animate.set_color(HOT_COLORS[0]))

        x_2 = MathTex(r"x_2 = 2", r"^{15}", r"=", r"32708").scale(0.8)
        x_2.next_to(x_1, DOWN, aligned_edge=LEFT)
        x_2[1].set_color(BLUE)
        x_2_tip = self.get_tip(math.log10(32708), r"x_2")
        self.play(Write(x_2))
        self.wait()
        self.play(Circumscribe(x_2[3][0], color=HOT_COLORS[2]), x_2[3].animate.set_color(HOT_COLORS[2]))

        self.wait()
        self.play(ReplacementTransform(x_1.copy(), x_1_tip))
    
        self.wait()
        self.play(ReplacementTransform(x_2.copy(), x_2_tip))
        self.wait(2.5)



        fractional_part = self.fractional_part(1.414)
        self.play(Write(fractional_part))
        x = ValueTracker(1.414)
        self.wait(1.5)
        self.play(FadeOut(fractional_part))
        frac_x_1_tip = self.get_tip(math.log10(1024), r"x_1", True)
        frac_x_2_tip = self.get_tip(math.log10(32708), r"x_2", True, DOWN)

        self.play(ReplacementTransform(x_1_tip.copy(), frac_x_1_tip))
        self.play(ReplacementTransform(x_2_tip.copy(), frac_x_2_tip))
        self.wait()

        self.set_inequality()
        formula = self.formula
        formula.set_z_index(11)
        box = SurroundingRectangle(formula, WHITE, buff=0.5, fill_color = DARKER_GRAY, stroke_width = 2.5)
        box.set_opacity(0.95).set_z_index(10)
        self.play(FadeIn(box))
        self.play(FadeIn(formula))
        self.wait()
        target_formula = self.get_target_inequality().set_z_index(11)
        self.play(TransformMatchingTex(formula, target_formula))
        self.wait()
        self.play(VGroup(target_formula, box).animate.scale(0.5).to_edge(UR))

        self.wait()
        fractional_numberline =  NumberLine(
            x_range=[0, 0.9999, 1],
            length=47/20,
            include_tip=False,
            include_numbers=True,
            include_ticks=True
        )
        fractional_numberline.add(indicating_lights[:9].copy().move_to(fractional_numberline.n2p(0.5)))
        fractional_numberline.to_edge(LEFT)
        fractional_numberline.shift(2*DOWN)

        self.play(FadeOut(
            x_1,
            x_2,
            x_1_tip,
            x_2_tip,
            frac_x_1_tip,
            frac_x_2_tip
        ))

        self.play(fractional_numberline.animate.move_to(ORIGIN))
        self.wait(2)

        green_dot_1 = Dot(color=GREEN).move_to(log_numberline.n2p(1.5))
        green_dot_1_ = always_redraw(lambda: Triangle(color=GREEN, fill_opacity = 1).scale(0.3).rotate(60*DEGREES).stretch(0.2, 0).next_to(green_dot_1, UP, buff=0))
        green_dot_2 = Dot(color=GREEN, fill_opacity = 1).move_to(log_numberline.n2p(1.5))
        green_dot_2_ = always_redraw(lambda: Triangle(color=GREEN).set_opacity(1).scale(0.3).rotate(60*DEGREES).stretch(0.2, 0).next_to(green_dot_2, UP, buff=0))
        self.play(FadeIn(green_dot_1, green_dot_1_))
        self.wait(0.5)
        self.add(green_dot_2_)
        self.play(green_dot_2.animate.move_to(fractional_numberline.n2p(0.5)))
        green_dot_2.add_updater(lambda mob: mob.move_to(fractional_numberline.n2p(
            log_numberline.p2n(green_dot_1.get_center())
            - int(log_numberline.p2n(green_dot_1.get_center()))
        )))
        self.wait()
        self.play(green_dot_1.animate.move_to(log_numberline.n2p(0)), run_time = 3)
        self.play(green_dot_1.animate.move_to(log_numberline.n2p(3.25)), run_time = 6)
        self.wait(0.5)
        red_dot_1 = Dot(color=RED).move_to(log_numberline.n2p(1.5))
        red_dot_1_ = always_redraw(lambda: Triangle(color=RED).set_opacity(1).scale(0.3).rotate(60*DEGREES).stretch(0.2, 0).next_to(red_dot_1, UP, buff=0))
        red_dot_2 = Dot(color=RED, fill_opacity = 1).move_to(log_numberline.n2p(1.5))
        red_dot_2_ = always_redraw(lambda: Triangle(color=RED).set_opacity(1).scale(0.3).rotate(60*DEGREES).stretch(0.2, 0).next_to(red_dot_2, UP, buff=0))
        red_dot_2.add_updater(lambda mob: mob.move_to(fractional_numberline.n2p(
            log_numberline.p2n(red_dot_1.get_center())
            - int(log_numberline.p2n(red_dot_1.get_center()))
        )))
        red_dot_1.move_to(log_numberline.n2p(4.75))
        self.add(red_dot_1, red_dot_2)
        self.play(FadeIn(red_dot_1_.next_to(red_dot_1, UP, buff=0), red_dot_2_.next_to(red_dot_2, UP, buff=0)))
        self.wait(0.5)
        self.play(
            green_dot_1.animate().move_to(log_numberline.n2p(4-0.05)),
            red_dot_1.animate().move_to(log_numberline.n2p(4+0.05)),
            rub_time = 2
        )
        self.wait()
        self.play(VGroup(
            red_dot_1_,
            red_dot_2_,
            green_dot_1_,
            green_dot_2_,
        ).animate(rate_func = rate_functions.wiggle).shift(0.25*UP))
        self.play(FadeOut(
            red_dot_2_,
            green_dot_2_,
        ))
        self.wait()
        green_dot_2.clear_updaters()
        red_dot_2.clear_updaters()
        green_dot_2.add_updater(lambda mob: mob.move_to(fractional_numberline.point_from_proportion(
            log_numberline.p2n(green_dot_1.get_center())
            - int(log_numberline.p2n(green_dot_1.get_center()))
        )))
        red_dot_2.add_updater(lambda mob: mob.move_to(fractional_numberline.point_from_proportion(
            log_numberline.p2n(red_dot_1.get_center())
            - int(log_numberline.p2n(red_dot_1.get_center()))
        )))
        self.play(UpdateFromAlphaFunc(fractional_numberline, self.form_line_to_circule(47/20)), run_time = 3)
        self.wait()
        self.play(
            green_dot_1.animate().move_to(log_numberline.n2p(4)),
            red_dot_1.animate().move_to(log_numberline.n2p(4)),
            rub_time = 2
        )
        self.remove(red_dot_1, red_dot_1_, red_dot_2, red_dot_2_)
        def alphaupdate(mob, alpha):
            self.form_line_to_circule(alpha * 8 + (1 - alpha) * 47/20)(mob, 1)

        self.play(UpdateFromAlphaFunc(
            fractional_numberline, alphaupdate
        ))
        self.wait()
        self.play(green_dot_1.animate.move_to(log_numberline.n2p(5.5)), run_time = 3)
        self.play(FadeOut(green_dot_1, green_dot_1_, green_dot_2))
        self.wait()

        points = VGroup(*[Dot(color = WHITE).scale(0.5).move_to(log_numberline.n2p(math.log10(pow(2, i)))) for i in range(20)])
        
        log_arrows = VGroup(
            *[
                Line(
                    p.get_center() + 0.75*DOWN,
                    p.get_center(),
                    stroke_width = DEFAULT_STROKE_WIDTH/2
                ).add_tip(tip_length=0.1)
                for p in points
            ]
        )

        labels = VGroup(
            *[
                MathTex(r"\log_{10}2", r"^{" + r"{:,}".format(int(i)) + r"}").scale(0.55).rotate(90*DEGREES).next_to(log_arrows[i], DOWN, buff = 0.15)
                for i in range(20)
            ]
        )
        for l in labels:
            l[1].set_color(BLUE)

        self.play(
            AnimationGroup(
                *[FadeIn(VGroup(points[i], log_arrows[i], labels[i])) for i in range(20)],
                lag_ratio=0.4
            ), run_time = 4
        )
    
        f_points = VGroup(*[Dot(color = WHITE).scale(0.5).move_to(
            fractional_numberline.point_from_proportion(
                math.log10(pow(2, i)) - int(math.log10(pow(2, i)))
            )
        ) for i in range(100)])
        
        self.wait(2)

        self.play(Flash(points[0]), Flash(f_points[0]), FadeIn(f_points[0]))
        self.play(Flash(points[1]), Flash(f_points[1]), FadeIn(f_points[1]))
        brace_s = VGroup(*[Brace(points[i:i+2], UP, buff=0.05) for i in range(19)])
        a_brace_s = VGroup(*[
            ArcBrace(ArcBetweenPoints(f_points[i].get_center(), f_points[i+1].get_center(), radius=4/PI))
            for i in range(18)
        ])
        self.play(FadeIn(brace_s[0], a_brace_s[0]))

        for i in range(2, 20):
            self.play(AnimationGroup(
                AnimationGroup(
                    Flash(points[i]),  Flash(f_points[i]),  FadeIn(f_points[i]),
                    ReplacementTransform(brace_s[i-2], brace_s[i-1])
                ),
                Rotating(a_brace_s[0], radians = 2*PI*math.log10(2), about_point=fractional_numberline[:9].get_center(), run_time=0.5),
                lag_ratio=0.5
            ))
        self.play(FadeOut(brace_s[18]), FadeOut(a_brace_s[0]))
        self.wait()
        self.play(AnimationGroup(
            *[
                FadeIn(p) for p in f_points[20:]
            ], lag_ratio=0.8
        ), run_time = 3)

        self.play(f_points.animate.set_opacity(0.3))
        f_points.set_z_index(1)

        a_line = VMobject().move_to(fractional_numberline.get_center())
        c_line = VMobject()
        self.form_line_to_circule(8)(a_line, 0.999)
        self.form_line_to_circule(8)(c_line, 0)
        a_line_ = VGroup(*[a_line[i] for i in range(9)])
        c_line_ = VGroup(*[c_line[i].rotate(PI/2) for i in range(9)])
        c_line_.arrange(RIGHT, aligned_edge=DOWN).to_edge(LEFT)
        self.play(AnimationGroup(
            *[
                ReplacementTransform(a_, c_) for a_, c_ in zip(a_line_, c_line_)
            ], lag_ratio = 0.9
        ))
    def setup_log_numberline(self):
        log_numberline = self.log_numberline = NumberLine(
            x_range=[0, 20, 1],
            length=47,
            include_tip=False,
            include_numbers=True,
            include_ticks=True
        )
        log_numberline.to_edge(LEFT)
        log_numberline.shift(2*DOWN)
    
    def tuen_on_ligths_onlg(self, x):
        indicating_lights = self.indicating_lights = super().tuen_on_ligths_onlg(x)
        indicating_lights.stretch_to_fit_height(1)

    def get_tip(self, x, variable = r"x", fractional = False, direction = UP):
        log_numberline = self.log_numberline
        y = pow(10, x)
        digits = int(x)
        starting_n = int(y/pow(10, digits))
        tip = Triangle().scale(0.3).rotate(60*DEGREES).stretch(0.2, 0)
        if direction[1] == DOWN[1]:
            tip.rotate(180*DEGREES)
        tip.set_opacity(1)
        if fractional:
            x = x-digits
            label = MathTex(
                r"\{" + r"\log_{10}" + variable + r"\}", r"=",
                r"{:.3f}".format(x)
            ).scale(0.7)
            
        else:
            label = MathTex(
                r"\log_{10}" + variable, r"=",
                r"{:.3f}".format(x)
            ).scale(0.7)
        label[0].set_color(BLUE)
        if fractional:
            label[0][0].set_color(YELLOW)
            label[0][-1].set_color(YELLOW)
        label[2].set_color(HOT_COLORS[starting_n-1])

        trp = VGroup(label, tip)
        
        tip.next_to(log_numberline.n2p(x), direction, buff=0.2)
        label.next_to(tip, direction, aligned_edge=LEFT)
        return trp

    def fractional_part(self, x):
        x = round(x, 3)
        x_fractional_part = x - int(x)
        fp = MathTex(
            r"\{", r"{:.3f}".format(x),  r"\}",
            r"=", r"{:.3f}".format(x_fractional_part)
        ).to_edge(UR)
        fp[0].set_color(YELLOW)
        fp[2].set_color(YELLOW)
        return fp

    def set_inequality(self):
        for_s_q = Tex(r"for some ", r"$q \in \mathbb{N} \cup \{0\}$").scale(0.4)
        for_s_q[1][0].set_color(RED)

        inequality_left = self.inequality_left = MathTex(r"\log_{10}k +", r"q", r"\leqslant")
        inequality_left[1].set_color(RED)
        inequality_right = self.inequality_right = MathTex(r"< \log_{10}(k + 1) +", r"q")
        inequality_right[1].set_color(RED)
        label = self.label = MathTex(
            r"{n}",
            r"\log_{10}2"
        )
        label[0].set_color(BLUE)
        label_c = MathTex(
            r"2",
            r"^n",
        )
        label_c[1].set_color(BLUE)
        
        inequality = VGroup(inequality_left, label, inequality_right).arrange(RIGHT, buff=0.2)
        updown = MathTex(r"\Updownarrow")

        starting = MathTex(r"\text{ is starting with: } k" )
        l_starting = VGroup(label_c, starting).arrange(RIGHT, buff=0.2)
        ineq = VGroup(inequality, updown, l_starting)
        ineq.arrange(DOWN, buff=0.25)
        for_s_q.next_to(inequality, UP, aligned_edge=LEFT)
        ineq.add(for_s_q)
        self.formula = ineq
    
    def get_target_inequality(self):
        inequality_left =  MathTex(r"\log_{10}k \leqslant")
        
        inequality_right =  MathTex(r"< \log_{10}(k + 1)")
        
        label = MathTex(
            r"\{", r"{n}",
            r"\log_{10}2", r"\}"
        )
        label_c = MathTex(
            r"2",
            r"^n",
        )
        label_c[1].set_color(BLUE)
        label[0].set_color(YELLOW)
        label[1].set_color(BLUE)
        label[-1].set_color(YELLOW)
        inequality = VGroup(inequality_left, label, inequality_right).arrange(RIGHT, buff=0.2)
        updown = MathTex(r"\Updownarrow")

        starting = MathTex(r"\text{ is starting with: } k" )
        l_starting = VGroup(label_c, starting).arrange(RIGHT, buff=0.2)
        ineq = VGroup(inequality, updown, l_starting)
        ineq.arrange(DOWN, buff=0.25)
        return ineq

    def form_line_to_circule(self, length, pos = 0):
        def updater(mob: VMobject, alpha, length = length):
            if alpha != 1:
                r = (length / (2* PI)) / alpha if alpha != 0 else (length / (2* PI)) / (1/500)
                a = np.sin(length / (2 * r) ) * r
                trip = Line(0.25*LEFT, ORIGIN, stroke_width = 0.25*DEFAULT_STROKE_WIDTH).rotate((1-alpha)*PI/2 - alpha*PI)
                arc_0 = Arc(start_angle = PI, angle = length / (r), radius=r)
                points_list = [arc_0.point_from_proportion(math.log10(i+1)) for i in range(10)]
                arc_list = [ArcBetweenPoints(points_list[i], points_list[i+1], color = HOT_COLORS[i], radius=r, stroke_width = 1.25*DEFAULT_STROKE_WIDTH) for i in range(9)]
                target_mob = VMobject()
                target_mob.add(*arc_list).rotate((1-alpha)*PI/2 - alpha*PI, about_point=ORIGIN)
                arc_0.rotate((1-alpha)*PI/2 - alpha*PI, about_point=ORIGIN)
                target_mob.append_points(arc_0.points)
                trip.move_to(target_mob.point_from_proportion(0))
                target_mob.add(trip)
                mob.become(target_mob.move_to(mob))
            else:
                r = (length / (2* PI))
                arc_0 = Circle(radius=r)
                points_list = [arc_0.point_from_proportion(math.log10(i+1)) for i in range(10)]
                arc_list = [ArcBetweenPoints(points_list[i], points_list[i+1], color = HOT_COLORS[i], radius=r, stroke_width = 1.25*DEFAULT_STROKE_WIDTH) for i in range(9)]
                target_mpb = ArcPolygonFromArcs(*arc_list)
                trip = Line(0.25*LEFT, ORIGIN, stroke_width = 0.25*DEFAULT_STROKE_WIDTH).rotate((1-alpha)*PI/2 - alpha*PI)
                trip.move_to(target_mpb.point_from_proportion(0))
                target_mpb.add(trip)
                mob.become(target_mpb.move_to(mob))
        return updater

class TestArc(Scene):
    def construct(self):
        a = fractional_numberline =  NumberLine(
            x_range=[0, 0.9999, 1],
            length=47/20,
            include_tip=False,
            include_numbers=True,
            include_ticks=True
        )
        fractional_numberline.to_edge(LEFT)
        self.play(UpdateFromAlphaFunc(fractional_numberline, self.form_line_to_circule(47/20)), run_time = 3)

    def form_line_to_circule(self, length, pos = 0):
        def updater(mob: VMobject, alpha, length = length):
            if alpha != 1:
                r = (length / (2* PI)) / alpha if alpha != 0 else (length / (2* PI)) / (1/500)
                a = np.sin(length / (2 * r) ) * r
                trip = Line(0.25*LEFT, ORIGIN, stroke_width = 0.25*DEFAULT_STROKE_WIDTH).rotate((1-alpha)*PI/2 - alpha*PI)
                arc_0 = Arc(start_angle = PI, angle = length / (r), radius=r)
                points_list = [arc_0.point_from_proportion(math.log10(i+1)) for i in range(10)]
                arc_list = [ArcBetweenPoints(points_list[i], points_list[i+1], color = HOT_COLORS[i], radius=r, stroke_width = 1.25*DEFAULT_STROKE_WIDTH) for i in range(9)]
                target_mob = VMobject()
                target_mob.add(*arc_list).rotate((1-alpha)*PI/2 - alpha*PI, about_point=ORIGIN)
                arc_0.rotate((1-alpha)*PI/2 - alpha*PI, about_point=ORIGIN)
                target_mob.append_points(arc_0.points)
                trip.move_to(target_mob.point_from_proportion(0))
                target_mob.add(trip)
                mob.become(target_mob.move_to(mob))
            else:
                r = (length / (2* PI))
                arc_0 = Circle(radius=r)
                points_list = [arc_0.point_from_proportion(math.log10(i+1)) for i in range(10)]
                arc_list = [ArcBetweenPoints(points_list[i], points_list[i+1], color = HOT_COLORS[i], radius=r, stroke_width = 1.25*DEFAULT_STROKE_WIDTH) for i in range(9)]
                target_mpb = ArcPolygonFromArcs(*arc_list)
                trip = Line(0.25*LEFT, ORIGIN, stroke_width = 0.25*DEFAULT_STROKE_WIDTH).rotate((1-alpha)*PI/2 - alpha*PI)
                trip.move_to(target_mpb.point_from_proportion(0))
                target_mpb.add(trip)
                mob.become(target_mpb.move_to(mob))
        return updater
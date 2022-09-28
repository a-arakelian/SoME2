from manim import *
import math
import random
import numpy as np

COLORS = [
    "#66ccff"
    "#00aaff",
    "#009bef",
    "#008ddf",
    "#007fcf",
    "#0071c0",
    "#0063b0",
    "#0056a1",
    "#004992",
    "#003d84",
    "#003175",
    "#002667",
    "#001c5a",
    "#000000"
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
    "#bad80f"
]

def interpolate(start, end):
    def r(t):
        return (1-t) * start + t * end
    return r

def surround_object(mob, buff = 0.1):
    mob_width = mob.get_edge_center(RIGHT)[0] - mob.get_edge_center(LEFT)[0]
    mob_height = mob.get_edge_center(UP)[1] - mob.get_edge_center(DOWN)[1]
    round_rect_width = mob_width + 2 * buff
    round_rect_height = mob_height + 2 * buff
    round_rect = RoundedRectangle()
    round_rect.stretch_to_fit_height(round_rect_height)
    round_rect.stretch_to_fit_width(round_rect_width)
    round_rect.move_to(mob)

def n_power_of_a(a, n, font_size = DEFAULT_FONT_SIZE, eq = True):
    num = int(pow(a, n))
    a_of = "{:,}".format(int(a))
    of_n = "{:,}".format(int(n))
    of_n = '^' + '{' + of_n + '}'
    equal = r'='
    answer = r"{:,}".format(num)
    if eq:
        formula = MathTex(a_of, of_n, equal, answer, font_size = font_size)
    else:
        formula = MathTex(a_of, of_n, r",", font_size = font_size)
    formula[1].set_color(BLUE)
    digits = int(math.log10(num))
    first_digit = int(num / pow(10, digits))
    formula.first_digit = first_digit
    return formula

def if_first_digit_is(group, digit):
    group_with_first_digit = VGroup()
    for p in group:
        if p.first_digit == digit:
            group_with_first_digit.add(p)
    return group_with_first_digit

def if_first_digit_not(group, digit):
    group_with_first_digit = VGroup()
    for p in group:
        if p.first_digit != digit:
            group_with_first_digit.add(p)
    return group_with_first_digit

def get_dot(mob):
    d = Dot().scale(2)
    d.match_color(mob)
    d.move_to(mob)
    return d

def prob_form(mob, text):
    p = MathTex(r"P(", r")")
    tex = MathTex(text)
    p[0].next_to(mob, LEFT, buff=0.18)
    p[1].next_to(mob, RIGHT, buff=0.18)
    tex.next_to(p[1], RIGHT, buff=0.18)
    return VGroup(p[0], mob, p[1], tex)

def prob_from_y_b_sec(sec: VGroup, up_limit = 3, buff = 0.1, diff_color = HOT_COLORS[0], text_label = r"YELLOW"):
    sec[up_limit:].set_opacity(0.4)
    sec[:up_limit].set_opacity(1)
    rec = Rectangle()
    rec.stretch_to_fit_width(
        sec[:up_limit].get_edge_center(RIGHT)[0]-sec[:up_limit].get_edge_center(LEFT)[0] + buff
    )
    rec.stretch_to_fit_height(
        sec[:up_limit:].get_edge_center(UP)[1]-sec[:up_limit].get_edge_center(DOWN)[1] + buff
    )
    rec.set_color(WHITE)
    rec.move_to(sec[:up_limit])

    color = Dot().set_color(diff_color)
    diff = color.get_color()

    count = 0
    for p in sec[:up_limit]:
        if p.get_color() == diff:
            count += 1

    

    
    white_dots = VGroup(*[Dot(radius = 0.2, color=WHITE) for _ in range(up_limit)])
    white_dots.arrange(DOWN)
    white_dots.align_to([0, 4.5, 0], LEFT+UP)
    white_dots.set_opacity(0.8)

    diff_dots = VGroup(*[Dot(radius = 0.2, color=diff_color) for _ in range(count)])
    diff_dots.arrange(DOWN)
    diff_dots.align_to([2, 4.5, 0], LEFT+UP)
    diff_dots.set_opacity(0.8)


    total = r"{:,}".format(int(up_limit))
    success = r"{:,}".format(int(count))

    beace_left = Brace(white_dots, LEFT).set_opacity(0.8)
    beace_left_text = MathTex(total).set_opacity(0.8)
    beace_left_text.next_to(beace_left, LEFT)

    beace_right = Brace(diff_dots, RIGHT).set_opacity(0.8)
    beace_right_text = MathTex(success).set_opacity(0.8)
    beace_right_text.next_to(beace_right, RIGHT)

    ul_text = MathTex(r"\text{number of elements: } ", total).next_to(diff_dots, RIGHT, aligned_edge=UP, buff = 3)
    label = Tex(text_label).set_color(diff_color)
    answer = float(count)/float(up_limit)
    answer = "=" + str(round(answer, 3))
    prob = prob_form(label, answer).next_to(ul_text, DOWN, aligned_edge=LEFT, buff = 2)

    to_return = VGroup(
        rec,                        #0
        white_dots,                 #1
        beace_left,                 #2
        beace_left_text,            #3 
        diff_dots,                  #4
        beace_right,                #5
        beace_right_text,           #6
        ul_text,                    #7
        prob                        #8
    )
    return to_return

    
def random_in_circle(n, radius=1):
    l = []
    for i in range(n):
        rand = random.random()
        r = rand**(1/(2 - rand/2)) * radius
        l.append([r * math.cos((2*PI * i)/n), r * math.sin((2*PI * i)/n), 0])
    random.shuffle(l)
    return(l)

class PlayingCards:
    def __init__(self, n=0, scale_factor = 1) -> None:
        self.scale_factor = scale_factor
        self.n = n
        self.back = self.get_back(scale_factor)
        self.front = self.get_front(n, scale_factor)

    def rotate_front_back(self, object : VMobject, pos = None, rot =None, scale = None):
        n = self.n
        if pos == None:
            def p(t):
                return object.get_center()
            pos = p
        if rot == None:
            def r(t):
                return 0
            rot = r
        if scale == None:
            def s(t):
                scale_factor = self.scale_factor
                return scale_factor
            scale = s
        
        self.scale_factor = scale(1)

        def rotate(mob: VMobject, alpha: float):

            alpha
            def get_width(t, scale):
                width = self.surrounding_rectangle(scale)[1].scale(scale).width
                l = math.cos(alpha*PI)*width
                return abs(l)
            if alpha <= 0.5:
                mob.become(
                    self.get_front(self.n, scale(alpha))
                    .stretch_to_fit_width(get_width(alpha, scale(alpha)))
                    .rotate(rot(alpha))
                    .move_to(pos(alpha))
                    
                )
            else:
                mob.become(
                    self.get_back(scale(alpha))
                    .stretch_to_fit_width(get_width(alpha, scale(alpha)))
                    .rotate(rot(alpha))
                    .move_to(pos(alpha))
                )
        return rotate

    def rotate_back_front(self, object : VMobject, pos = None, rot =None, scale = None):
        n = self.n
        object_width = object.width
        if pos == None:
            def p(t):
                return object.get_center()
            pos = p
        if rot == None:
            def r(t):
                return 0
            rot = r
        if scale == None:
            def s(t):
                scale_factor = self.scale_factor
                return scale_factor
            scale = s

        self.scale_factor = scale(1)

        def rotate(mob: VMobject, alpha: float):

            alpha
            def get_width(t, scale):
                width = self.surrounding_rectangle(scale)[1].scale(scale).width
                l = math.cos(alpha*PI)*width
                return abs(l)
            if alpha <= 0.5:
                mob.become(
                    self.get_back(scale(alpha))
                    .stretch_to_fit_width(get_width(alpha, scale(alpha)))
                    .rotate(rot(alpha))
                    .move_to(pos(alpha))
                )
            else:
                mob.become(
                    self.get_front(self.n, scale(alpha))
                    .stretch_to_fit_width(get_width(alpha, scale(alpha)))
                    .rotate(rot(alpha))
                    .move_to(pos(alpha))
                )
        return rotate




    def get_front(self, n,  scale_factor):
        rec, r_rec, m_rec = self.surrounding_rectangle(scale_factor)
        number = MathTex(r"2", r"^{" + r"{:,}".format(int(n)) + r"}").scale(1.5)
        number[1].set_color(BLUE)
        number.align_to(rec, UL)
        number_r = number.copy().rotate(180*DEGREES).align_to(rec, DR)
        
        digits = int(math.log10(pow(2,n)))
        starting_n = int(pow(2,n)/pow(10, digits))
        starting_number = MathTex(r"{:,}".format(starting_n)).scale(4.2)
        starting_number.set_color(HOT_COLORS[starting_n-1])
        number_v = MathTex(r"{:,}".format(int(pow(2,n))))
        if number_v.width > rec.width:
            number_v.scale_to_fit_width(rec)

        starting_number.next_to(number_v, UP) #.shift((starting_number.width+0.05)/2*RIGHT)
        starting_number_r = starting_number.copy().rotate(180*DEGREES).next_to(number_v, DOWN) #.shift((starting_number.width+0.05)/2*LEFT)
      
        
        r_rec.set_stroke(color=WHITE)
        r_rec.set_fill(color= HOT_COLORS[starting_n-1], opacity=1)

        m_rec.set_stroke(color=HOT_COLORS[starting_n-1])
        m_rec.set_fill(color= GRAY_E, opacity=1)

        return VGroup(r_rec, m_rec, VGroup(number, number_r), VGroup(starting_number, starting_number_r), number_v).scale(scale_factor)

    def get_back(self, scale_factor):
        rec, r_rec, m_rec = self.surrounding_rectangle(scale_factor)
        r_rec.set_fill(GRAY_E, 1)
        lines = self.get_lines(scale_factor, rec).set_z_index(1)
        return VGroup(
            r_rec,
            m_rec,
            lines,
            rec
        ).scale(scale_factor)

    def surrounding_rectangle(self, scale_factor):
        rec = Rectangle(height=6.0, width=4.0, stroke_width = scale_factor*DEFAULT_STROKE_WIDTH).scale(0.8)
        r_rec = SurroundingRectangle(rec, corner_radius=scale_factor*0.25, color=GRAY_A, fill_opacity = 0.2, stroke_width = scale_factor*0.8*DEFAULT_STROKE_WIDTH, buff = scale_factor*0.2).set_z_index(-2)
        m_rec = SurroundingRectangle(rec, corner_radius=scale_factor*0.1, color=RED, stroke_width = scale_factor*1.2*DEFAULT_STROKE_WIDTH, buff = scale_factor*0.1).set_z_index(-1)
        return [rec, r_rec, m_rec]
    def get_lines(self, scale_factor, rec):
        lines = VGroup()
        for i in range(1, 20):
            a = (28 + i) % 40
            b = (28 - i) % 40
            lines.add(
                Line(rec.point_from_proportion(a/40), rec.point_from_proportion(b/40), stroke_width = scale_factor*0.8*DEFAULT_STROKE_WIDTH).set_color(HOT_COLORS[int((i)%9)]).add(
                    Line(rec.point_from_proportion(((a+0.25)/40)%1), rec.point_from_proportion(((b-0.25)/40)%1), stroke_width = scale_factor*0.2*DEFAULT_STROKE_WIDTH).set_color(HOT_COLORS[int((i)%9)]),
                    Line(rec.point_from_proportion(((a-0.25)/40)%1), rec.point_from_proportion(((b+0.25)/40)%1), stroke_width = scale_factor*0.2*DEFAULT_STROKE_WIDTH).set_color(HOT_COLORS[int((i)%9)])
                )
            )
            a = (20 + i) % 40
            b = (20 - i) % 40
            lines.add(
                Line(rec.point_from_proportion(a/40), rec.point_from_proportion(b/40), stroke_width = scale_factor*0.8*DEFAULT_STROKE_WIDTH).set_color(HOT_COLORS[int((i)%9)]).add(
                    Line(rec.point_from_proportion(((a+0.25)/40)%1), rec.point_from_proportion(((b-0.25)/40)%1), stroke_width = scale_factor*0.2*DEFAULT_STROKE_WIDTH).set_color(HOT_COLORS[int((i)%9)]),
                    Line(rec.point_from_proportion(((a-0.25)/40)%1), rec.point_from_proportion(((b+0.25)/40)%1), stroke_width = scale_factor*0.2*DEFAULT_STROKE_WIDTH).set_color(HOT_COLORS[int((i)%9)])
                )
            )
        return lines

class Distribution(Axes):
    def __init__(self, base = 2, up_limit = 10, x_length = 5, y_length = 3, **kwargs):
        self.base = base
        self.up_limit = up_limit
        pr = 1 if base == 10 else 0.5
        super().__init__(
            x_range=[0, 9, 1],
            y_range=[0, pr],
            x_length = x_length,
            y_length = y_length,
            tips = False,
            **kwargs
        )
        self.x_nums = VGroup(
            *[
                Integer()
                .scale(0.75)
                .set_value(k)
                .next_to(self.c2p(k-1, 0), DR, buff = 0.2)
                for k in range(1,10)
            ]
        )
        
        self.y_nums = VGroup(
            *[
                Integer(k, unit="\\%")
                .scale(0.55)
                .next_to(self.c2p(0, k / 100), LEFT, buff = 0.15)
                for k in range(0, 60, 10)
            ]
        )
        self.text_up_limit = (
            Tex("number of elements: ")
            .scale(0.6)
            .next_to(self, UP, aligned_edge=RIGHT)
        )
        counter_1 = (
            Integer(self.up_limit)
            .scale(0.6)
            .next_to(self.text_up_limit, RIGHT, buff=0.3)
        )
        

        self.text_base = (
            Tex("base: ")
            .scale(0.6)
            .next_to(self.text_up_limit, DOWN, aligned_edge=RIGHT)
        )
        counter_2 = (
            Integer(self.base)
            .scale(0.6)
            .next_to(self.text_base, RIGHT, buff=0.3)
        )
        self.text_up_limit.add(counter_1)
        self.text_base.add(counter_2)


        self.bars = self.get_bars()
        self.add(self.x_nums, self.y_nums, self.bars, self.text_up_limit, self.text_base)

    def get_list_of_powers(self):
        return [pow(self.base, n) for n in range(self.up_limit)]
    def get_distribution(self):
        distribution = [
            0, 0, 0, 0, 0, 0, 0, 0, 0
        ]
        for p in self.get_list_of_powers():
            digits = int(math.log10(p))
            first_digit = int(p / pow(10, digits))
            distribution[first_digit - 1] += 1/self.up_limit
        return distribution    
        
    def get_bars(self):
        distribution = self.get_distribution()
        bars = VGroup()
        for i in range(9):
            p1 = VectorizedPoint().move_to(self.c2p(i, 0))
            p2 = VectorizedPoint().move_to(self.c2p(i + 1, 0))
            p3 = VectorizedPoint().move_to(self.c2p(i + 1, distribution[i]))
            p4 = VectorizedPoint().move_to(self.c2p(i, distribution[i]))
            points = VGroup(p1, p2, p3, p4)
            bar = Rectangle().replace(points, stretch=True)
            bars.add(bar)
        descending_order = [i[0] for i in sorted(enumerate(distribution), key=lambda k: k[1], reverse=True)]
        for i in range(9):
            bars[descending_order[i]].set_style(
                stroke_width=1,
                fill_color=[GRAY_A, COLORS[i]],
                fill_opacity=0.9,
                stroke_color=[GRAY, COLORS[i]]
            )
        return bars

class StartingWith(RoundedRectangle):
    def __init__(self, digit = 1, size_scale = 1, **kwargs):
        self._p = 0 
        text_1 = r"\text{leading digit}: "
        text_2 = r"{:,}".format(int(digit))
        label = MathTex(text_1 + text_2).scale(0.6)
        position = VGroup(*[VectorizedPoint() for _ in range(9)])
        position.arrange_in_grid(3, 3, (0.2, 0.15), flow_order="rd")
        size = size_scale * (label.get_edge_center(RIGHT)[0] - label.get_edge_center(LEFT)[0] + 0.2)
        super().__init__(corner_radius = 0.1, stroke_width=2, **kwargs)
        self.stretch_to_fit_height(size)
        self.stretch_to_fit_width(size)
        position.match_width(self)
        position.scale(0.7)
        rectangle = Rectangle()
        rectangle.stretch_to_fit_width(size)
        rectangle.stretch_to_fit_height(
            label.get_edge_center(UP)[1] - label.get_edge_center(DOWN)[1] + 0.1)
        rectangle.align_to(self, UP)
        self.semirect = Intersection(rectangle, self)
        position.next_to(rectangle, DOWN, buff=0.1)
        self.position = position
        self.semirect.set_style(
            fill_color=HOT_COLORS[digit-1],
            stroke_color=HOT_COLORS[digit-1],
            fill_opacity=0.65,
            stroke_width=2
        )
        self.label = label.move_to(self.semirect)
        self.add(self.semirect, self.label, position)

    def next_p(self):
        i = self._p
        self._p += 1
        return self.position[i]

class LeadingDigit(Scene):
    def construct(self):
        number = MathTex("3", "2768").scale(2.25).to_edge(RIGHT, buff=1).shift(1.25*UP)
        self.add(number)
        sr = SurroundingRectangle(number[0])
        l = Line([2.5, -0.75, 0], sr.get_bottom(), buff=0.01, stroke_width=0.8*DEFAULT_STROKE_WIDTH).add_tip(tip_length=0.25)
        text = Tex("leading digit").scale(1.5).next_to(l.get_start(), DOWN)
        self.play(AnimationGroup(
            Create(sr),
            GrowFromPoint(l, [2.5, -0.75, 0]),
            FadeIn(text),
            lag_ratio=0.3
        ))
        self.wait(2.5)

class PowersofA(Scene):
    def construct(self):
        powers_of_two = VGroup(*[n_power_of_a(2, n, 25) for n in range(60)])
        powers_of_two.arrange_in_grid(15, 4, (1.1, 0.23), col_alignments = "llll", flow_order="dr")
        self.play(
            AnimationGroup(*[FadeIn(p) for p in powers_of_two], lag_ratio = 0.5),
            run_time = 8
        )
        self.wait(2)
        self.play(
            powers_of_two.animate.set_opacity(0.4),
            run_time = 0.8
        )
        self.wait()
        for k in range(1, 10):
            lag_r = 0.05 if k > 2 else 0.5
            self.play(
                if_first_digit_is(powers_of_two, k).animate.set_opacity(1),
                run_time = lag_r * 1.5
            )
            self.play(AnimationGroup(
                *[
                    p[-1]
                    .animate
                    .set_color(HOT_COLORS[k-1])
                    for p in if_first_digit_is(powers_of_two, k)
                ],
                lag_ratio=lag_r
            ), run_time = lag_r * 6 / (2*k**(1/2)))
            self.wait(1 / (3*k**(1/3)))
        self.wait()

        for i in range(59):
            if (i + 1) % 15 != 0:
                arrow = Line(
                    powers_of_two[i].get_edge_center(RIGHT),
                    powers_of_two[i+1].get_edge_center(RIGHT),
                    buff= 0.08,
                    path_arc=-2
                ).add_tip(tip_length = 0.15)
                arrow.set_color([
                    HOT_COLORS[powers_of_two[i+1].first_digit - 1],
                    HOT_COLORS[powers_of_two[i].first_digit - 1]
                ])
                powers_of_two[i].arrow = arrow
            else:
                arrow = VMobject()
                powers_of_two[i].arrow = arrow
        self.play(if_first_digit_not(powers_of_two, 1).animate.set_opacity(0.4), run_time = 0.5)
        self.wait()
        self.play(if_first_digit_is(powers_of_two, 2).animate.set_opacity(1))
        self.play(if_first_digit_is(powers_of_two, 3).animate.set_opacity(1))
        self.play(AnimationGroup(
                *[
                    FadeIn(p.arrow)
                    for p in if_first_digit_is(powers_of_two, 1)
                ],
                lag_ratio=0.6
            ), run_time = 6)
        
        self.wait()
        self.play(
            if_first_digit_not(powers_of_two, 4).animate.set_opacity(0.4),
            if_first_digit_is(powers_of_two, 4).animate.set_opacity(1),
            *[
                FadeOut(p.arrow)
                for p in if_first_digit_is(powers_of_two, 1)
            ]
        )
        self.wait()
        self.play(if_first_digit_is(powers_of_two, 8).animate.set_opacity(1))
        self.play(if_first_digit_is(powers_of_two, 9).animate.set_opacity(1))
        self.play(AnimationGroup(
                *[
                    FadeIn(p.arrow)
                    for p in if_first_digit_is(powers_of_two, 4)
                ],
                lag_ratio=0.5
            ), run_time = 3)
        self.wait()
        self.play(
            powers_of_two.animate.set_opacity(1),
            *[
                FadeOut(p.arrow)
                for p in if_first_digit_is(powers_of_two, 4)
            ]
        )
        self.wait()
        self.play(FadeOut(powers_of_two[30:]))

        boxes = VGroup(*[
            StartingWith(k+1).scale(0.8) for k in range(9)
        ])

        boxes.arrange_in_grid(3, 3, (0.2, 0.2), flow_order="rd")
        boxes.move_to([3, 0, 0])
        self.play(FadeIn(boxes))
        self.wait()
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        p[:2].animate.next_to(boxes[p.first_digit - 1].next_p(), DOWN, buff=0),
                        FadeOut(p[2:], rate_func = lambda x: x**(1/3))
                    )
                    for p in powers_of_two[:30]
                ],
                lag_ratio = 0.7
            ),
            run_time = 8
        )
        self.wait(2)
        len_list = [len(if_first_digit_is(powers_of_two[:30], k+1)) for k in range(9)]
        
        count = VGroup()
        for i in range(9):
            count.add(
                MathTex(r"{:,}".format(int(len_list[i]))).scale(2)
                .move_to(boxes[i].position[4]).set_color(HOT_COLORS[i])
            )
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        FadeOut(if_first_digit_is(powers_of_two[:30], i+1), rate_func = lambda x: x**(1/3)),
                        Write(count[i])
                    )
                    for i in range(9)
                ],
                lag_ratio=0.5
            )
        )

        def prob_formula(n):
            text_1 = r"\text{leading digit}: "
            text_2 = "{:,}".format(int(n))
            text_3 = "{:,}".format(int(len_list[n-1]))
            formula = MathTex(
                r"P(",
                text_1 + text_2,
                r") =",
                r"\frac{" + text_3+ r"}{30}"
            )               
            formula[1].set_color(HOT_COLORS[n-1])
            formula[3][0].set_color(HOT_COLORS[n-1])
            formula[3][2:].set_color(HOT_COLORS)
            return formula.scale(0.9)
        formula_summ = MathTex(
                "9+6+3+3+3+3+0+3+0=", "30"
            ).scale(0.7)
        for i in range(0, 17, 2):
            formula_summ[0][i].set_color(HOT_COLORS[int(i/2)])
        formula_summ[1].set_color(HOT_COLORS)
        formula_summ.to_edge(UL)
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        ReplacementTransform(count[i].copy(), formula_summ[0][2*i]),
                        Write(formula_summ[0][2*i+1]),
                        lag_ratio=0.8
                    )
                    for i in range(9)
                ],
                Write(formula_summ[1]),
                lag_ratio=0.5
            ), run_time = 2.5
        )
        self.wait()
        self.play(FadeOut(formula_summ))
        formulas = VGroup(*[prob_formula(i+1).to_edge(UL) for i in range(9)])
        self.play(Write(formulas[0]))
        self.wait(2)
        for i in range(8):
            self.play(ReplacementTransform(formulas[i], formulas[i+1]), run_time=1/((i+1)**(1/2)))
            self.wait(0.5/((i+1)**(1/3)))   
           

        self.wait(0)

        dist = Distribution(2, 30).move_to([-3.75, -0.5, 0]).scale(1.05).align_to(boxes, DOWN)
        [dist.bars[i].set_color(HOT_COLORS[i]) for i in range(9)]

        self.play(Write(dist))
        self.wait(2)
        self.play(FadeOut(boxes, count, formulas[-1]))

        
        set_of_pow = VGroup(*[n_power_of_a(2, k, eq = False) for k in range(30)])
        set_of_pow[-1].remove(set_of_pow[-1][-1])
        set_of_pow.arrange(RIGHT, buff=0.15,  aligned_edge=UP)
        set_of_pow_br = MathTex(r"A = \{", r"\}")
        set_of_pow_br[0].next_to(set_of_pow, LEFT, buff=0.15)
        set_of_pow_br[1].next_to(set_of_pow, RIGHT, buff=0.15)
        set_of_pow.add(set_of_pow_br)
        set_of_pow.scale(0.52)
        
        set_of_pow.to_edge(UL, buff=0.15).shift(0.15*DOWN)
        count_30 = VGroup(*[
            MathTex("{:,}".format(int(n))).scale(0.4).next_to(set_of_pow[n-1][0], DOWN, buff=0.1) for n in range(1, 31)
        ])
        count_30.set_color(RED)
        self.play(
            Write(set_of_pow),
        )
        self.wait()
        self.play(
            AnimationGroup(
                *[
                    FadeIn(c, rate_func=rate_functions.there_and_back)
                    for c in count_30
                ],
                lag_ratio=0.05
            ),
            Circumscribe(dist.text_up_limit, run_time = 3),
            run_time = 3
        )
        self.wait()
        self.play(
            AnimationGroup(
                *[
                    set_of_pow[n-1][0].animate(rate_func=rate_functions.there_and_back).set_color(RED)
                    for n in range(1, 31)
                ],
                lag_ratio=0.05
            ),
            Circumscribe(dist.text_base, run_time = 3),
            run_time = 3
        )
        s_s = VGroup(*[
                        MathTex(r"\text{leading digit}: ", r"{:,}".format(int(n+1)))
                        .set_color(HOT_COLORS[n]) for n in range(9)
        ])
        p_s = VGroup(
            *[
                VGroup(
                    MathTex(r"\{"),
                    n_power_of_a(2, k, eq = False)[:-1],
                    MathTex(r"\}")
                ).arrange(RIGHT, buff=0.17)
                
                for k in range(30)
            ]
        )
        p_s.move_to([3, 1.7, 0])
        s_s.move_to([3, 1.7, 0])

        
        p_1 = prob_form(s_s[0], r"=\frac{3}{10}" )
        p_2 = prob_form(s_s[1], r"=\frac{2}{10}" )
        p_3 = prob_form(s_s[2], r"=\frac{1}{10}" )
        p_4 = prob_form(s_s[3], r"=\frac{1}{10}" )
        p_5 = prob_form(s_s[4], r"=\frac{1}{10}" )
        p_6 = prob_form(s_s[5], r"=\frac{1}{10}" )
        p_7 = prob_form(s_s[6], r"=\frac{0}{10}" )
        p_8 = prob_form(s_s[7], r"=\frac{1}{10}" )
        p_9 = prob_form(s_s[8], r"=\frac{0}{10}" )

        p_sw_g = [p_1, p_2, p_3, p_4, p_5, p_6, p_7, p_8, p_9]

        p_ss_g =VGroup(*[prob_form(p, r"=\frac{1}{30}") for p in p_s])

        question_marck = MathTex(r"?")
        question_marck.next_to(p_1[-1][0], UP)  

        self.play(Write(p_1))

        self.play(Indicate(question_marck))
        self.wait()
        self.play(FadeOut(question_marck, p_1))

        self.play(Write(
            p_ss_g[0]
        ))
        self.wait()
        for i in range(29):
            self.play(ReplacementTransform(p_ss_g[i], p_ss_g[i+1]), run_time = 0.3)
        self.wait()
        self.play(FadeOut(p_ss_g[-1]))
        self.play(
            FadeIn(p_1),
            if_first_digit_is(set_of_pow[:30], 1).animate.set_color(HOT_COLORS[0])
        )
        self.wait()
        for i in range(0, 8):
            self.play(
                ReplacementTransform(p_sw_g[i], p_sw_g[i+1]),
                if_first_digit_is(set_of_pow[:30], i+2).animate.set_color(HOT_COLORS[i+1])
            )
        self.wait(3)

class ProbabilityChart(MovingCameraScene):
    def construct(self):
        x = ValueTracker(2)
        d_p2 = always_redraw(lambda: Distribution(2, int(x.get_value())).align_to([-6.5, -2, 0], LEFT + DOWN))
        d_p3 = always_redraw(lambda: Distribution(3, int(x.get_value())).align_to([0.5, -2, 0], LEFT + DOWN))
        d_p4 = always_redraw(lambda: Distribution(4, int(x.get_value())).align_to([7.5, -2, 0], LEFT + DOWN))

        d_p5 = always_redraw(lambda: Distribution(5, int(x.get_value())).align_to([-6.5, -8, 0], LEFT + DOWN))
        d_p6 = always_redraw(lambda: Distribution(6, int(x.get_value())).align_to([0.5, -8, 0], LEFT + DOWN))
        d_p7 = always_redraw(lambda: Distribution(7, int(x.get_value())).align_to([7.5, -8, 0], LEFT + DOWN))

        d_p8 = always_redraw(lambda: Distribution(8, int(x.get_value())).align_to([-6.5, -14, 0], LEFT + DOWN))
        d_p9 = always_redraw(lambda: Distribution(9, int(x.get_value())).align_to([0.5, -14, 0], LEFT + DOWN))
        d_p10 = always_redraw(lambda: Distribution(10, int(x.get_value())).align_to([7.5, -14, 0], LEFT + DOWN))

        self.add(
            d_p2, 
            d_p3, 
            d_p4, 
            d_p5, 
            d_p6, 
            d_p7, 
            d_p8, 
            d_p9, 
            d_p10
        )
        self.play(
            self.camera.frame.animate(rate_func = lambda x: rate_functions.lingering(x)**(1/2)).scale(2.1).move_to(d_p6),
            x.animate(rate_func=rate_functions.ease_in_out_sine).set_value(300),
            run_time = 10)
        self.wait()
        self.play(
            x.animate(rate_func=rate_functions.there_and_back).set_value(10),
            run_time = 10
        )
        d_p2.clear_updaters()
        d_p3.clear_updaters()
        d_p4.clear_updaters()
        d_p5.clear_updaters()
        d_p6.clear_updaters()
        d_p7.clear_updaters()
        d_p8.clear_updaters()
        d_p9.clear_updaters()
        d_p10.clear_updaters()

        d_list = [d_p2, d_p3, d_p4, d_p5, d_p6, d_p7, d_p8, d_p9, d_p10]

       
        

        self.play(
                self.camera.frame.animate.scale(1/3.2).move_to(d_p10),
                run_time = 1
        )
        
        self.wait()
        self.play(
            Circumscribe(d_p10)
        )
        self.wait()

class WhatIsProbably(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()

        pow_of_two = VGroup(
            *[n_power_of_a(2, i, eq=False) for i in range(30)]
        ).arrange_in_grid(2, 15, buff=(0.2, 0.4))
        [p.remove(p[-1]) for p in pow_of_two]
        self.play(FadeIn(pow_of_two))
        self.wait()
        self.play(
            if_first_digit_is(pow_of_two, 1)
            .animate.set_color(HOT_COLORS[0]),
            if_first_digit_not(pow_of_two, 1)
            .animate.set_color(BLUE)
        )
        self.wait()

        dots = VGroup(
            *[get_dot(p) for p in pow_of_two]
        )

        self.play(
            AnimationGroup(
                *[
                    ReplacementTransform(p1, p2)
                    for p1, p2 in zip(pow_of_two, dots)
                ], lag_ratio=0.2
            ),
            run_time = 2
        )

        pos_list = random_in_circle(n=30, radius=3.25)
        bounding_circle = Circle(3.5, WHITE)
        self.wait()
        self.play(
            *[p.animate.move_to(pos) for p, pos in zip(dots, pos_list)]
        )
        self.play(Create(bounding_circle))
        self.wait()
        for i in range(4):
            pos_list = random_in_circle(n=30, radius=3.25)
            self.play(
                *[p.animate.move_to(pos) for p, pos in zip(dots, pos_list)],
                run_time = 0.25*(1.7 - rate_functions.there_and_back_with_pause(i/3))
            )
            self.wait(0.3*(2 - rate_functions.there_and_back_with_pause(i/3)))
        self.wait(1)
        self.play(FadeOut(bounding_circle, dots))

        infty_p_of_two = VGroup(
            *[n_power_of_a(2, i, eq=False) for i in range(500)]
        ).arrange(RIGHT).align_to(4*LEFT+UP, LEFT+UP)
        [p.remove(p[-1]) for p in infty_p_of_two]
        self.play(FadeIn(infty_p_of_two))
        self.wait(1)
        self.play(
                self.camera.frame.animate(rate_func = rate_functions.ease_in_out_circ).scale(2).move_to(infty_p_of_two[438]),
                run_time = 6
        )
        self.wait()
        self.play(Restore(self.camera.frame))
        p_1 = if_first_digit_is(infty_p_of_two, 1)
        p_n1 = if_first_digit_not(infty_p_of_two, 1)
        self.play(
            p_1.animate.set_color(HOT_COLORS[0]),
            p_n1.animate.set_color(BLUE)
        )
        p_1copy = p_1[:32].copy()
        p_n1copy = p_n1[:32].copy()

        anim_list = []
        for i in range(32):
            anim_list.append(p_1copy[i].animate.next_to(infty_p_of_two[2*i], DOWN, buff = 2))
            anim_list.append(p_n1copy[i].animate.next_to(infty_p_of_two[2*i+1], DOWN, buff = 2))

        self.play(
            AnimationGroup(*anim_list, lag_ratio=0.7),
            self.camera.frame
            .animate(rate_func = lambda x: rate_functions.lingering(x)**(1/2))
            .scale(2).move_to(infty_p_of_two[15]),
            run_time = 12
        )
        
        self.remove(infty_p_of_two[40:])
        [infty_p_of_two.remove(infty_p_of_two[i]) for i in range(499, 39, -1)]

        init_dot = VGroup(*[get_dot(p) for p in infty_p_of_two])
        
        rot_sec = VGroup()
        for i in range(32):
            rot_sec.add(p_1copy[i])
            rot_sec.add(p_n1copy[i])

        rot_dot = VGroup(*[get_dot(p) for p in rot_sec])

        self.wait()
        self.play(Circumscribe(infty_p_of_two))
        self.wait()
        self.play(Circumscribe(rot_sec))
        
        self.play(
            ReplacementTransform(infty_p_of_two, init_dot),
            FadeOut(rot_sec)
        )
        self.play(init_dot.animate.shift(6*UP))

        self.play(init_dot.animate.set_opacity(0.4))
        x = ValueTracker(1)
        ch = always_redraw(lambda: prob_from_y_b_sec(init_dot, int(x.get_value())))
        self.play(Write(ch))
        self.play(Circumscribe(ch[7]))
        self.wait(2)
        for i in range(1, 50):
            self.play(x.animate.set_value(i+0.2), run_time = 1/59)
            self.wait(0.2*(1.5 - rate_functions.there_and_back_with_pause((i-1)/17)))

        self.wait(5)

class PlayingCardsScene(MovingCameraScene):
    def construct(self):
        playing_cards = [PlayingCards(i, scale_factor=0.5) for i in range(30)]
        cards = VGroup(*[p.front.copy().shift(2*UP) for p in playing_cards])
        for i in range(30):
            cards[i].set_z_index(i)

        self.play(Rotating(cards, radians = PI/3.2, about_point=[0, -4.8, 0]), run_time = 0.5)    
        for i in range(29):
            self.play(Rotating(cards[i+1:], radians = -(1/29)*PI*2/3.2, about_point=[0, -4.8, 0], rate_func=rate_functions.linear), run_time = 1.5/29)
        self.wait(3)

        for i in range(30):
            cards[29-i].set_z_index(29+i)
            self.play(
                UpdateFromAlphaFunc(
                    cards[29-i],
                    playing_cards[29-i].rotate_front_back(
                        cards[29-i],
                        pos = interpolate(cards[29-i].get_center(), np.array([4+(i/580), -2.5+(i/580), 0])),
                        rot = interpolate(PI/3.2 - ((29-i)/29)*PI*2/3.2, -PI/2),
                        scale= interpolate(0.5, 0.45)
                        )
                    ),
                    run_time = 0.5
            )
        playing_cards = [PlayingCards(i, scale_factor=0.3) for i in range(30)]
        cards_target = VGroup(*[p.back.copy() for p in playing_cards]).arrange_in_grid(3, 10)
        self.wait()

        self.play(AnimationGroup(*[
            ReplacementTransform(p, p_t)
            for p, p_t in zip(cards, cards_target)
        ], lag_ratio=0.75), run_time = 1.5)
        self.wait()
    def shuffling_cards(self, cards):
        l = [i for i in range(30)]
        
        random.shuffle(l)
        huffled_cards_pos = [cards[i].get_center() for i in l]
        pointer = 0
        check_pointer = {}
        j = 0
        i = 0
        poser = []
        while(j <= 29):
            def shuffel(i):
                if i == 0:
                    check_pointer.add(pointer)
                    t = (pointer , l[pointer])
                    if l[pointer] in check_pointer:
                        pointer += 1
                    return t
                else:
                    check_pointer.add(shuffel(i-1)[1])
                    t = (shuffel(i-1)[1], l[shuffel(i-1)[1]])
                    if l[shuffel(i-1)[1]] in check_pointer:
                        pointer += 1
                    return t
            
            p = pointer
            poser.append(shuffel(i))

            i += 1
            j += 1
            if pointer - p > 0:
                i = 0
                    
                

        animation = [cards[i].move_to(huffled_cards_pos[i]) ]
        


class TestScene(Scene):
    def construct(self):
        c = PlayingCards(10)
        card = c.front.copy()
        two = MathTex("2^{10}")
        self.add(card)
        self.wait()
        self.play(TransformMatchingShapes(card, two))
        self.wait()

class PowersofB(Scene):
    def construct(self):
        scale_factor = 0.24
        cards_list = [PlayingCards(i, scale_factor=scale_factor) for i in range(30)]
        cards = VGroup(*[card.back for card in cards_list])
        cards.arrange_in_grid(6, 5, (0.35, 0.18))
        cards.to_corner(LEFT, buff=0.35)

        
        self.play(AnimationGroup(
            *[UpdateFromAlphaFunc(cards[i], cards_list[i].rotate_back_front(cards[i]))  for i in range(30)],
            lag_ratio = 0.3
        ), run_time = 2)
        self.wait(2)

        boxes = VGroup(*[
            StartingWith(k+1).scale(0.8) for k in range(9)
        ])
        powers_of_two = VGroup(*[n_power_of_a(2, n, 25) for n in range(30)]).move_to([0, -20, 0])

        boxes.arrange_in_grid(3, 3, (0.2, 0.2), flow_order="rd")
        boxes.move_to([3, 0, 0])
        self.play(FadeIn(boxes))
        self.wait()
        
        self.play(
            AnimationGroup(
                *[
                    ReplacementTransform(c, p[:2].next_to(boxes[p.first_digit - 1].next_p(), DOWN, buff=0))
                    for c, p in zip(cards, powers_of_two)
                ], lag_ratio = 0.7
            ), run_time = 8
        )

        ###
        len_list = [len(if_first_digit_is(powers_of_two, k+1)) for k in range(9)]
        count = VGroup()
        for i in range(9):
            count.add(
                MathTex(r"{:,}".format(int(len_list[i]))).scale(2)
                .move_to(boxes[i].position[4]).set_color(HOT_COLORS[i])
            )
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        FadeOut(if_first_digit_is(powers_of_two, i+1), rate_func = lambda x: x**(1/3)),
                        Write(count[i])
                    )
                    for i in range(9)
                ],
                lag_ratio=0.5
            )
        )

        def prob_formula(n):
            text_1 = r"\text{leading digit}: "
            text_2 = "{:,}".format(int(n))
            text_3 = "{:,}".format(int(len_list[n-1]))
            formula = MathTex(
                r"P(",
                text_1 + text_2,
                r") =",
                r"\frac{" + text_3+ r"}{30}"
            )               
            formula[1].set_color(HOT_COLORS[n-1])
            formula[3][0].set_color(HOT_COLORS[n-1])
            formula[3][2:].set_color(HOT_COLORS)
            return formula.scale(0.9)
        formula_summ = MathTex(
                "9+6+3+3+3+3+0+3+0=", "30"
            ).scale(0.7)
        for i in range(0, 17, 2):
            formula_summ[0][i].set_color(HOT_COLORS[int(i/2)])
        formula_summ[1].set_color(HOT_COLORS)
        formula_summ.to_edge(UL)
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(
                        ReplacementTransform(count[i].copy(), formula_summ[0][2*i]),
                        Write(formula_summ[0][2*i+1]),
                        lag_ratio=0.8
                    )
                    for i in range(9)
                ],
                Write(formula_summ[1]),
                lag_ratio=0.5
            ), run_time = 2.5
        )
        self.wait()
        self.play(FadeOut(formula_summ))
        formulas = VGroup(*[prob_formula(i+1).to_edge(UL) for i in range(9)])
        self.play(Write(formulas[0]))
        self.wait(2)
        for i in range(8):
            self.play(ReplacementTransform(formulas[i], formulas[i+1]), run_time=1/((i+1)**(1/2)))
            self.wait(0.5/((i+1)**(1/3)))   
           

        self.wait(0)

        dist = Distribution(2, 30).move_to([-3.75, -0.5, 0]).scale(1.05).align_to(boxes, DOWN)
        [dist.bars[i].set_color(HOT_COLORS[i]) for i in range(9)]

        self.play(Write(dist))
        self.wait(2)
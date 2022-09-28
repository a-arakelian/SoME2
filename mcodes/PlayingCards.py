import math
from telnetlib import DO
from manim import *

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
                l = abs(math.cos(alpha*PI))*width
                return l
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
            number_v.scale_to_fit_width(rec.width)

        starting_number.next_to(number_v, UP) #.shift((starting_number.width+0.05)/2*RIGHT)
        starting_number_r = starting_number.copy().rotate(180*DEGREES).next_to(number_v, DOWN) #.shift((starting_number.width+0.05)/2*LEFT)
      
        
        r_rec.set_stroke(color=WHITE)
        r_rec.set_fill(color= HOT_COLORS[starting_n-1], opacity=1)

        m_rec.set_stroke(color=HOT_COLORS[starting_n-1])
        m_rec.set_fill(color= GRAY_E, opacity=1)

        return VGroup(
            r_rec,                                      #0
            m_rec,                                      #1
            VGroup(number, number_r),                   #2
            VGroup(starting_number, starting_number_r), #3
            number_v                                    #4
        ).scale(scale_factor)

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


class PlayingCardsScene(MovingCameraScene):
    def construct(self):
        pc = PlayingCards(15, 1)
        card = pc.back
        card.to_corner(RIGHT, buff=1)
        self.add(card)
        self.play(UpdateFromAlphaFunc(card, pc.rotate_back_front(card)), run_time = 1.5)
        self.wait()
        front = pc.front.to_corner(RIGHT, buff=1)
        self.add(front)
        self.remove(card)
        self.play(Indicate(front[2][0]), Indicate(front[2][1]), run_time = 1.5)
        self.wait()
        self.play(Indicate(front[4]), run_time = 1.5)
        self.wait()
        self.play(Indicate(front[3]), Circumscribe(front[4][0][0]))
        self.wait()
        self.play(UpdateFromAlphaFunc(front, pc.rotate_front_back(front)))
        self.wait()
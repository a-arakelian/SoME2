import math
from colour import Color
import numpy as np
from manim import *

def fraction(a):
    a = float(a)
    return a%1

class WhatIsProb(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=2,
            zoomed_display_width=2,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame
        zoomed_display_frame.set_color(GRAY)
        zoomed_display.shift(2*DOWN)
        
        radius = 8/PI
        simple_arc_length = ValueTracker(2/9)
        
        simple_circle = self.fractioncircle(0, 0.001, radius)
        simple_arc = Arc(radius, angle = simple_arc_length.get_value() * 2* PI)
        #simple_arc_l_1 = Line(simple_circle.circle_center.get_center(), simple_arc.point_from_proportion(0), stroke_width = 0.2*DEFAULT_STROKE_WIDTH)
        #simple_arc_l_2 = Line(simple_circle.circle_center.get_center(), simple_arc.point_from_proportion(1), stroke_width = 0.2*DEFAULT_STROKE_WIDTH)

        def moving_arc_label(arc_):
            def moving_arc_label(mob):
                circle_center = simple_circle.circle_center.get_center()
                arc_center = arc_.point_from_proportion(0.5)
                shift_vector = (0.6/radius) * (arc_center - circle_center)
                mob.move_to(arc_center)
                mob.shift(shift_vector)
            return moving_arc_label
        arc_label = MathTex(r'\frac{2}{9}').scale(0.8)
        arc_label.add_updater(moving_arc_label(simple_arc))
        self.add(simple_circle)
        self.wait()
        dots = [Dot().add(MathTex("{:,}".format(i+1)).scale(0.2).set_color(BLACK)).move_to(simple_circle.circle.point_at_angle(4/9 *i*PI)) for i in range(9)]
        self.play(FadeIn(dots[0]), Flash(dots[0]))
        self.play(Create(simple_arc))
        self.play(FadeIn(arc_label))
        for i in range(1, 9):
            self.play(FadeIn(dots[i]), Flash(dots[i]))
            self.play(Rotating(simple_arc, radians=4/9*PI, about_point=simple_circle.circle_center.get_center()), run_time = 1/3)
        self.wait()
        poligon = Polygon(*[d.get_center() for d in dots], stroke_width = 0.2*DEFAULT_STROKE_WIDTH)
        #self.play(Rotating(simple_arc, radians=2/5*PI, about_point=simple_circle.circle_center.get_center()), run_time = 1/5)
        #self.play()
        self.play(Create(poligon, rate_func = linear), run_time = 3)
        arc_general_label = MathTex(r"\frac{a}{b}").scale(0.8).move_to(arc_label)
        self.wait()
        self.play(TransformMatchingTex(arc_label, arc_general_label))
        
        #self.activate_zooming()
        self.wait()
        self.play(Uncreate(poligon), FadeOut(*dots, simple_arc, arc_general_label))

        log_arc = Arc(radius, angle = math.log10(2) * 2* PI)
        log_arc_label = MathTex(r"\log", r"_{10}", r"2").scale(0.8)
        log_arc_label[2].set_color(BLUE)
        log_arc_label[1].set_color(RED)
        log_arc_label.add_updater(moving_arc_label(log_arc))
        log_dots = [
            Dot().add(
                MathTex("{:,}".format(i+1)).scale(0.2).set_color(RED)
                .set_color(BLACK)).move_to(simple_circle.circle.point_at_angle(math.log10(2) * 2 *i*PI)
            ).scale(0.5)  for i in range(200)
        ]
        self.play(Flash(dots[0]), FadeIn(log_dots[0]))
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)
        frame.move_to(simple_circle.circle.point_at_angle(0))
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))
        self.play(Create(frame))
        self.activate_zooming()
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
        frame.add_updater(lambda mob: mob.move_to(log_arc.point_from_proportion(1)))
        self.play(Create(log_arc), FadeIn(log_arc_label))
        for i in range(1, 50):
            self.play(FadeIn(log_dots[i]), Flash(log_dots[i]))
            self.play(Rotating(log_arc, radians=math.log10(2) * 2*PI, about_point=simple_circle.circle_center.get_center()), run_time = 1/3)
        frame.clear_updaters()
        self.play(FadeOut(log_arc, log_arc_label))
        self.play(
            AnimationGroup(frame.animate.move_to(log_dots[-1]), FadeIn(*log_dots[50:]), lag_ratio=0.5)
        )
        self.wait()
        self.play(log_dots[-1].animate(rate_func = rate_functions.there_and_back).scale(1.5))
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        
        self.wait()

        left_s = 2.5*LEFT
        arc_length = ValueTracker(0.001)
        arc_starting = ValueTracker(0.3)
        self.play(VGroup(simple_circle, *log_dots).animate.shift(left_s))
        def my_good_arc():
            arc = Arc(radius, 2*PI*fraction(arc_starting.get_value()), 2*PI*arc_length.get_value()).shift(left_s).set_stroke(opacity=0.5)
            simple_arc_l_1 = Line(simple_circle.circle_center.get_center(), arc.point_from_proportion(0), stroke_width = 0.2*DEFAULT_STROKE_WIDTH)
            simple_arc_l_2 = Line(simple_circle.circle_center.get_center(), arc.point_from_proportion(1), stroke_width = 0.2*DEFAULT_STROKE_WIDTH)
            arc_label = MathTex("{:.2f}".format(arc_length.get_value())).scale(0.8)
            moving_arc_label(arc)(arc_label)
            arc.set_color(BLUE)
            return VGroup(arc, simple_arc_l_1, simple_arc_l_2, arc_label)
        
        
        
            

        l_arc = always_redraw(my_good_arc)
        def if_dot_on_arc(mob):
            start = l_arc[0].point_from_proportion(0) - simple_circle.circle_center.get_center()
            mob_vector = mob.get_center() - simple_circle.circle_center.get_center()
            my_or = np.sign((np.cross(start, mob_vector) @ np.array([0, 0, 1])))
            angle_s = np.arccos(((start @ mob_vector) / ((start@start)**(1/2) * (start@start)**(1/2)))) * my_or
            if angle_s < 0:
                angle_s += 2*PI
            angle = 2*PI*arc_length.get_value()
            if angle_s <= angle:
                mob[0].set_color(PINK)
            else:
                mob[0].set_color(WHITE)

        self.play(Create(l_arc[:3]), FadeIn(l_arc[-1]))
        self.add(l_arc)
        for d in log_dots:
            d.add_updater(if_dot_on_arc)
        self.play(arc_length.animate.set_value(0.25), arc_starting.animate.set_value(0.125))
        self.wait()
        tali = Tex(r"The arc length is").scale(0.7) #
        tnopi = Tex(r"Total number of points is $200$").scale(0.7).to_corner(DL)
        tnopota = Tex(r"The number of points  on the arc is").scale(0.7)#
        fract_text = MathTex(r"\frac{\text{The number of points  on the arc}}{\text{Total number of points}} = ").scale(0.5)#
        VGroup(tali, tnopota, fract_text).arrange(DOWN, aligned_edge=LEFT).next_to(simple_circle)
        tnopota.next_to(tnopi).shift(2*RIGHT)
       

        def count_pink():
            i = 0
            for p in log_dots:
                if p.color == Color(PINK):
                    i += 1
            arc_label = MathTex("{:.2f}".format(arc_length.get_value())).scale(0.7).next_to(tali)
            a = MathTex("{:,}".format(i)).scale(0.7).next_to(tnopota)
            b = MathTex("{:.3f}".format(i/200)).scale(0.7).next_to(fract_text)
            return VGroup(a, b, arc_label)
        
        cp = always_redraw(count_pink)

        self.play(Write(VGroup(tnopi, tali, tnopota, fract_text, cp,)))
        self.play(arc_starting.animate.set_value(0.5))
        self.play(arc_starting.animate.set_value(0.75), arc_length.animate.set_value(0.05))
        self.wait()
        self.play(arc_starting.animate.set_value(1), run_time = 2.5)
        self.wait()
        self.play(arc_starting.animate.set_value(1.75), arc_length.animate.set_value(0.05), run_time = 9)
        self.wait()

        #The arc length is 20
        #Total number of points is 200
        #The number of points  on the arc is
    
    def fractioncircle(self, a, da, r = 1):
        arc_angle = 2*PI if da >= 1 else da * (2 * PI)
        start_angle = (2 * PI) * fraction(a) - (arc_angle / 2)
        circle = Circle(radius=r)
        center = VectorizedPoint()
        trip = Line(0.25*LEFT, ORIGIN, stroke_width = 0.25*DEFAULT_STROKE_WIDTH)
        trip.move_to(circle.point_at_angle(0))
        circle.add(trip, center)
        arc = Arc(radius=r, start_angle=start_angle, angle=arc_angle)
        frac = VGroup(circle, arc)
        frac.arc = frac[1]
        frac.circle_center = frac[0][2]
        frac.circle = frac[0]

        return frac

class IsIrational(Scene):
    def construct(self):
        log_2_is_r = MathTex(r"\log", r"_{10}", r"2", r"=", r"\frac{a}{b}").shift(2*UP)
        log_2_is_r[1].set_color(RED)
        log_2_is_r[2].set_color(BLUE)
        log_2_is_r[-1][0].set_color(GREEN)
        log_2_is_r[-1][2].set_color(PINK)

        log_2_is_r_10 = MathTex(r"10", r"^{\log_{10}2}", "=", r"10", r"^{\frac{a}{b}}").shift(0.75*UP)
        log_2_is_r_10[0].set_color(RED)
        log_2_is_r_10[3].set_color(RED)
        log_2_is_r_10[1][3:5].set_color(RED)
        log_2_is_r_10[1][-1].set_color(BLUE)
        log_2_is_r_10[-1][0].set_color(GREEN)
        log_2_is_r_10[-1][2].set_color(PINK)

        log_2_is = MathTex(r"2", "=", r"10", r"^{\frac{a}{b}}").shift(0.75*UP)
        log_2_is[0].set_color(BLUE)
        log_2_is[2].set_color(RED)
        log_2_is[-1][0].set_color(GREEN)
        log_2_is[-1][2].set_color(PINK)

        log_2_is_2_5 = MathTex(r"2", "=", r"(2 \cdot 5)", r"^{\frac{a}{b}}").shift(0.75*UP)
        log_2_is_2_5[0].set_color(BLUE)
        log_2_is_2_5[2][3].set_color(RED)
        log_2_is_2_5[2][1].set_color(BLUE)          
        log_2_is_2_5[-1][0].set_color(GREEN)
        log_2_is_2_5[-1][2].set_color(PINK)

        _2_is_2_5 = MathTex(r"2", "=", r"2", r"^{\frac{a}{b}} \cdot", r"5", r"^{\frac{a}{b}}").shift(0.75*UP)
        _2_is_2_5[0].set_color(BLUE)
        _2_is_2_5[2].set_color(BLUE)
        _2_is_2_5[4].set_color(RED)          
        _2_is_2_5[-1][0].set_color(GREEN)
        _2_is_2_5[-1][2].set_color(PINK)
        _2_is_2_5[3][0].set_color(GREEN)
        _2_is_2_5[3][2].set_color(PINK)

        _is_2_5 = MathTex(r"2", r"^{1-\frac{a}{b}}", "=", r"5", r"^{\frac{a}{b}}").shift(0.75*UP)
        _is_2_5[0].set_color(BLUE)
        _is_2_5[1][2].set_color(GREEN)
        _is_2_5[1][4].set_color(PINK)
        _is_2_5[3].set_color(RED)          
        _is_2_5[-1][0].set_color(GREEN)
        _is_2_5[-1][2].set_color(PINK)

        is_2_5 = MathTex(r"2", r"^{\frac{b - a}{b}}", "=", r"5", r"^{\frac{a}{b}}").shift(0.75*UP)
        is_2_5[0].set_color(BLUE)
        is_2_5[1][0].set_color(PINK)
        is_2_5[1][2].set_color(GREEN)
        is_2_5[1][4].set_color(PINK)
        is_2_5[3].set_color(RED)          
        is_2_5[-1][0].set_color(GREEN)
        is_2_5[-1][2].set_color(PINK)

        _2_5 = MathTex(r"2", r"^{b - a}", "=", r"5", r"^a").shift(0.75*UP)
        _2_5[0].set_color(BLUE)
        _2_5[1][0].set_color(PINK)
        _2_5[1][2].set_color(GREEN)
        _2_5[3].set_color(RED)          
        _2_5[-1].set_color(GREEN)

        rec =  SurroundingRectangle(VGroup(log_2_is_r, log_2_is_r_10, _2_is_2_5, log_2_is, _is_2_5, log_2_is_2_5, log_2_is_2_5, _is_2_5, is_2_5, _2_5).shift(3.5*LEFT).scale(1.3), color=DARKER_GRAY).set_opacity(0.8)
        VGroup(log_2_is_r, log_2_is_r_10, _2_is_2_5, log_2_is, _is_2_5, log_2_is_2_5, log_2_is_2_5, _is_2_5, is_2_5, _2_5, rec).to_corner().to_edge(LEFT)
        self.play(FadeIn(rec, log_2_is_r))
        self.wait()
        self.play(TransformMatchingShapes(log_2_is_r.copy(), log_2_is_r_10))
        self.wait()
        self.play(
            TransformMatchingShapes(log_2_is_r_10[:4], log_2_is[0]),
            TransformMatchingShapes(log_2_is_r_10[4:], log_2_is[1:])
        )
        self.wait()
        self.play(
            TransformMatchingShapes(log_2_is[0], log_2_is_2_5[0]),
            TransformMatchingShapes(log_2_is[1:], log_2_is_2_5[1:])
        )
        self.wait(0.5)
        self.play(TransformMatchingShapes(log_2_is_2_5, _2_is_2_5))
        self.wait(0.5)
        self.play(TransformMatchingShapes(_2_is_2_5, _is_2_5))
        self.wait(1.5)
        self.play(
            TransformMatchingShapes(_is_2_5[:4], is_2_5[:4]),
            TransformMatchingShapes(_is_2_5[4:], is_2_5[4:])
        )
        self.wait()
        self.play(TransformMatchingShapes(is_2_5, _2_5))
        self.wait()
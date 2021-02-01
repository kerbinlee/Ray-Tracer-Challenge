import numpy as np
import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from color import Color
from pattern import *
from transformations import Transformations
from tuple import *
from sphere import Sphere

class TestPattern(unittest.TestCase):
    black = Color(0, 0, 0)
    white = Color(1, 1, 1)

    # Scenario: Creating a stripe pattern
    def test_striped_pattern(self):
        pattern = Stripe(TestPattern.white, TestPattern.black)
        self.assertEqual(pattern.a, TestPattern.white)
        self.assertEqual(pattern.b, TestPattern.black)

    # Scenario: A stripe pattern is constant in y
    def test_striped_pattern_constant_y(self):
        pattern = Stripe(TestPattern.white, TestPattern.black)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 1, 0)), TestPattern.white)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 2, 0)), TestPattern.white)

    # Scenario: A stripe pattern is constant in z
    def test_striped_pattern_constant_z(self):
        pattern = Stripe(TestPattern.white, TestPattern.black)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 0, 1)), TestPattern.white)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 0, 2)), TestPattern.white)

    # Scenario: A stripe pattern alternates in x
    def test_striped_pattern_alternate_x(self):
        pattern = Stripe(TestPattern.white, TestPattern.black)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(Stripe.stripe_at(pattern, Point(0.9, 0, 0)), TestPattern.white)
        self.assertEqual(Stripe.stripe_at(pattern, Point(1, 0, 0)), TestPattern.black)
        self.assertEqual(Stripe.stripe_at(pattern, Point(-0.1, 0, 0)), TestPattern.black)
        self.assertEqual(Stripe.stripe_at(pattern, Point(-1, 0, 0)), TestPattern.black)
        self.assertEqual(Stripe.stripe_at(pattern, Point(-1.1, 0, 0)), TestPattern.white)

    # # Scenario: Stripes with an object transformation
    # def test_stripes_object_transformation(self):
    #     object = Sphere()
    #     object.transform = Transformations.scaling(2, 2, 2)
    #     pattern = Pattern.stripe_pattern(TestPattern.white, TestPattern.black)
    #     c = Pattern.stripe_at_object(pattern, object, Point(1.5, 0, 0))
    #     self.assertEqual(c, TestPattern.white)

    # # Scenario: Stripes with a pattern transformation
    # def test_stripes_pattern_transfromation(self):
    #     object = Sphere()
    #     pattern = Pattern.stripe_pattern(TestPattern.white, TestPattern.black)
    #     pattern.transform = Transformations.scaling(2, 2, 2)
    #     c = Pattern.stripe_at_object(pattern, object, Point(1.5, 0, 0))
    #     self.assertEqual(c, TestPattern.white)

    # # Scenario: Stripes with both an object and a pattern transformation
    # def test_stripes_object_and_pattern_transformation(self):
    #     object = Sphere()
    #     object.transform = Transformations.scaling(2, 2, 2)
    #     pattern = Pattern.stripe_pattern(TestPattern.white, TestPattern.black)
    #     pattern.transform = Transformations.translation(0.5, 0, 0)
    #     c = Pattern.stripe_at_object(pattern, object, Point(2.5, 0, 0))
    #     self.assertEqual(c, TestPattern.white)

    # Scenario: The default pattern transformation
    def test_default_pattern_transformation(self):
        pattern = Pattern.test_pattern()
        self.assertTrue(np.array_equal(pattern.transform, np.identity(4)))

    # Scenario: Assigning a transformation
    def test_assign_transformation(self):
        pattern = Pattern.test_pattern()
        pattern.transform = Transformations.translation(1, 2, 3)
        self.assertTrue(np.array_equal(pattern.transform, Transformations.translation(1, 2, 3)))

    # Scenario: A pattern with an object transformation
    def test_pattern_object_transformation(self):
        shape = Sphere()
        shape.transform = Transformations.scaling(2, 2, 2)
        pattern = Pattern.test_pattern()
        c = pattern.pattern_at_shape(shape, Point(2, 3, 4))
        self.assertEqual(c, Color(1, 1.5, 2))

    # Scenario: A pattern with a pattern transformation
    def test_pattern_transformation(self):
        shape = Sphere()
        pattern = Pattern.test_pattern()
        pattern.transform = Transformations.scaling(2, 2, 2)
        c = pattern.pattern_at_shape(shape, Point(2, 3, 4))
        self.assertEqual(c, Color(1, 1.5, 2))

    # Scenario: A pattern with both an object and a pattern transformation
    def test_pattern_object_and_pattern_transformation(self):
        shape = Sphere()
        shape.transform = Transformations.scaling(2, 2, 2)
        pattern = Pattern.test_pattern()
        pattern.transform = Transformations.translation(0.5, 1, 1.5)
        c = pattern.pattern_at_shape(shape, Point(2.5, 3, 3.5))
        self.assertEqual(c, Color(0.75, 0.5, 0.25))

    # Scenario: A gradient linearly interpolates between colors
    def test_gradient_linear_interpolate(self):
        pattern = Gradient(TestPattern.white, TestPattern.black)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(0.25, 0, 0)), Color(0.75, 0.75, 0.75))
        self.assertEqual(pattern.pattern_at(Point(0.5, 0, 0)), Color(0.5, 0.5, 0.5))
        self.assertEqual(pattern.pattern_at(Point(0.75, 0, 0)), Color(0.25, 0.25, 0.25))

    # Scenario: A ring should extend in both x and z
    def test_ring_extend_x_z(self):
        pattern = Ring(TestPattern.white, TestPattern.black)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(1, 0, 0)), TestPattern.black)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 1)), TestPattern.black)
        # 0.708 = just slightly more than √2/2
        self.assertEqual(pattern.pattern_at(Point(0.708, 0, 0.708)), TestPattern.black)

    # Scenario: Checkers should repeat in x
    def test_checkers_repeat_x(self):
        pattern = Checkers(TestPattern.white, TestPattern.black)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(0.99, 0, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(1.01, 0, 0)), TestPattern.black)

    # Scenario: Checkers should repeat in y
    def test_checkers_repeat_y(self):
        pattern = Checkers(TestPattern.white, TestPattern.black)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(0, 0.99, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(0, 1.01, 0)), TestPattern.black)

    # Scenario: Checkers should repeat in z
    def test_checkers_repeat_z(self):
        pattern = Checkers(TestPattern.white, TestPattern.black)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 0.99)), TestPattern.white)
        self.assertEqual(pattern.pattern_at(Point(0, 0, 1.01)), TestPattern.black)

if __name__ == '__main__':
    unittest.main()
    
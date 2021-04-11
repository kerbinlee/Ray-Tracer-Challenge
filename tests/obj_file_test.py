import os, sys
import unittest

sys.path.append(os.path.abspath('..'))
from obj_file import ObjFile
from tuple import *

class TestObjFile(unittest.TestCase):
    # Scenario: Ignoring unrecognized lines
    def test_ignoring_unrecognized_lines(self):
        # Given gibberish = a file containing:
        #     """
        #     There was a young lady named Bright
        #     who traveled much faster than light.
        #     She set out one day
        #     in a relative way,
        #     and came back the previous night.
        #     """
        parser = ObjFile.parse_obj_file("tests/obj_test_files/gibberish.obj")
        self.assertEqual(parser.ignored_lines, 5)

    # Scenario: Vertex records
    def test_vertex_records(self):
    # Given file = a file containing:
    #     """
    #     v -1 1 0
    #     v -1.0000 0.5000 0.0000
    #     v 1 0 0
    #     v 1 1 0
    #     """
        parser = ObjFile.parse_obj_file("tests/obj_test_files/vertex.obj")
        self.assertEqual(parser.vertices[1], Point(-1, 1, 0))
        self.assertEqual(parser.vertices[2], Point(-1, 0.5, 0))
        self.assertEqual(parser.vertices[3], Point(1, 0, 0))
        self.assertEqual(parser.vertices[4], Point(1, 1, 0))

    # Scenario: Parsing triangle faces
    # Given file = a file containing:
    #     """
    #     v -1 1 0
    #     v -1 0 0
    #     v 1 0 0
    #     v 1 1 0

    #     f 1 2 3
    #     f 1 3 4
    #     """
    def test_parsing_trangle_faces(self):
        parser = ObjFile.parse_obj_file("tests/obj_test_files/triangle_faces.obj")
        g = parser.default_group
        t1 = g.members[0]
        t2 = g.members[1]
        self.assertEqual(t1.p1, parser.vertices[1])
        self.assertEqual(t1.p2, parser.vertices[2])
        self.assertEqual(t1.p3, parser.vertices[3])
        self.assertEqual(t2.p1, parser.vertices[1])
        self.assertEqual(t2.p2, parser.vertices[3])
        self.assertEqual(t2.p3, parser.vertices[4])

    # Scenario: Triangulating polygons
    # Given file = a file containing:
    #     """
    #     v -1 1 0
    #     v -1 0 0
    #     v 1 0 0
    #     v 1 1 0
    #     v 0 2 0

    #     f 1 2 3 4 5
    #     """
    def test_triangulating_polygons(self):
        parser = ObjFile.parse_obj_file("tests/obj_test_files/triangulating_polygons.obj")
        g = parser.default_group
        t1 = g.members[0]
        t2 = g.members[1]
        t3 = g.members[2]
        self.assertEqual(t1.p1, parser.vertices[1])
        self.assertEqual(t1.p2, parser.vertices[2])
        self.assertEqual(t1.p3, parser.vertices[3])
        self.assertEqual(t2.p1, parser.vertices[1])
        self.assertEqual(t2.p2, parser.vertices[3])
        self.assertEqual(t2.p3, parser.vertices[4])
        self.assertEqual(t3.p1, parser.vertices[1])
        self.assertEqual(t3.p2, parser.vertices[4])
        self.assertEqual(t3.p3, parser.vertices[5])

    # Scenario: Triangles in groups
    def test_triangles_in_groups(self):
        parser = ObjFile.parse_obj_file("tests/obj_test_files/triangles.obj")
        g1 = parser.named_groups["FirstGroup"]
        g2 = parser.named_groups["SecondGroup"]
        t1 = g1.members[0]
        t2 = g2.members[0]
        self.assertEqual(t1.p1, parser.vertices[1])
        self.assertEqual(t1.p2, parser.vertices[2])
        self.assertEqual(t1.p3, parser.vertices[3])
        self.assertEqual(t2.p1, parser.vertices[1])
        self.assertEqual(t2.p2, parser.vertices[3])
        self.assertEqual(t2.p3, parser.vertices[4])

    # Scenario: Converting an OBJ file to a group
    def test_converting_obj_file_to_group(self):
        parser = ObjFile.parse_obj_file("tests/obj_test_files/triangles.obj")
        g = ObjFile.obj_to_group(parser)
        self.assertIn(parser.named_groups["FirstGroup"], g.members)
        self.assertIn(parser.named_groups["SecondGroup"], g.members)

    # # Scenario: Vertex normal records
    # Given file = a file containing:
    #     """
    #     vn 0 0 1
    #     vn 0.707 0 -0.707
    #     vn 1 2 3
    #     """
    def test_vertex_normal_records(self):
        parser = ObjFile.parse_obj_file("tests/obj_test_files/vertex_normal.obj")
        self.assertEqual(parser.normals[1], Vector(0, 0, 1))
        self.assertEqual(parser.normals[2], Vector(0.707, 0, -0.707))
        self.assertEqual(parser.normals[3], Vector(1, 2, 3))

    # # Scenario: Faces with normals
    # Given file = a file containing:
    #     """
    #     v 0 1 0
    #     v -1 0 0
    #     v 1 0 0

    #     vn -1 0 0
    #     vn 1 0 0
    #     vn 0 1 0

    #     f 1//3 2//1 3//2
    #     f 1/0/3 2/102/1 3/14/2
    #     """
    def test_faces_normals(self):
        parser = ObjFile.parse_obj_file("tests/obj_test_files/faces_normals.obj")
        g = parser.default_group
        t1 = g.members[0]
        t2 = g.members[1]
        self.assertEqual(t1.p1, parser.vertices[1])
        self.assertEqual(t1.p2, parser.vertices[2])
        self.assertEqual(t1.p3, parser.vertices[3])
        self.assertEqual(t1.n1, parser.normals[3])
        self.assertEqual(t1.n2, parser.normals[1])
        self.assertEqual(t1.n3, parser.normals[2])
        self.assertEqual(t2, t1)

if __name__ == '__main__':
    unittest.main()

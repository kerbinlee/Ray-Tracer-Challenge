from smooth_triangle import SmoothTriangle
from group import Group
from tuple import Point, Vector
from typing import Iterable

class ObjFile:
    def __init__(self):
        self.ignored_lines: int = 0
        self.vertices: Iterable[Point] = [None]
        self.default_group: Group = Group()
        self.named_groups = {}
        self.normals: Iterable[Vector] = [None]

    def parse_obj_file(filepath: str) -> int:
        objFile = ObjFile()
        with open(filepath, "r") as obj_file:
            group_name = None
            for line in obj_file:
                tokens = line.split()
                if len(tokens) == 4 and tokens[0] == 'v':
                    objFile.vertices.append(Point(float(tokens[1]), float(tokens[2]), float(tokens[3])))
                elif len(tokens) >= 4 and tokens[0] == 'f':
                    for triangle in ObjFile.fan_triangulation(objFile.vertices, objFile.normals, tokens):
                        if group_name:
                            objFile.named_groups[group_name].add_child(triangle)
                        else:
                            objFile.default_group.add_child(triangle)
                elif len(tokens) == 2 and tokens[0] == 'g':
                    group_name = tokens[1]
                    objFile.named_groups[group_name] = Group()
                elif len(tokens) == 4 and tokens[0] == "vn":
                    objFile.normals.append(Vector(float(tokens[1]), float(tokens[2]), float(tokens[3])))
                else:
                    objFile.ignored_lines += 1
        
        return objFile

    def fan_triangulation(vertices: Iterable[Point], vertex_normals: Iterable[Point], vertex_indices: Iterable[str]) -> Iterable:
        from triangle import Triangle

        triangles = []
        vertex_1_info = vertex_indices[1].split('/')
        for index in range(2, len(vertex_indices) - 1):
            if len(vertex_1_info) == 1:
                tri = Triangle(vertices[int(vertex_indices[1])], vertices[int(vertex_indices[index])], vertices[int(vertex_indices[index + 1])])
                triangles.append(tri)
            else:
                vertex_2_info = vertex_indices[index].split('/')
                vertex_3_info = vertex_indices[index + 1].split('/')
                tri = SmoothTriangle(vertices[int(vertex_1_info[0])], vertices[int(vertex_2_info[0])], vertices[int(vertex_3_info[0])], vertex_normals[int(vertex_1_info[2])], vertex_normals[int(vertex_2_info[2])], vertex_normals[int(vertex_3_info[2])])
                triangles.append(tri)

        return triangles

    def obj_to_group(parser: 'ObjFile') -> Group:
        group = Group()
        for _, named_group in parser.named_groups.items():
            group.add_child(named_group)

        return group

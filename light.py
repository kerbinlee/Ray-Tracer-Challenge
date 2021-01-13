from color import Color
from material import Material
from tuple import *

class PointLight:
    def __init__(self, position: Point, intensity: Color):
        self.position = position
        self.intensity = intensity

    def __eq__(self, other):
        return self.position == other.position and self.intensity == other.intensity

    def lighting(material: Material, light: 'PointLight', point: Point, eyev: Vector, normalv: Vector) -> Color:
        # combine the surface color with the light's color/intensity
        effective_color = material.color * light.intensity

        # find the direction to the light source
        lightv = Vector.normalize(light.position - point)

        # compute the ambient contribution
        ambient = effective_color * material.ambient

        # light_dot_normal represents the cosine of the angle between the
        # light vector and the normal vector. A negative number means the
        # light is on the other side of the surface.
        light_dot_normal = Vector.dot(lightv, normalv)
        if light_dot_normal < 0:
            diffuse = Color(0, 0, 0) # black
            specular = Color(0, 0, 0) # black
        else:
            # compute the diffuse contribution
            diffuse = effective_color * material.diffuse * light_dot_normal

            # reflect_dot_eye represents the cosine of the angle between the
            # reflection vector and the eye vector. A negative number means the
            # light reflects away from the eye.
            reflectv = Vector.reflect(-lightv, normalv)
            reflect_dot_eye = Vector.dot(reflectv, eyev)

            if reflect_dot_eye <= 0:
                specular = Color(0, 0, 0) # black
            else:
                # compute the specular contribution
                factor = math.pow(reflect_dot_eye, material.shininess)
                specular = light.intensity * material.specular * factor

        # Add the three contributions together to get the final shading
        return ambient + diffuse + specular
    
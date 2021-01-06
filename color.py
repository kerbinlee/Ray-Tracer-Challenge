from tuple import Tuple

class Color(Tuple):
    def __init__(self, red, green, blue):
        super().__init__(red, green, blue, 0)

    @property
    def red(self):
        return self.x

    @property
    def green(self):
        return self.y

    @property
    def blue(self):
        return self.z

    def __add__(self, other):
        return Color(self.red + other.red, self.green + other.green, self.blue + other.blue)

    def __sub__(self, other):
        return Color(self.red - other.red, self.green - other.green, self.blue - other.blue)

    def __mul__(self, other):
        # hadamard_product
        # https://stackoverflow.com/questions/4233628/override-mul-from-a-child-class-using-parent-implementation-leads-to-proble/4233800#4233800
        if isinstance(other, Color):
            return Color(self.red * other.red, self.green * other.green, self.blue * other.blue)
        else:
            return Color(self.red * other, self.green * other, self.blue * other)

    def clamp_ppm_pixel(self, pixel):
        if pixel < 0:
            return 0
        elif pixel > 255:
            return 255
        else:
            return pixel

    def scale_ppm_pixel(self, pixel):
        return self.clamp_ppm_pixel(round(pixel * 255))

    def ppm_str(self):
        return f"{self.scale_ppm_pixel(self.red)} {self.scale_ppm_pixel(self.green)} {self.scale_ppm_pixel(self.blue)}"
        
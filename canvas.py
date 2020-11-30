from color import Color

class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[Color(0, 0, 0) for _ in range(width)] for _ in range(height)] 

    def write_pixel(self, x, y, color):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return
        self.pixels[y][x] = color

    def pixel_at(self, x, y):
        return self.pixels[y][x]

    def canvas_to_ppm(self):
        with open("canvas.ppm", "w") as ppm_file: 
            ppm_header = ["P3\n", f"{self.width} {self.height}\n", "255\n"]
            ppm_file.writelines(ppm_header)
            for y in range(self.height):
                line = ""
                for x in range(self.width):
                    if line != "":
                        line += " " + self.pixel_at(x, y).ppm_str()
                    else:
                        line = self.pixel_at(x, y).ppm_str()
                # break into 70 character lines
                while True:
                    if len(line) is 0:
                        break
                    write_line = line[0:70]
                    # if 70 characters is within a color value, partition at last space before 70 characters
                    if len(write_line) is 70 and len(line) > 0 and write_line[69] != ' ' and line[0] != ' ':
                        write_line_partitions = write_line.rpartition(' ')
                        ppm_file.write(write_line_partitions[0] + "\n")
                        line = write_line_partitions[2] + line[70:]
                    else:
                        ppm_file.write(write_line + "\n")
                        line = line[70:]
            ppm_file.write("\n")

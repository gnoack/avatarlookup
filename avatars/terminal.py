import os
import subprocess


W3MIMGDISPLAY = "/usr/lib/w3m/w3mimgdisplay"


def draw_image(filename):
  if os.path.exists(filename):
    windowsize_str = subprocess.check_output((W3MIMGDISPLAY, "-test"))
    windowx, windowy = map(int, windowsize_str.split(b" "))

    # TODO: Coordinate calculation could be more flexible.
    w, h = 48, 48
    x = windowx - w - 8 * 2
    y = 0 + 16 * 2

    drawing = subprocess.Popen(W3MIMGDISPLAY, stdin=subprocess.PIPE)
    commands = "0;1;%s;%s;%s;%s;;;;;%s\n4;\n3;" % (x, y, w, h, filename)
    commands = bytes(commands, encoding="utf-8")
    drawing.stdin.write(commands)
    drawing.communicate()

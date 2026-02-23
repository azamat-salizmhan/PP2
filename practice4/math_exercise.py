# math.py

import math

degree = 15
radian = degree * (math.pi / 180)
print("Input degree:", degree)
print("Output radian:", round(radian, 6))

height = 5
base1 = 5
base2 = 6
area_trapezoid = ((base1 + base2) / 2) * height
print("Area of trapezoid:", area_trapezoid)

n = 4
side = 25
area_polygon = (n * side ** 2) / (4 * math.tan(math.pi / n))
print("The area of the polygon is:", int(area_polygon))

base = 5
height_para = 6
area_para = base * height_para
print("Area of parallelogram:", float(area_para))

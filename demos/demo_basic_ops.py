from meadow_map.basic_ops import *
import numpy as np
import matplotlib.pyplot as plt

# Sample test
a = np.array([0, 0], dtype=np.float64)
b = np.array([8, 4], dtype=np.float64)
c = np.array([0, 1], dtype=np.float64)
d = np.array([4, 2], dtype=np.float64)
e = np.array([4.2, 2.2], dtype=np.float64)

# Print All points
print("a: {}".format(a))
print("b: {}".format(b))
print("c: {}".format(c))
print("d: {}".format(d))
print()

print("c is left to ab?")
print(left(a, b, c))
print()

print("d is left ab?")
print(left(a, b, d))
print()

print("d is left or on ab?")
print(left_on(a, b, d))
print()

print("d is on ab?")
print(collinear(a, b, d))
print()

print("d is between ab?")
print(collinear(a, b, d) and between(a, b, d))
print()

print("b is between ad?")
print(collinear(a, d, b) and between(a, d, b))
print()

print("e is on ab?")
print(collinear(a, b, e))
print()

plt.plot([a[0], b[0]], [a[1], b[1]], label="ab")
plt.scatter([c[0]], [c[1]], label="c")
plt.scatter([d[0]], [d[1]], label="d")
plt.scatter([e[0]], [e[1]], label="e")

plt.legend()
plt.show()

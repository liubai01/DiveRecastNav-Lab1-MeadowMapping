from meadow_map.intersect import intersect
import numpy as np
import matplotlib.pyplot as plt


# Sample test
a1 = np.array([0.5, 0.5])
a2 = np.array([5.0, 5.0])

b1 = np.array([0.5, 4.0])
b2 = np.array([5.5, 2.0])

c1 = np.array([1.0, 0.5])
c2 = np.array([8.0, 5.0])

print("Intersection of a && b")
print(intersect(a1, a2, b1, b2))

print("Intersection of a && c")
print(intersect(a1, a2, c1, c2))

print("Intersection of b && c")
print(intersect(b1, b2, c1, c2))

# Visualize 2D-lines: <a1, a2>, <b1, b2>, <c1, c2>
plt.plot([a1[0], a2[0]], [a1[1], a2[1]], label="a")
plt.plot([b1[0], b2[0]], [b1[1], b2[1]], label="b")
plt.plot([c1[0], c2[0]], [c1[1], c2[1]], label="c")

plt.grid()
plt.legend()
plt.show()

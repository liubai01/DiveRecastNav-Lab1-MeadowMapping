from MeadowMap.ConvexifyNoHole import convexify, find_concave_vertex
import MeadowMap
import numpy as np
import matplotlib.pyplot as plt


# Sample test
verts_poly = np.array(
    [
        [0., 0.], [0., 4.], [2., 4.],
        [1., 3.], [2., 1.], [3., 3.], [4., 1.],
        [1., 0.]
    ]
)

indices_poly = [verts_poly.shape[0] - i - 1 for i in range(verts_poly.shape[0])]  # CCW

# draw the polygon
polys, diags = convexify(verts_poly, indices_poly)
MeadowMap.plot_poly(verts_poly, indices_poly)

# Plot diagonals that split original region in dotted line
for d in diags:
    pos_a = verts_poly[indices_poly[d[0]]]
    pos_b = verts_poly[indices_poly[d[1]]]
    plt.plot([pos_a[0], pos_b[0]], [pos_a[1], pos_b[1]], "--", c="blue")

itest = find_concave_vertex(verts_poly, indices_poly)

plt.grid()
plt.title("Convexify simple polygon (without hole)")
plt.show()



from meadow_map.convex_no_hole import convexify, find_concave_vertex
import meadow_map
import numpy as np
import matplotlib.pyplot as plt


def plot_poly(verts: np.ndarray, indices: np.ndarray, color="blue") -> None:
    """
    Plot the simple polygon.
    :param verts:      np.ndarray (#verts, 2)  a list of 2D-vertices position
    :param indices:    np.ndarray (#vert, )    a list of polygon vertex index (to array `verts`)
    :param color:      str                     color
    :return:
    """
    x = []
    y = []
    for i in indices:
        x.append(verts[i][0])
        y.append(verts[i][1])

    x.append(verts[indices[0]][0])
    y.append(verts[indices[0]][1])

    plt.plot(x, y, c=color)


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
plot_poly(verts_poly, indices_poly)

# Plot diagonals that split original region in dotted line
for d in diags:
    pos_a = verts_poly[indices_poly[d[0]]]
    pos_b = verts_poly[indices_poly[d[1]]]
    plt.plot([pos_a[0], pos_b[0]], [pos_a[1], pos_b[1]], "--", c="blue")

plt.grid()
plt.title("Convexify simple polygon (without hole)")
plt.show()



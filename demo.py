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


# The poly region that we want to divide into convex areas
verts_poly = np.array(
    [
        [0., 0.], [0., 4.], [2., 4.],
        [1., 3.], [2., 1.], [3., 3.], [4., 1.],
        [1., 0.]
    ]
)
indices_poly = [verts_poly.shape[0] - i - 1 for i in range(verts_poly.shape[0])]  # CCW

verts_hole = np.array(
    [
        [0.5, 0.5], [0.2, 1.5], [0.4, 2.],
        [1.8, 0.5]
    ]
)
indices_hole = [(i + 2) % 4 for i in range(verts_hole.shape[0])]  # CW

verts, indices, mergeLineSeg = meadow_map.merge_hole(verts_poly, indices_poly, verts_hole, indices_hole)
polys, diags = meadow_map.convexify(verts, indices)

# plot the result
plot_poly(verts_poly, indices_poly, [0, 0, 1.0])
plot_poly(verts_hole, indices_hole, [0.0, 0.0, 0.0])

# plot all diags. with dotted line
for d in diags:
    posA = verts[indices[d[0]]]
    posB = verts[indices[d[1]]]
    plt.plot([posA[0], posB[0]], [posA[1], posB[1]], "--", c=[0.4, 0.4, 0.8])
# plot the line segment that merge the hole
plt.plot(
    [verts[mergeLineSeg[0]][0], verts[mergeLineSeg[1]][0]],
    [verts[mergeLineSeg[0]][1], verts[mergeLineSeg[1]][1]],
    "--", c=[0.9, 0.4, 0.8]
)

plt.grid()
plt.title("Convexify with holes")
plt.show()

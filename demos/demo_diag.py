import numpy as np
from meadow_map.diag import diagonalie, in_cone
import matplotlib.pyplot as plt
from meadow_map.utils import plot_poly

# Sample test
verts_poly = np.array(
    [
        [0., 0.], [0., 4.], [2., 4.],
        [1., 3.], [2., 1.], [3., 3.], [4., 1.],
        [1., 0.]
    ][::-1]
)
indices_poly = [verts_poly.shape[0] - i - 1 for i in range(verts_poly.shape[0])]  # CCW

# Visualize 4 diagonal status
plt_ids = [221, 222, 223, 224]
dias = [0, 2, 4, 6]
dibs = [2, 4, 6, 2]

for pid, dia, dib in zip(plt_ids, dias, dibs):
    diag = diagonalie(verts_poly, indices_poly, dia, dib)
    lbl = "not intersect" if diag else "intersect"
    if diag:
        internal = in_cone(verts_poly, indices_poly, dia, dib)
        lbl += " (internal)" if internal else " (external)"

    plt.subplot(pid)
    # print polygon
    plt.plot(
        list(verts_poly[:, 0]) + [verts_poly[0, 0]],
        list(verts_poly[:, 1]) + [verts_poly[0, 1]]
    )
    # print sampled diagonal
    plt.plot(
        [verts_poly[dia, 0], verts_poly[dib, 0]],
        [verts_poly[dia, 1], verts_poly[dib, 1]],
        label=lbl
    )
    plt.legend()
plt.show()

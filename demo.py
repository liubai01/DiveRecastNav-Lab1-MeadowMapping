import meadow_map
import numpy as np
import matplotlib.pyplot as plt
from utils.MinBinaryHeap import MinBinaryHeap

from meadow_map.basic_ops import left_on


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

verts_hole = np.array(
    [
        [0.5, 0.5], [0.2, 1.5], [0.4, 2.],
        [1.8, 0.5]
    ]
)

verts_hole1 = np.array(
    [
        [2.5, 1.], [3., 2], [3.5, 1]
    ]
)
indices_hole = [(i + 2) % verts_hole.shape[0] for i in range(verts_hole.shape[0])]  # CW
indices_hole1 = [(i + 2) % verts_hole1.shape[0] for i in range(verts_hole1.shape[0])]  # CW

verts, indices, mergeLineSeg1 = meadow_map.merge_hole(verts_poly, indices_poly, verts_hole, indices_hole)
verts, indices, mergeLineSeg2 = meadow_map.merge_hole(verts, indices, verts_hole1, indices_hole1)

polys, diags = meadow_map.convexify(verts, indices)

# plot all diags. with dotted line
diagsAll = []
diagsAll.append([mergeLineSeg1[0], mergeLineSeg1[1]])
for d in diags:
    posA = verts[indices[d[0]]]
    posB = verts[indices[d[1]]]
    diagsAll.append([indices[d[0]], indices[d[1]]])
    plt.plot([posA[0], posB[0]], [posA[1], posB[1]], "--", c=[0.4, 0.4, 0.8])

# indices for result convexy_polys
indices_res_polys = [i for i in range(len(polys))]
# indices for diagnals
indices_res_diags = [i for i in range(len(diagsAll))]

for diag_indice in indices_res_diags:
    _diag = diagsAll[diag_indice]
    posA = verts[_diag[0]]
    posB = verts[_diag[1]]
    plt.text((posA[0] + posB[0]) / 2, (posA[1] + posB[1]) / 2, diag_indice, color="red")

# plot the result
plot_poly(verts_poly, indices_poly, [0, 0, 1.0])
plot_poly(verts_hole, indices_hole, [0.0, 0.0, 0.0])
plot_poly(verts_hole1, indices_hole1, [0.0, 0.0, 0.0])

# plot the line segment that merge the hole
plt.plot(
    [verts[mergeLineSeg1[0]][0], verts[mergeLineSeg1[1]][0]],
    [verts[mergeLineSeg1[0]][1], verts[mergeLineSeg1[1]][1]],
    "--", c=[0.9, 0.4, 0.8]
)

plt.plot(
    [verts[mergeLineSeg2[0]][0], verts[mergeLineSeg2[1]][0]],
    [verts[mergeLineSeg2[0]][1], verts[mergeLineSeg2[1]][1]],
    "--", c=[0.9, 0.4, 0.8]
)



# get the center pos of poly
def getCenterPos(verts, verts_indices):
    sumx = 0
    sumy = 0
    for indice in verts_indices:
        sumx += verts[indice][0]
        sumy += verts[indice][1]
    centX = sumx / len(verts_indices)
    centY = sumy / len(verts_indices)
    return [centX, centY]


# show the centroid of a triangle by the item number
center_of_polys = {}
for i in range(len(polys)):
    centerPos = getCenterPos(verts, polys[i])
    center_of_polys[i] = centerPos
    plt.text(centerPos[0], centerPos[1], i, color="black")
    # plt.scatter(centX, centY)

# search the path
startPos = [1., 3.5]
endPos = [3.5, 1.2]

plt.scatter(startPos[0], startPos[1])
plt.scatter(endPos[0], endPos[1])


def generateLineNum(origin, target):
    return str(origin) + "_" + str(target)


# establishing a bidirectional index for the diagonals
biDirDignal = {}
for diag_indice in indices_res_diags:
    _diag = diagsAll[diag_indice]
    positive_str = generateLineNum(_diag[0], _diag[1])
    negative_str = generateLineNum(_diag[1], _diag[0])
    biDirDignal[positive_str] = diag_indice
    biDirDignal[negative_str] = diag_indice

# record ploygons connected by diagnals
diag_poly_map = {}

# record neighbours of polygons
poly_neighbour = {}
# detect which polygons contain internal diagonals.
for i in range(len(polys)):
    poly_indices = polys[i]
    for j in range(len(poly_indices)):
        now = poly_indices[j]
        if j != len(poly_indices) - 1:
            next = poly_indices[j + 1]
        else:
            next = poly_indices[0]
        lineStr = generateLineNum(now, next)
        if lineStr in biDirDignal:
            diag_num = biDirDignal[lineStr]
            if diag_num not in diag_poly_map:
                diag_poly_map[diag_num] = []
            if i not in poly_neighbour:
                poly_neighbour[i] = {}
            diag_poly_map[diag_num].append(i)
            poly_neighbour[i][diag_num] = 0  # Simply providing default values and will handle the rest later


# get distance between two pos
def getDistance(posA, posB):
    return (posB[0] - posA[0]) ** 2 + (posB[1] - posA[1]) ** 2


# mapping of adjacent triangles to corresponding diagonals
poly_diag_map = {}
#
center_distance_map = {}
for diag_num, poly_indices in diag_poly_map.items():
    poly_indice1 = poly_indices[0]
    poly_indice2 = poly_indices[1]
    poly_diag_map[str(poly_indice1) + "_" + str(poly_indice2)] = diag_num
    poly_diag_map[str(poly_indice2) + "_" + str(poly_indice1)] = diag_num
    center_poly1 = getCenterPos(verts, polys[poly_indice1])
    center_poly2 = getCenterPos(verts, polys[poly_indice2])
    distance = getDistance(center_poly1, center_poly2)
    center_distance_map[str(poly_indice1) + "_" + str(poly_indice2)] = distance
    center_distance_map[str(poly_indice2) + "_" + str(poly_indice1)] = distance

# get neighbours of polygons
for poly_indice, diag_nums in poly_neighbour.items():
    for diag_num in diag_nums:
        if diag_num in diag_poly_map:
            for _poly_indice in diag_poly_map[diag_num]:
                if _poly_indice != poly_indice:
                    poly_neighbour[poly_indice][diag_num] = _poly_indice

# get the polygon where the starting point and ending point are located.
startPolyIndice = 0
endPolyIndice = 0
for poly_indice in indices_res_polys:
    poly = polys[poly_indice]
    count = len(poly)
    if startPolyIndice == 0 or endPolyIndice == 0:
        startFlag = True
        endFlag = True
        for i in range(count):
            ia = verts[poly[i]]
            if i != count - 1:
                ia_next = verts[poly[i + 1]]
            else:
                ia_next = verts[poly[0]]
            if startPolyIndice == 0:
                if not left_on(ia, ia_next, startPos):
                    startFlag = False
            if endPolyIndice == 0:
                if not left_on(ia, ia_next, endPos):
                    endFlag = False
        if startPolyIndice == 0 and startFlag:
            startPolyIndice = poly_indice
        if endPolyIndice == 0 and endFlag:
            endPolyIndice = poly_indice


# construct path
def constructPath(predecessors, start, goal):
    path_polys = []
    current_poly = goal
    while (current_poly != start):
        path_polys.insert(0, current_poly)
        current_poly = predecessors[current_poly]
    return path_polys

# overloading the compare function of binaryheap
def custom_compare(node1, node2):
    if node1['f'] == node2['f']:
        return True
    else:
        return node1['f'] < node2['f']


# overloading the insert function of binaryheap
def insert(self, value):
    self.heap.append(value)
    index = len(self.heap) - 1
    value['index'] = index
    self.value_index_map[value['polyIndice']] = value
    self._percolate_up(index)

#A* algorithm
def findPassPolys(poly_neighbour, startPoly, endPoly):
    """
    Return the pass polygon indices between start polygon and end polygon.
    :param poly_neighbour   dictionary  all the polys and thier neighbours
    :param startPoly:       int         the index of start polygon
    :param endPoly:         int         the index of end polygon
    :return:                list        a list of the pass polygon indices between start polygon and end polygon.
    """
    closeList = {}  # visited poly
    initNode = {
        'g': 0,
        'h': 0,
        'f': 0,
        'polyIndice': startPoly
    }
    heap = MinBinaryHeap(compare_func=custom_compare, insert_func=insert)
    heap.insert(heap, initNode)
    while (len(heap.heap) > 0):
        node = heap.pop_min()
        closeList[node['polyIndice']] = True
        nodePolyIndice = node['polyIndice']
        if nodePolyIndice == endPoly:
            path = []
            path.append(nodePolyIndice)
            fatherIndice = heap.value_index_map[nodePolyIndice]['father']
            while (fatherIndice != startPolyIndice):
                path.append(fatherIndice)
                fatherIndice = heap.value_index_map[fatherIndice]['father']
            path.append(startPoly)
            path.reverse()
            return path
        for diag_num, neighbour_poly_indice in poly_neighbour[nodePolyIndice].items():
            if neighbour_poly_indice not in closeList:
                g = node['g'] + center_distance_map[str(neighbour_poly_indice) + "_" + str(nodePolyIndice)]
                if neighbour_poly_indice not in heap.value_index_map:
                    # get value H of neighbour
                    h = getDistance(center_of_polys[neighbour_poly_indice], endPos)
                    # get value G when arrive neighbour
                    neighbour_node = {
                        'g': g,
                        'h': h,
                        'f': h + g,
                        'polyIndice': neighbour_poly_indice,
                        'father': nodePolyIndice,
                    }
                    heap.insert(heap, neighbour_node)
                else:
                    neighbour_node = heap.value_index_map[neighbour_poly_indice]
                    ng = neighbour_node['g']
                    if ng > g:
                        neighbour_node['father'] = node
                        neighbour_node['g'] = g
                        neighbour_node['f'] = h + g
                        # fix heap
                        heap.update(neighbour_node['index'])


# get the pass ploygons No. between the startpos and endpos
path_poly = findPassPolys(poly_neighbour, startPolyIndice, endPolyIndice)

# show the path of polys
for i in range(len(path_poly) - 1):
    center = center_of_polys[path_poly[i]]
    next_center = center_of_polys[path_poly[i + 1]]
    plt.plot(
        [center[0], next_center[0]],
        [center[1], next_center[1]],
        "--", c='green'
    )


pass_diagnals = []
for i in range(len(path_poly) - 1):
    pass_diagnals.append(poly_diag_map[str(path_poly[i])+"_"+str(path_poly[i + 1])])


#get the pass diagnals (Funnel Algorithm)



plt.grid()
plt.title("Convexify with holes")
plt.show()

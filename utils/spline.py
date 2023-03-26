import bpy
import bpy.utils
import mathutils
import numpy

from ..log import logger, log

NUM_POINTS = 100  # The higher the number the more precise the curve will be

def catmull_rom_spline(P0, P1, P2, P3, num_points, alpha=0.5):
    """
    Compute the points in the spline segment
    :param P0, P1, P2, and P3: The (x,y) point pairs that define the Catmull-Rom spline
    :param num_points: The number of points to include in the resulting curve segment
    :param alpha: 0.5 for the centripetal spline, 0.0 for the uniform spline, 1.0 for the chordal spline.
    :return: The points
    """

    # Calculate t0 to t4. Then only calculate points between P1 and P2.
    # Reshape linspace so that we can multiply by the points P0 to P3
    # and get a point for each value of t.
    def tj(ti, pi, pj):
        xi, yi, zi = pi
        xj, yj, zj = pj
        dx, dy, dz = xj - xi, yj - yi, zj - zi
        l = (dx ** 2 + dy ** 2 + dz ** 2) ** 0.5
        return ti + l

    t0 = 0.0
    t1 = tj(t0, P0, P1)
    t2 = tj(t1, P1, P2)
    t3 = tj(t2, P2, P3)
    t = numpy.linspace(t1, t2, num_points).reshape(num_points, 1)

    A1 = (t1 - t) / (t1 - t0) * P0 + (t - t0) / (t1 - t0) * P1
    A2 = (t2 - t) / (t2 - t1) * P1 + (t - t1) / (t2 - t1) * P2
    A3 = (t3 - t) / (t3 - t2) * P2 + (t - t2) / (t3 - t2) * P3
    B1 = (t2 - t) / (t2 - t0) * A1 + (t - t0) / (t2 - t0) * A2
    B2 = (t3 - t) / (t3 - t1) * A2 + (t - t1) / (t3 - t1) * A3
    points = (t2 - t) / (t2 - t1) * B1 + (t - t1) / (t2 - t1) * B2
    return points


def catmull_rom_chain(points: tuple, num_points: int) -> list:
    """
    Calculate Catmull-Rom for a sequence of initial points and return the combined curve.
    :param points: Base points from which the quadruples for the algorithm are taken
    :param num_points: The number of points to include in each curve segment
    :return: The chain of all points (points of all segments)
    """
    point_quadruples = (
        (points[idx_segment_start + d] for d in range(4))
        for idx_segment_start in range(len(points) - 3)
    )
    all_splines = (catmull_rom_spline(*q, num_points) for q in point_quadruples)

    chain = [chain_point for spline in all_splines for chain_point in spline]  # flatten

    return chain


def catmull_rom_length(points):
    sum = 0
    for i in range(len(points) - 1):
        sum += numpy.linalg.norm(points[i + 1] - points[i])
    return sum


@log
def point_on_catmull_rom(points: list[list[float]], t: float) -> mathutils.Vector:
    """
    Get a point on a Catmull-Rom spline
    :param points: List of points (x,y,z) that define the spline
    :param t: A value between 0 and 1 that defines the position on the spline
    :return: The point on the spline
    """
    if t < 0 or t > 1:
        return None
    if t < 0.001:
        return points[1]
    elif t > 0.999:
        return points[-2]
    chain_points = catmull_rom_chain(points, NUM_POINTS)[1:-1]
    spline_len = catmull_rom_length(chain_points)

    target_len = spline_len * t

    len_sum = 0
    for i in range(len(chain_points) - 1):
        seg_vec = chain_points[i + 1] - chain_points[i]
        seg_len = numpy.linalg.norm(seg_vec)
        if len_sum + seg_len >= target_len:
            magnitude = numpy.linalg.norm(seg_vec)
            normalized_vec = seg_vec / magnitude
            final_pos = (target_len - len_sum) * normalized_vec + chain_points[i]
            return final_pos
        else:
            len_sum += seg_len
    return None
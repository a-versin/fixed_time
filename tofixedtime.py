import math
import numpy as np


def procsegment(d_xyz, v_raw, t_s, a_lim):
    # Interpolates a movement segment
    # Parameters: d_xyz: coordinate changes (x,y,z), v_raw: target velocity,
    # t_s: desired step size, and a_lim: acceleration limit
    # Returns x, y, z numpy arrays

    trvl_len = (d_xyz[0] ** 2 + d_xyz[1] ** 2 + d_xyz[2] ** 2) ** (1 / 2)

    # Velocity pulse train would have been length n:
    # the distance divided by velocity and sample time
    n = math.ceil(trvl_len / v_raw / t_s)
    v_raw = trvl_len / (n * t_s)  # to account for ceil()

    # To limit the net acceleration, account for the axis
    # distribution first
    a_lim_net = a_lim * trvl_len / (abs(d_xyz[0]) + abs(d_xyz[1]) + abs(d_xyz[2]))

    # Coefficient of linear filter is determined by the
    # target velocity divided by acceleration limit and sample time
    m = math.ceil(v_raw / (a_lim_net * t_s))

    v = [0.0] * (n + m - 1)

    # "Convolution" of v_raw with linear (moving average) filter
    for k, _ in enumerate(v):
        # Difference equation: y[k] = y[k-1] + 1/m (v_raw[k]) - 1/m (v_raw[k-m])
        if k == 0:
            v[k] = 0
        else:
            v[k] = v[k - 1]
        # Evaluate v_raw[k] as nonzero only if index in range
        if 0 <= k < n:
            v[k] += (1 / m) * v_raw
        # Evaluate v_raw[k] as nonzero only if index in range
        if 0 <= (k - m) < n:
            v[k] -= (1 / m) * v_raw

    v = np.array(v)
    # Integrate velocity profile to get position, then
    # scale by distance ratio to distribute
    x = np.cumsum(t_s * (d_xyz[0] / trvl_len) * v)
    y = np.cumsum(t_s * (d_xyz[1] / trvl_len) * v)
    z = np.cumsum(t_s * (d_xyz[2] / trvl_len) * v)

    return x, y, z

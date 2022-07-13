import numpy as np
import csv
import matplotlib.pyplot as plt
from tofixedtime import procsegment


# Load the file
file_in = open(".\\in\\DDA_Trajectory_07_11.txt", 'r')
data_in = np.genfromtxt(file_in, delimiter=' ', skip_footer=1)  # skipping last line to avoid error
strtPsn = data_in[:, 3:6].tolist()
deltaPsn = data_in[:, 6:9].tolist()
v_in = (750000 * data_in[:, 11]).tolist()


# Do the conversion to fixed time

# setup running lists, step size to use
x = [strtPsn[0][0]]; y = [strtPsn[0][1]]; z = [strtPsn[0][2]]
t_s = 0.0025

# Iterate through the segments in the input file
for segIdx, _ in enumerate(strtPsn):
    # zero travel protection (when all axis displacement is zero)
    if max([abs(axis) for axis in deltaPsn[segIdx]]) == 0:
        continue
    else:
        # Interpolate the segment. the step size, t_s is in seconds
        # the acceleration limit is in mm/s**2 (?) (1000 = .1 g)
        x_new, y_new, z_new = procsegment(deltaPsn[segIdx], v_raw=v_in[segIdx], t_s=t_s, a_lim=1000)

        # add the starting position to the calculated trajectory
        x_new = (strtPsn[segIdx][0] + x_new).tolist()
        y_new = (strtPsn[segIdx][1] + y_new).tolist()
        z_new = (strtPsn[segIdx][2] + z_new).tolist()

        # append the data to the running lists
        for i, _ in enumerate(x_new):
            x.append(x_new[i])
            y.append(y_new[i])
            z.append(z_new[i])


# Output to csv

with open('.\\out\\fixedTimeOutput.csv', 'w', newline='') as csvfile:
    writerObj = csv.writer(csvfile, delimiter=',')
    for i, _ in enumerate(x):
        writerObj.writerow([x[i], y[i], z[i], round(i*t_s, 4)])


# Plot the results

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# https://matplotlib.org/stable/gallery/mplot3d/scatter3d.html?highlight=3d%20scatter
ax.scatter(x, y, z, marker='.', s=5, linewidths=0, c=z, cmap='viridis', norm=plt.Normalize(0, 21))

# Focus window on the part
ax.set_xlim([110, 140])
ax.set_ylim([90, 120])
ax.set_zlim([0, 25])
plt.show()

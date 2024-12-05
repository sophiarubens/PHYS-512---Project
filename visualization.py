import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.animation import FuncAnimation

num_checks = 54
time = np.zeros((5000*num_checks, 1))
rx = np.zeros((5000*num_checks, 9))
ry = np.zeros((5000*num_checks, 9))
vx = np.zeros((5000*num_checks, 9))
vy = np.zeros((5000*num_checks, 9))

for i in range(1, num_checks+1):
    data_check = pd.read_csv(f'./Checkpoints3/SolarSystemSimulationCheckpoint{i}.csv')

    time[5000*(i-1):5000*(i), 0] = data_check.iloc[:, 1].to_numpy()
    rx[5000*(i-1):5000*(i), :] = data_check.iloc[:, 2:11].to_numpy()
    ry[5000*(i-1):5000*(i), :] = data_check.iloc[:, 11:20].to_numpy()
    vx[5000*(i-1):5000*(i), :] = data_check.iloc[:, 20:29].to_numpy()
    vy[5000*(i-1):5000*(i), :] = data_check.iloc[:, 29:38].to_numpy()

print('Import successful.')

time = time[-2000:, 0]
rx = rx[-2000:, :]
ry = ry[-2000:, :]
vx = vx[-2000:, :]
vy = vy[-2000:, :]

#0 = Sun, 1 = Mercury, 2 = Venus, 3 = Earth, 4 = Mars, 5 = Jupiter, 6 = Saturn, 7 = Uranus, 8 = Neptune

body_names=['Sun','Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus','Neptune']
colors = ['yellow', 'gray', 'orange', 'blue', 'red', 'brown', 'gold', 'lightblue', 'darkblue']
sizes = [10, 2, 3, 4, 3, 6, 5, 5, 5]  # Plotting size of each planet, not physical (obviously)

#Create figure for static plot
fig, axs = plt.subplots(nrows=1, ncols=2)
for i in range(9):
        #Plot all the planets
        axs[0].plot(rx[-2000:, i], ry[-2000:, i], c=colors[i], markersize=2, label=body_names[i])
        #Plot the inner 4 planets.
        axs[1].plot(rx[-26:, i], ry[-26:, i], c=colors[i], markersize=2, label=body_names[i])
axs[0].set_aspect('equal', 'box')
axs[1].legend(loc="upper left", bbox_to_anchor=(1, 1))
axs[1].set_aspect('equal', 'box')
axs[1].set_xlim(-6.1e12, -5.4e12)
axs[1].set_ylim(7.7e12, 8.4e12)
plt.show()


# Create figure for animation - used help from online sources.
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_aspect('equal', 'box')

#Lists to store where planets are in the animation
planet_location = []
tails = []
#Create a tail on each planet.
len_tail = 10

for i in range(len(body_names)):
    #Plot the planet
    scatter, = ax.plot([], [], 'o', color=colors[i], markersize=sizes[i], label=body_names[i])
    #Create the tail
    trail, = ax.plot([], [], '-', color=colors[i], linewidth=1, alpha=0.5)

    planet_location.append(scatter)
    tails.append(trail)

ax.legend()
#Time counter initialization
time_text = ax.text(-2e13, 2e13, '', fontsize=12, color='black', ha='left', bbox=dict(facecolor='white', alpha=0.5))
'''
#Run the animation
for frame in range(len(time)):
    for i, (scatter, trail) in enumerate(zip(planet_location, tails)):
        #Update the planet location
        scatter.set_data([rx[frame, i]], [ry[frame, i]])

        #Update the tail
        start = max(0, frame - len_tail)
        trail.set_data(rx[start:frame, i], ry[start:frame, i])

    #Dynamically update the axis bounds
    ax.set_xlim(np.min(rx) - 1e11, np.max(rx) + 1e11)
    ax.set_ylim(np.min(ry) - 1e11, np.max(ry) + 1e11)

    #Dynamically update the position of the year counter
    time_text.set_position((np.min(rx) + 2e11, np.max(ry) - 2e11))
    #Earth time
    time_text.set_text(f"Time: Earth Year {2024 + time[frame]/(86400*7*52*0.5):.2f}")
'''
def update(frame):
    for i, (scatter, trail) in enumerate(zip(planet_location, tails)):
        #Update the planet location
        scatter.set_data([rx[frame, i]], [ry[frame, i]])

        #Update the tail
        start = max(0, frame - len_tail)
        trail.set_data(rx[start:frame, i], ry[start:frame, i])

    #Dynamically update the axis bounds
    ax.set_xlim(np.min(rx) - 1e11, np.max(rx) + 1e11)
    ax.set_ylim(np.min(ry) - 1e11, np.max(ry) + 1e11)

    #Dynamically update the position of the year counter
    time_text.set_position((np.min(rx) + 2e11, np.max(ry) - 2e11))
    #Earth time
    time_text.set_text(f"Time: Earth Year {2024 + time[frame].item()/(86400*7*52*0.5):.2f}")

    return planet_location + tails + [time_text]

# Create the animation
anim = FuncAnimation(fig, update, frames=len(time), interval=50, blit=True)

# Save the animation as a GIF
anim.save("solar_system.gif", writer="pillow", fps=20)

print("Animation complete")


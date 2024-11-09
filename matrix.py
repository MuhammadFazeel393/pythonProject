import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.animation import FuncAnimation
import shutil

# Check if ffmpeg is available; if not, use GIF
if shutil.which("ffmpeg") is None:
    print("ffmpeg not available; defaulting to GIF format.")

# Ask the user for the desired filename
filename = input("Enter the filename (with .gif extension): ")
if not filename.endswith(".gif"):
    filename = filename + ".gif"

# Create figure and 3D axes with increased figure size
fig = plt.figure(figsize=(24, 16))  # Larger figure size for more space
ax = fig.add_subplot(111, projection='3d')

# Define cube dimensions (5x5x5 for simplicity)
x, y, z = np.indices((5, 5, 5))

# Define the base color array for cells
colors = np.empty(x.shape + (4,), dtype=float)
colors[...] = [0.5, 0.5, 1, 0.6]  # Default color with transparency (light blue)

# Coordinates of the red voxel's base position
highlighted_column_x, highlighted_column_y = 1, 3

# Animation update function to move the red voxel up and down along the z-axis
def update(frame):
    ax.cla()  # Clear the plot for each frame

    # Create a fresh colors array for each frame
    current_colors = colors.copy()

    # Calculate z-position to create up-and-down motion
    z_position = frame if frame <= 4 else 8 - frame  # Moves up and then down

    # Apply the red color to the calculated z position in the highlighted column
    current_colors[highlighted_column_x, highlighted_column_y, z_position] = [1, 0, 0, 0.8]

    # Plot the voxels with the updated color array
    ax.voxels(np.ones((5, 5, 5), dtype=bool), facecolors=current_colors, edgecolor='k', linewidth=0.2)

    # Set axis labels with extra padding and increased fontsize
    ax.set_xlabel('Main Function of the Component', labelpad=120, fontsize=16)
    ax.set_ylabel('Failure Mode of the Component', labelpad=120, fontsize=16)
    ax.set_zlabel('Intended Correction', labelpad=105, fontsize=16)

    # Customize tick labels for each axis with more spacing and rotation adjustments
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_xticklabels(['Optimize Lubrication', 'Protect Components', 'Absorb Mechanical Loads',
                        'Minimize Friction', 'Support Shaft Rotation'], rotation=20, ha="right", fontsize=14)

    ax.set_yticks([0, 1, 2, 3, 4])
    ax.set_yticklabels(['Bearing Fatigue', 'Corrosion', 'Thermal Expansion',
                        'Misalignment Issues', 'Abrasion Wear'], rotation=-25, ha="left", fontsize=14)

    ax.set_zticks([0, 1, 2, 3, 4])
    ax.set_zticklabels(['Enhance Alignment Precision', 'Add Protective Coatings', 'Increase Inspection Frequency',
                        'Improve Material Quality', 'Use High-Quality Bearings'], fontsize=14)

    # Adjust view and layout for more space between labels
    fig.subplots_adjust(left=0.35, right=0.65, top=0.85, bottom=0.3)  # Adjust layout for spacing

    # Shift the z-axis position for better label placement
    ax.get_proj = lambda: np.dot(Axes3D.get_proj(ax), np.diag([1, 1, 0.7, 1]))  # Compressed z-axis for more space

    # Increase distance of tick labels from the plot using tick_params
    ax.tick_params(axis='x', pad=20)
    ax.tick_params(axis='y', pad=20)
    ax.tick_params(axis='z', pad=50)

    # Set main title with additional padding
    fig.suptitle("3D Reliability Analysis for Gamesa G114 Gearbox", fontsize=18, y=0.94)

    # Adjust viewing angle for clarity
    ax.view_init(elev=25, azim=135)

    # Set the aspect ratio to make the plot rectangular
    ax.set_box_aspect([1.5, 1.5, 1])

# Create the animation
ani = FuncAnimation(fig, update, frames=np.arange(0, 9), repeat=True)

# Save the animation as a GIF
ani.save(filename, writer='imagemagick', fps=5)

# Show plot for preview (optional)
plt.show()

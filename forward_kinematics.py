from scipy.spatial.transform import Rotation as R
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

l1_length = 35
l2_length = 35
l3_length = 35
l4_length = 35
l5_length = 35
l6_length = 30

scale_factor = 30
# Rotation and translation functions
def rotate_vector(v, axis, angle_deg):
    angle_rad = np.radians(angle_deg)
    if axis == 'x':
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(angle_rad), -np.sin(angle_rad)],
            [0, np.sin(angle_rad), np.cos(angle_rad)]
        ])
    elif axis == 'y':
        rotation_matrix = np.array([
            [np.cos(angle_rad), 0, np.sin(angle_rad)],
            [0, 1, 0],
            [-np.sin(angle_rad), 0, np.cos(angle_rad)]
        ])
    elif axis == 'z':
        rotation_matrix = np.array([
            [np.cos(angle_rad), -np.sin(angle_rad), 0],
            [np.sin(angle_rad), np.cos(angle_rad), 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Axis must be one of 'x', 'y', or 'z'")
    return np.dot(rotation_matrix, v)

def translate_vector(v, translation):
    return v + translation

# Function to create a coordinate frame
def create_frame(origin=np.array([0, 0, 0]), axes=None):
    if axes is None:
        axes = {
            'X': np.array([scale_factor, 0, 0]),
            'Y': np.array([0, scale_factor, 0]),
            'Z': np.array([0, 0, scale_factor])
        }
    return {
        'origin': origin,
        'axes': axes
    }

def cos(angle):
    return np.cos(np.radians(angle))

def sin(angle):
    return np.sin(np.radians(angle))

def sec(angle):
    return 1 / np.cos(np.radians(angle))

def tan(angle):
    return 1 / np.tan(np.radians(angle))

# Function to plot the frame
def plot_frame(ax, frame, color_map=None, label_prefix=""):
    color_map = color_map or {'X': 'b', 'Y': 'g', 'Z': 'r'}
    ax.quiver(*frame['origin'], *frame['axes']['X'], color=color_map['X'], length=1, label=f'{label_prefix} X-axis', arrow_length_ratio=0.1)
    ax.quiver(*frame['origin'], *frame['axes']['Y'], color=color_map['Y'], length=1, label=f'{label_prefix} Y-axis', arrow_length_ratio=0.1)
    ax.quiver(*frame['origin'], *frame['axes']['Z'], color=color_map['Z'], length=1, label=f'{label_prefix} Z-axis', arrow_length_ratio=0.1)

# Define the Transformation class
class Transformation:
    def __init__(self, type, **kwargs):
        self.type = type
        self.kwargs = kwargs
    
    def apply(self, frame):
        if self.type == 'rotation':
            axis = self.kwargs['axis']
            angle = self.kwargs['angle']
            frame['axes']['X'] = rotate_vector(frame['axes']['X'], axis, angle)
            frame['axes']['Y'] = rotate_vector(frame['axes']['Y'], axis, angle)
            frame['axes']['Z'] = rotate_vector(frame['axes']['Z'], axis, angle)
        elif self.type == 'translation':
            translation = self.kwargs['translation']
            frame['origin'] = translate_vector(frame['origin'], translation)
        return frame

# Function to update the plot based on slider values
def update_plot(val):
    # Reinitialize the frame
    current_frame = create_frame(np.array([0, 0, 0]), {'X': np.array([scale_factor, 0, 0]), 'Y': np.array([0, scale_factor, 0]), 'Z': np.array([0, 0, scale_factor])})
    euler_angles_deg = [0,0,0]
    # Read slider values
    theta1 = slider_theta1.val
    theta2 = slider_theta2.val
    theta3 = slider_theta3.val
    theta4 = slider_theta4.val
    theta5 = slider_theta5.val
    theta6 = slider_theta6.val
    
    # Define transformations for each frame (simplified for this example)
    transformations = [
    [  # Transformations for Frame 1
        Transformation('translation', translation=np.array([0, 0, l1_length])),
        Transformation('rotation', axis='z', angle=theta1),
    ],
    [  # Transformations for Frame 2
         Transformation('rotation', axis='z', angle=-theta1),
         Transformation('rotation', axis='x', angle=-90),
         Transformation('rotation', axis='y', angle=theta2),
         Transformation('rotation', axis='z', angle=theta1),
         Transformation('translation', translation=np.array([l2_length * cos(theta1), l2_length * sin(theta1), 0])),
    ],
    [  # Transformations for Frame 3
         Transformation('rotation', axis='z', angle=-theta1),
         Transformation('rotation', axis='y', angle=-theta2),
         Transformation('translation', translation=np.array([(l3_length * sin(theta2)) - (l3_length * sin(theta2) * (1 - cos(theta1))) , l3_length * sin(theta1) * sin(theta2), l3_length * cos(theta2)])),
         Transformation('rotation', axis='y', angle=theta3),
         Transformation('rotation', axis='y', angle=theta2),
         Transformation('rotation', axis='z', angle=theta1),
      
    ],
    [  # Transformations for Frame 4
        Transformation('rotation', axis='z', angle=-theta1),
        Transformation('rotation', axis='y', angle=-theta2),
        Transformation('rotation', axis='y', angle=-theta3),
        Transformation('translation', translation=np.array([l4_length * cos(theta2 + theta3) * cos(theta1), l4_length * sin(theta1) * cos(theta2 + theta3), -1 * l4_length * sin(180-(theta2+theta3))])),
        Transformation('rotation', axis='z', angle=-90),
        Transformation('rotation', axis='x', angle=theta4),
        Transformation('rotation', axis='y', angle=theta3),
        Transformation('rotation', axis='y', angle=theta2),
        Transformation('rotation', axis='z', angle=theta1),
    ],
    [  # Transformations for Frame 5
        Transformation('rotation', axis='z', angle=-theta1),
        Transformation('rotation', axis='y', angle=-theta2),
        Transformation('rotation', axis='y', angle=-theta3),
        Transformation('rotation', axis='x', angle=-theta4),
        Transformation('translation', translation=np.array([l5_length * cos(theta2 + theta3) * cos(theta1), l5_length * sin(theta1) * cos(theta2 + theta3), -1 * l5_length * sin(180-(theta2+theta3))])),
        Transformation('rotation', axis='z', angle=90),
        Transformation('rotation', axis='y', angle=theta5),
        Transformation('rotation', axis='x', angle=theta4),
        Transformation('rotation', axis='y', angle=theta3),
        Transformation('rotation', axis='y', angle=theta2),
        Transformation('rotation', axis='z', angle=theta1),
    ],
    ]

    end_effector_degrees = []
    temp_frame = create_frame(np.array([0, 0, 0]), {'X': np.array([scale_factor, 0, 0]), 'Y': np.array([0, scale_factor, 0]), 'Z': np.array([0, 0, scale_factor])})
    for transform_list in transformations:
        for transform in transform_list:
            temp_frame = transform.apply(temp_frame)
            rotation_matrix = np.array([temp_frame['axes']['X'], temp_frame['axes']['Y'], temp_frame['axes']['Z']]) / scale_factor
            rotation = R.from_matrix(rotation_matrix)
            end_effector_degrees = rotation.as_euler('zyx', degrees=True)
           
    yaw =  end_effector_degrees[0]
    pitch =end_effector_degrees[1]
    roll = end_effector_degrees[2]

    # x = temp_frame['origin'][0]
    # y = temp_frame['origin'][1]
    # z = temp_frame['origin'][2]

    dx = l6_length * cos(yaw) * cos(pitch)
    dy = -1 * l6_length * sin(yaw) * cos(pitch)
    dz = l6_length * sin(pitch)
   

    # print(yaw, pitch, roll, x+dx,y+dy,z+dz)

  #  print("End effector degrees", end_effector_degrees)
    end_transform = [  # Transformations for Frame 6
        Transformation('rotation', axis='z', angle=-theta1),
        Transformation('rotation', axis='y', angle=-theta2),
        Transformation('rotation', axis='y', angle=-theta3),
        Transformation('rotation', axis='x', angle=-theta4),
        Transformation('rotation', axis='y', angle=-theta5),
        Transformation('rotation', axis='z', angle=-90),
        Transformation('rotation', axis='x', angle=theta6),
    
        Transformation('translation', translation=np.array([dx, dy, dz])),
        Transformation('rotation', axis='y', angle=theta5),
        Transformation('rotation', axis='x', angle=theta4),
        Transformation('rotation', axis='y', angle=theta3),
        Transformation('rotation', axis='y', angle=theta2),
        Transformation('rotation', axis='z', angle=theta1),
    ]
    
    transformations.append(end_transform)
    # Initialize rotation matrix (identity matrix)
 
    # Apply transformations and plot frames

    ax.clear()  # Clear previous plot
    
    for transform_list in transformations:
        for transform in transform_list:
            current_frame = transform.apply(current_frame)
            rotation_matrix = np.array([current_frame['axes']['X'], current_frame['axes']['Y'], current_frame['axes']['Z']]) / scale_factor
            rotation = R.from_matrix(rotation_matrix)
            euler_angles_deg = rotation.as_euler('zyx', degrees=True)
           
        plot_frame(ax, current_frame, label_prefix="Frame")

    # Print the final rotation matrix
    xyz = current_frame['origin']
    
    euler_text.set_text(f"RPY: {euler_angles_deg[1]:.2f} {euler_angles_deg[2]:.2f} {euler_angles_deg[0]:.2f}")
    
    xyz_text.set_text(f"XYZ: {xyz[0]:.2f} {xyz[1]:.2f} {xyz[2]:.2f}")
    # print(total_rotation_matrix)
    
    # Set plot limits and labels
    ax.set_xlim([0, 200])
    ax.set_ylim([0, 200])
    ax.set_zlim([0, 200])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.grid(True)
    # print("RPY", euler_angles_deg)

    # Redraw the plot
    fig.canvas.draw()

# Set up the plot

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create the base frame
base_frame = create_frame(np.array([0, 0, 0]), {'X': np.array([30, 0, 0]), 'Y': np.array([0, 30, 0]), 'Z': np.array([0, 0, 30])})
plot_frame(ax, base_frame, label_prefix="Base (Origin)")


euler_text = fig.text(0.7, 0.9, "Tr", fontsize=10)
xyz_text = fig.text(0.7, 0.85, "Tr", fontsize=10)
#'X=0.00, Y=0.00, Z=0.00'
# Initialize slider values for joint angles
slider_theta1 = Slider(plt.axes([0.1, 0.9, 0.4, 0.03]), 'Theta1', -180, 180, valinit=90)
slider_theta2 = Slider(plt.axes([0.1, 0.85, 0.4, 0.03]), 'Theta2', -180, 180, valinit=-0)
slider_theta3 = Slider(plt.axes([0.1, 0.8, 0.4, 0.03]), 'Theta3', -180, 180, valinit=-0)
slider_theta4 = Slider(plt.axes([0.1, 0.75, 0.4, 0.03]), 'Theta4', -180, 180, valinit=0)
slider_theta5 = Slider(plt.axes([0.1, 0.7, 0.4, 0.03]), 'Theta5', -180, 180, valinit=-0)
slider_theta6 = Slider(plt.axes([0.1, 0.65, 0.4, 0.03]), 'Theta6', -180, 180, valinit=0)

# Connect sliders to the update function
slider_theta1.on_changed(update_plot)
slider_theta2.on_changed(update_plot)
slider_theta3.on_changed(update_plot)
slider_theta4.on_changed(update_plot)
slider_theta5.on_changed(update_plot)
slider_theta6.on_changed(update_plot)

# Initial plot update
update_plot(None)

# Show the plot with sliders
plt.show()

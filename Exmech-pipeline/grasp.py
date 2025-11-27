import robotcontrol
import pyrealsense2 as rs
import math
import time
import numpy as np
import cv2
import transforms3d as tfs
import img_target_estimation
import robot_waypoint
from datetime import datetime

# AUBO initialization
ret = robotcontrol.Auboi5Robot().initialize()
print("auboi5robot().initialize is {0}".format(ret))
# Instantiate object
robot = robotcontrol.Auboi5Robot()
# Create context
handle = robot.create_context()

# Relative movement
def relative_move(axis, distance):
    """
    Move relative to the current position along the specified coordinate axis
    :param axis: x, y, z, direction: relative to the base coordinate system
    :param distance: unit - meters
    """
    if axis == 'x':
        current_pos = robot.get_current_waypoint()
        current_pos['pos'][0] += distance  # Move along X-axis, X increase
        ik_result = robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
        robot.move_line(ik_result['joint'])
    elif axis == 'y':
        current_pos = robot.get_current_waypoint()
        current_pos['pos'][1] += distance  # Move along Y-axis, Y increase
        ik_result = robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
        robot.move_line(ik_result['joint'])
    elif axis == 'z':
        current_pos = robot.get_current_waypoint()
        current_pos['pos'][2] += distance  # Move along Z-axis, Z increase
        ik_result = robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
        robot.move_line(ik_result['joint'])
    else:
        print('Invalid command')
    return

# Get transformation matrix from gripper to base coordinate system
def get_M_g2b():
    # Get current flange center position (in base coordinate system)
    current_pos = robot.get_current_waypoint()
    for i in range(10):
        if current_pos is None:
            print('Failed to get robotic arm position, retrying...')
            time.sleep(1)
            current_pos = robot.get_current_waypoint()
        else:
            print(f'current_pos is: {current_pos}')
            break
    if current_pos is None:
        print('Failed to get robotic arm position, using default joint information')
        current_pos = {
            'joint': [-1.681898, 0.045488, 1.551645, -0.064616, 1.570789, -0.099272],
            'ori': [6.179754714738223e-06, 0.9999533647638482, -0.009657549000516151, -2.56349241260495e-06],
            'pos': [-0.18025101042533231, -0.49193827160772113, 0.4178571394369189]
        }
    tool_pos_on_end = (0, 0, 0.27195)
    tool_ori_on_end = (1, 0, 0, 0)
    tool_desc = {"pos": tool_pos_on_end, "ori": tool_ori_on_end}
    tool_pos_on_base = robot.base_to_base_additional_tool(current_pos['pos'], current_pos['ori'], tool_desc)
    # Convert quaternion to Euler angles (radians)
    tool_rpy = robot.quaternion_to_rpy(tool_pos_on_base['ori'])
    # Convert radians to degrees
    tool_rpy_deg = [math.degrees(radian) for radian in tool_rpy]
    # Position and orientation
    tcp_pos = {"pos": tool_pos_on_base["pos"], "ori": tool_rpy_deg}
    # Get R_g2b
    R_g2b = (tfs.euler.euler2mat(tool_rpy[0], tool_rpy[1], tool_rpy[2], 'sxyz'))
    # Get T_g2b
    T_g2b = tcp_pos['pos']
    homogeneous_matrix = np.eye(4)
    homogeneous_matrix[:3, :3] = R_g2b
    homogeneous_matrix[:3, 3] = T_g2b

    return homogeneous_matrix

# Get aligned rgb and depth images
def get_aligned_images():
    # Initialize realsense, configure camera and start pipeline
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    profile = pipeline.start(config)
    align_to = rs.stream.color
    align = rs.align(align_to)
    time.sleep(1)
    frames = pipeline.wait_for_frames()
    aligned_frames = align.process(frames)
    aligned_depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()
    # Get intel realsense parameters
    intr = color_frame.profile.as_video_stream_profile().intrinsics
    # Intrinsic matrix, converted to ndarray for later use with OpenCV
    intr_matrix = np.array([
        [intr.fx, 0, intr.ppx], [0, intr.fy, intr.ppy], [0, 0, 1]
    ])
    depth_image = np.asanyarray(aligned_depth_frame.get_data())
    depth_image_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)
    pos = np.where(depth_image_8bit == 0)
    depth_image_8bit[pos] = 255
    color_image = np.asanyarray(color_frame.get_data())
    pipeline.stop()
    cv2.destroyAllWindows()
    return color_image, depth_image, intr_matrix, np.array(intr.coeffs)

# Grasping
def plane_grasp(target):
    # Set collision level
    robot.set_collision_class(10)
    joint_maxvelc = (0.6, 0.6, 0.6, 0.6, 0.6, 0.6)
    joint_maxacc = (1.2, 1.2, 1.2, 1.2, 1.2, 1.2)
    robot.set_joint_maxacc(joint_maxacc)
    robot.set_joint_maxvelc(joint_maxvelc)
    p = target[0:3]
    angle = target[3]
    p_pre = p.copy()
    p_pre[2] = 0.436369
    p1 = tuple(p_pre)
    if angle <= 0:
        r1 = (180, 0, angle + 90)
    else:
        r1 = (180, 0, angle - 90)
    robot.move_to_target_in_cartesian(p1, r1)
    time.sleep(1)
    distance = -0.177533
    robot.set_board_io_status(5, "U_DO_00", 1)
    robot.set_board_io_status(5, "U_DO_01", 0)
    time.sleep(1)
    joint_maxvelc = (0.3, 0.3, 0.3, 0.3, 0.3, 0.3)
    joint_maxacc = (0.8, 0.8, 0.8, 0.8, 0.8, 0.8)
    robot.set_joint_maxacc(joint_maxacc)
    robot.set_joint_maxvelc(joint_maxvelc)
    relative_move('z', distance=distance)
    time.sleep(1)
    robot.set_board_io_status(5, "U_DO_00", 0)
    robot.set_board_io_status(5, "U_DO_01", 0)
    time.sleep(1)
    joint_maxvelc = (0.4, 0.4, 0.4, 0.4, 0.4, 0.4)
    joint_maxacc = (1, 1, 1, 1, 1, 1)
    robot.set_joint_maxacc(joint_maxacc)
    robot.set_joint_maxvelc(joint_maxvelc)
    robot.move_joint(robot_waypoint.Tray.photograph)
    return

def grasp_main():
    """
    Grasping main function
    Displays identified target
    Specifies target index
    Performs grasping
    Moves to preparation point
    """
    robot.move_joint(robot_waypoint.Tray.photograph)
    get_aligned_images()
    time.sleep(3)

    color_image, depth_image, intr_matrix, intr_coeffs = get_aligned_images()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    img_name = f"image_{timestamp}.png"
    depth_name = f"depth_{timestamp}.csv"
    cv2.imwrite(img_name, color_image)
    np.savetxt(depth_name, depth_image, delimiter=",", fmt='%d')
    targets = img_target_estimation.target_estimation(color_image)
    user_index = 0
    if user_index == 'q':
        print('Exiting')
    else:
        user_index = int(user_index)
        X = targets[user_index]["centroid"][0]
        Y = targets[user_index]["centroid"][1]
        depth = 0.423
        center = [X, Y, depth]
        point_pixel = np.dot(np.linalg.inv(intr_matrix), np.array([center[0], center[1], 1])) * center[2]
        point_camera = np.append(point_pixel, 1)
        RT_c2g = np.loadtxt('RT_c2g.txt')
        point_gripper = np.dot(RT_c2g, point_camera)
        M_g2b = get_M_g2b()
        point_base = np.dot(M_g2b, point_gripper)
        point_base_rotate = point_base.copy()
        point_base_rotate[3] = targets[user_index]["arrow_angle"]
        print(f"The position of target under base locates on {point_base_rotate}")
        print('Now the gripper is going to the target')
        plane_grasp(point_base_rotate)
    return

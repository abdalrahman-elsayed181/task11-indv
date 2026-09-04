from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
import xacro
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    package_path = get_package_share_directory('robot')  # read the package
    # access xacro file in the package
    xacro_file = os.path.join(
        package_path,
        'urdf',
        'robot.xacro'
    ) 
    # process the file
    robot_description_config = xacro.process_file(
        xacro_file
    )  
    # convert robot description to string
    robot_description = {           
        'robot_description': robot_description_config.toxml()
    }  


    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )


    # calling Gazebo Harmonic launch file

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            )
        ),
        launch_arguments={'gz_args': '-r empty.sdf'}.items()
    )


    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'task11_car'
        ],
        output='screen'
    )


    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry'
        ],
        output='screen'
    )


    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_robot,
        bridge
    ])
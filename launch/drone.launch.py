import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    world = os.path.join(
        get_package_share_directory("my_drone"), "worlds", "one_drone.sdf"
    )

    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory("ros_gz_sim"),
                "launch",
                "gz_sim.launch.py",
            )
        ),
        launch_arguments={"gz_args": f"-r {world}"}.items(),
    )

    # ']' = ROS -> Gazebo,  '[' = Gazebo -> ROS
    bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            "/X3/gazebo/command/twist@geometry_msgs/msg/Twist]gz.msgs.Twist",
            "/X3/enable@std_msgs/msg/Bool]gz.msgs.Boolean",
            "/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock",
        ],
        output="screen",
    )

    return LaunchDescription([gz_sim, bridge])

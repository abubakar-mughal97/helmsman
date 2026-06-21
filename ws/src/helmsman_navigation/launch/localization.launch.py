import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_nav = get_package_share_directory("helmsman_navigation")
    amcl_params = os.path.join(pkg_nav, "config", "amcl.yaml")
    map_yaml = os.path.join(pkg_nav, "maps", "warehouse.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time")
    declare_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use Gazebo's /clock instead of wall time",
    )

    map_server = Node(
        package="nav2_map_server",
        executable="map_server",
        name="map_server",
        output="screen",
        parameters=[
            amcl_params,
            {"use_sim_time": use_sim_time, "yaml_filename": map_yaml},
        ],
    )

    amcl = Node(
        package="nav2_amcl",
        executable="amcl",
        name="amcl",
        output="screen",
        parameters=[amcl_params, {"use_sim_time": use_sim_time}],
    )
    
    lifecycle_manager = Node(
        package="nav2_lifecycle_manager",
        executable="lifecycle_manager",
        name="lifecycle_manager_localization",
        output="screen",
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "autostart": True,
                "node_names": ["map_server", "amcl"],
            }
        ],
    )
    
    odom_publisher = Node(
        package="robot_localization",
        executable="ekf_node",
        name="ekf_filter_node",
        parameters=[{
            "use_sim_time": True,
            "odom_frame": "odom",
            "base_link_frame": "base_footprint",
            "world_frame": "odom",
            "publish_tf": True,

            "odom0": "/odom",
            "odom0_config": [
                True, True, False,
                False, False, True,
                False, False, False,
                False, False, False,
                False, False, False
            ]
        }]
    )
    return LaunchDescription([
        declare_sim_time, 
        map_server, 
        amcl, 
        lifecycle_manager,
        odom_publisher,
    ])
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='lanelet2_map_loader',
            executable='lanelet2_map_loader_node',
            name='lanelet2_map_loader',
            output='screen',
            parameters=[{
                'map_file': '/home/username/ros2_ws/src/shuttle_navigation/maps/laneletmapfinal.osm.bin'
            }]
        )
    ])

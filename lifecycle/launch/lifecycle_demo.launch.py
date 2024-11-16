# Copyright 2018 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import Shutdown
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler, LogInfo
from launch_ros.event_handlers import OnStateTransition

from launch_ros.events.lifecycle import ChangeState
import launch
from lifecycle_msgs.msg import Transition


def generate_launch_description():
    node = LifecycleNode(package='lifecycle', executable='lifecycle_talker',
                         name='lc_talker', namespace='', output='screen')

    configure_event = EmitEvent(
        event=ChangeState(
            lifecycle_node_matcher=launch.events.matches_action(
                node),
            transition_id=Transition.TRANSITION_CONFIGURE,
        ))

    state_handler = RegisterEventHandler(
        OnStateTransition(
            target_lifecycle_node=node,
            goal_state='inactive',
            entities=[
                # Log
                LogInfo(
                    msg="RegisterEventHandler worked")]))

    return LaunchDescription([
        configure_event, node, state_handler
        # Node(package='lifecycle', executable='lifecycle_listener', output='screen'),
        # Node(package='lifecycle', executable='lifecycle_service_client', output='screen',
        #      on_exit=Shutdown()),
    ])

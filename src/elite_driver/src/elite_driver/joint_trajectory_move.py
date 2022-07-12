#!/usr/bin/env python3
"""
################################################################################
# Copyright(C) 2022-2027 Elite. All Rights Reserved.
# @brief : 简介
# @author: 作者
################################################################################
"""
from time import time
import rospy
from elite_msgs.srv import JointTrajectoryMove, JointTrajectoryMoveResponse, JointTrajectoryMoveRequest
from elite import EC


class JointTrajectoryMoveTService():  # pylint: disable=R0903
    """关节轨迹运动服务"""

    def __init__(self) -> None:
        rospy.loginfo("JointTrajectoryMoveTService is started...")
        self.joint_trajectory_move_server = rospy.Service(
            'joint_trajectory_movet', JointTrajectoryMove, self.handle_trajectory_move_)

    def handle_trajectoy_move_(self, request: JointTrajectoryMoveRequest):
        """处理运动请求"""
        response = JointTrajectoryMoveResponse()
        length = request.length
        time_stamp = list(request.time_stamp)
        joint = list(request.joint)
        # time_stamp[1] 为从0开始的第一个时间戳 单位：s
        self.elite_robot.TT_init(t=time_stamp[1]*1000)
        for i in range(len(time_stamp)):
            temp_joint = joint[i*8:i*8+6]
            self.elite_robot.TT_add_joint(temp_joint)
        if request.is_blocking:
            self.elite_robot.wait_stop()  # pylint: disable=E1101
        response.result = True
        return response

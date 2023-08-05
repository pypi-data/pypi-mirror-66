#!/usr/bin/env python3
import numpy as np



def dh_trans_matrix(theta, a, d, alpha):
    t = np.array([[np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)], \
                  [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)], \
                  [0            ,  np.sin(alpha)              ,  np.cos(alpha)              , d              ], \
                  [0            ,  0                          ,  0                          , 1              ]])
    return t






class UR10_Kinematics():
    def __init__(self):

        # Denavit Hartemberg parameters
        self.dh = [{'theta':0, 'a':0,       'd':0.1273,     'alpha': np.pi/2},
                   {'theta':0, 'a':-0.612,  'd':0,          'alpha': 0},
                   {'theta':0, 'a':-0.5723, 'd':0,          'alpha': 0},
                   {'theta':0, 'a':0,       'd':0.163941,   'alpha': np.pi/2},
                   {'theta':0, 'a':0,       'd':0.1157,     'alpha': -np.pi/2},
                   {'theta':0, 'a':0,       'd':0.0922,     'alpha': 0}]


    def get_ee_pose(self,thetas):


        t = self._get_full_t(thetas)
        x = t[0][3]
        y = t[1][3]
        z = t[2][3]

        return [x,y,z]

    def _get_dh_trans_matrix(self, theta, joint_number):

        return dh_trans_matrix(theta, self.dh[joint_number]['a'], \
                               self.dh[joint_number]['d'], self.dh[joint_number]['alpha'])

    def _get_full_t(self, thetas):

        t = self._get_dh_trans_matrix(thetas[0],0)
        for i in range(1,len(thetas)):
            t = np.matmul(t, self._get_dh_trans_matrix(thetas[i],i))

        return t

    def _ros_joint_list_to_ur10_joint_list(self,ros_thetas):

        return np.array([ros_thetas[2],ros_thetas[1],ros_thetas[0],ros_thetas[3],ros_thetas[4],ros_thetas[5]])

    def _ur_10_joint_list_to_ros_joint_list(self,thetas):

        return np.array([thetas[2],thetas[1],thetas[0],thetas[3],thetas[4],thetas[5]])

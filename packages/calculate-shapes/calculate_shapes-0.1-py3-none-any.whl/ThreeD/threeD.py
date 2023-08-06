#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
{Description}
{License_info}
"""
from ThreeD import Constants as const
import math

__author__ = "Deepesh Ahuja"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Deepesh Ahuja"
__email__ = "deepeshahuja141291@gmail.com"
__status__ = "Dev"

class ThreeD():
    def calculateCubeOperation(self,side, operation):
        """
        Calculates Operation for Cube 
        """
        if operation == const.OPERATIONS[0]:
            print('Formula of Cube %s = 6*side*side' % (const.OPERATIONS[0]))
            return 6*side*side
        elif operation == const.OPERATIONS[1]:
            print('Formula of Cube %s = side*side*side' % (const.OPERATIONS[1]))
            return math.pow(side, 3)
    
    def calculateSphereOperation(self,radius, operation):
        """
        Calculates Operation for Sphere 
        """
        if operation == const.OPERATIONS[0]:
            print('Formula of Sphere %s = 4*pi*radius*radius' % (const.OPERATIONS[0]))
            return 4*math.pi*math.pow(radius,2)
        elif operation == const.OPERATIONS[1]:
            print('Formula of Sphere %s = (4/3)*pi*radius*radius*radius' % (const.OPERATIONS[1]))
            return (4/3)*math.pi*math.pow(radius,3)


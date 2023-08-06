#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
{Description}
{License_info}
"""
from TwoD import Constants as const


__author__ = "Deepesh Ahuja"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Deepesh Ahuja"
__email__ = "deepeshahuja141291@gmail.com"
__status__ = "Dev"

class TwoD():
    def calculateSquareOperation(self,side, operation):
        """
        Calculates Operation for Square 
        """
        if operation == const.OPERATIONS[0]:
            print('Formula of Square %s = side*side' % (const.OPERATIONS[0]))
            return side*side
        elif operation == const.OPERATIONS[1]:
            print('Formula of Square %s = 4*side' % (const.OPERATIONS[1]))
            return 4*side
        
    
    def calculateRectangleOperation(self,width, height, operation):
        """
        Calculates Operation for Rectangle 
        """
        if operation == const.OPERATIONS[0]:
            print('Formula of Rectangle %s = width*height' % (const.OPERATIONS[0]))
            return width*height
        elif operation == const.OPERATIONS[1]:
            print('Formula of Rectangle %s = 2*width+2*height' % (const.OPERATIONS[1]))
            return 2*width+2*height
    
    def calculateCircleOperation(self,radius, operation):
        """
        Calculates Operation for Circle 
        """
        if operation == const.OPERATIONS[0]:
            print('Formula of Circle %s = 3.14*radius*radius' % (const.OPERATIONS[0]))
            return 3.14*radius*radius
        elif operation == const.OPERATIONS[1]:
            print('Formula of Circle %s = 3.14*2*radius' % (const.OPERATIONS[1]))
            return 3.14*2*radius


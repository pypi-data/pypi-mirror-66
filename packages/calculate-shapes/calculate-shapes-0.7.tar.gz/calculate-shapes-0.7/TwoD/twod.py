#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
{Description}
{License_info}
"""
from TwoD import Constants as const
import math


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
    
    def calculateEllipseOperation(self,longAxis, shortAxis, operation):
        """
        Calculates Operation for Ellipse 
        """
        if operation == const.OPERATIONS[1]:
            print('Formula of Ellipse %s = 2*pi*sqrt*((longAxis*longAxis+shortAxis*shortAxis)/2)' % (const.OPERATIONS[1]))
            tmp = math.pow(longAxis, 2)+math.pow(shortAxis, 2)
            return 2*math.pi*math.sqrt(tmp/2)
        elif operation == const.OPERATIONS[0]:
            print('Formula of Ellipse %s = pi*longAxis*shortAxis' % (const.OPERATIONS[0]))
            return math.pi*longAxis*shortAxis


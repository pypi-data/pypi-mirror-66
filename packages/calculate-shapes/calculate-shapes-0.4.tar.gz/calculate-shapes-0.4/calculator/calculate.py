
#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
{Description}
"""

from TwoD.twod import TwoD
from TwoD import Constants as TwoDconst
from ThreeD.threeD import ThreeD
from ThreeD import Constants as ThreeDconst
import click
import sys


__author__ = "Deepesh Ahuja"
__copyright__ = ""
__license__ = ""
__version__ = "1.0"
__maintainer__ = "Deepesh Ahuja"
__email__ = "deepeshahuja141291@gmail.com"
__status__ = "Dev"

def exit_n(message, exitcode=1):
    click.echo("{} {}".format(click.style('Failed', fg='red'), message), err=True)
    sys.exit(exitcode)

@click.group('main')
@click.option('-d', 'debug', is_flag=True, default=False, help="Print debug messages to stdout.")
@click.pass_context
def main(ctx, debug):
    print('Click Version: {}'.format(click.__version__))
    print('Python Version: {}'.format(sys.version))

@main.command('square', help='List of operations performed on square.')
@click.option('--operation', '-o', 'operation', required=True,
              help="List of Operation Performed are "+ str(TwoDconst.OPERATIONS))
@click.argument('side', nargs=1)
def square(operation, side):
    """Calculate Square Opearions"""
    if operation.casefold() in TwoDconst.OPERATIONS:
        sq = TwoD()
        print('Square '+ operation.casefold() + '= %f' % (sq.calculateSquareOperation(float(side), operation.casefold())))
    else:
        print('Invalid Operation')

@main.command('rectangle', help='List of operations performed on rectangle.')
@click.option('--operation', '-o', 'operation', required=True,
              help="List of Operation Performed are "+ str(TwoDconst.OPERATIONS))
@click.argument('width', nargs=1)
@click.argument('height', nargs=1)
def rectangle(operation, width, height):
    """Calculate Rectangle Opearions"""
    if operation.casefold() in TwoDconst.OPERATIONS:
        rc = TwoD()
        print('Rectangle '+ operation.casefold() + '= %f' % (rc.calculateRectangleOperation(float(width), float(height),operation.casefold())))
    else:
        print('Invalid Operation')

@main.command('circle', help='List of operations performed on circle.')
@click.option('--operation', '-o', 'operation', required=True,
              help="List of Operation Performed are "+ str(TwoDconst.OPERATIONS))
@click.argument('radius', nargs=1)
def circle(operation, radius):
    """Calculate Circle Opearions"""
    if operation.casefold() in TwoDconst.OPERATIONS:
        cir = TwoD()
        print('Circle '+ operation.casefold() + '= %f' % (cir.calculateCircleOperation(float(radius),operation.casefold())))
    else:
        print('Invalid Operation')

@main.command('sphere', help='List of operations performed on sphere.')
@click.option('--operation', '-o', 'operation', required=True,
              help="List of Operation Performed are "+ str(ThreeDconst.OPERATIONS))
@click.argument('radius', nargs=1)
def sphere(operation, radius):
    """Calculate Sphere Opearions"""
    if operation.casefold() in ThreeDconst.OPERATIONS:
        sp = ThreeD()
        print('Sphere '+ operation.casefold() + '= %f' % (sp.calculateSphereOperation(float(radius),operation.casefold())))
    else:
        print('Invalid Operation')

@main.command('cube', help='List of operations performed on Cube.')
@click.option('--operation', '-o', 'operation', required=True,
              help="List of Operation Performed are "+ str(ThreeDconst.OPERATIONS))
@click.argument('side', nargs=1)
def cube(operation, side):
    """Calculate Cube Opearions"""
    if operation.casefold() in ThreeDconst.OPERATIONS:
        cb = ThreeD()
        print('Cube '+ operation.casefold() + '= %f' % (cb.calculateCubeOperation(float(side),operation.casefold())))
    else:
        print('Invalid Operation')


@main.command('cone', help='List of operations performed on cone.')
@click.option('--operation', '-o', 'operation', required=True,
              help="List of Operation Performed are "+ str(ThreeDconst.OPERATIONS))
@click.argument('radius', nargs=1)
@click.argument('height', nargs=1)
def cone(operation, radius, height):
    """Calculate Cone Opearions"""
    if operation.casefold() in ThreeDconst.OPERATIONS:
        cn = ThreeD()
        print('Cone '+ operation.casefold() + '= %f' % (cn.calculateConeOperation(float(radius), float(height),operation.casefold())))
    else:
        print('Invalid Operation')

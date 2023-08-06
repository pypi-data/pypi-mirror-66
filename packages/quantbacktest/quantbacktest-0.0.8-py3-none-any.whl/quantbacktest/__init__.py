# __init__.py
__version__ = "0.0.8"

# Importing modules from this repository
import sys
PATH_TO_PROJECT = '/home/janspoerer/code/janspoerer/quantbacktest'
sys.path.insert(1, PATH_TO_PROJECT + '/quantbacktest/components')

from _0_wrappers import backtest_visualizer

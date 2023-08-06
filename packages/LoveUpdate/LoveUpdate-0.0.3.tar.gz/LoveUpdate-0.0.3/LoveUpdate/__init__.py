import os
import sys
ordir=os.getcwd()
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
from update import *
from report import *
os.chdir(ordir)
del ordir
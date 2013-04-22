import os
import sys
import unittest
from IndexTest import IndexTest

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(1, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(2, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(2, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

unittest.TextTestRunner().run(IndexTest())
